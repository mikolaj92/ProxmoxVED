#!/usr/bin/env python3
"""
Recursively crawl a website.
Usage: python3 crawl.py <url> [--depth <n>] [--limit <n>] [--include <pattern>] [--exclude <pattern>]
"""

import sys
import json
import argparse
import time
from urllib.parse import urljoin, urlparse
from collections import deque
import requests
from bs4 import BeautifulSoup
from fetch import fetch_page, extract_content


def should_crawl(url, base_domain, include_patterns=None, exclude_patterns=None):
    """Check if URL should be crawled."""
    parsed = urlparse(url)

    # Same domain only
    if parsed.netloc != base_domain:
        return False

    # Include patterns
    if include_patterns:
        if not any(pattern in url for pattern in include_patterns):
            return False

    # Exclude patterns
    if exclude_patterns:
        if any(pattern in url for pattern in exclude_patterns):
            return False

    # Skip common non-content paths
    skip_extensions = ('.pdf', '.jpg', '.png', '.gif', '.css', '.js', '.zip', '.exe')
    if any(url.lower().endswith(ext) for ext in skip_extensions):
        return False

    return True


def extract_links_from_page(soup, base_url):
    """Extract all links from a page."""
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute = urljoin(base_url, href)
        links.add(absolute)
    return links


def crawl(start_url, max_depth=1, max_pages=100, delay=0,
           include_patterns=None, exclude_patterns=None):
    """Crawl website recursively."""
    base_domain = urlparse(start_url).netloc
    visited = set()
    results = []
    queue = deque([(start_url, 0)])

    while queue and len(visited) < max_pages:
        url, depth = queue.popleft()

        if url in visited or depth > max_depth:
            continue

        print(f"Crawling: {url} (depth: {depth}, visited: {len(visited)})")

        try:
            response = fetch_page(url)
            soup = BeautifulSoup(response.text, 'lxml')

            # Extract content
            page_data = {
                'url': url,
                'depth': depth,
                'status': response.status_code,
                'title': soup.title.string if soup.title else None,
                'content': extract_content(soup)[:2000]
            }
            results.append(page_data)
            visited.add(url)

            # Find links to crawl further
            if depth < max_depth:
                links = extract_links_from_page(soup, url)
                for link in links:
                    if should_crawl(link, base_domain, include_patterns, exclude_patterns):
                        if link not in visited and link not in [u for u, _ in queue]:
                            queue.append((link, depth + 1))

            # Rate limiting
            if delay > 0:
                time.sleep(delay)

        except Exception as e:
            print(f"Error crawling {url}: {e}", file=sys.stderr)

    return results


def main():
    parser = argparse.ArgumentParser(description='Recursively crawl a website')
    parser.add_argument('url', help='Starting URL')
    parser.add_argument('--depth', '-d', type=int, default=1, help='Max crawl depth')
    parser.add_argument('--limit', '-l', type=int, default=100, help='Max pages to visit')
    parser.add_argument('--delay', type=float, default=0, help='Delay between requests (seconds)')
    parser.add_argument('--include', '-i', action='append', help='URL pattern to include')
    parser.add_argument('--exclude', '-e', action='append', help='URL pattern to exclude')
    parser.add_argument('--output', '-o', help='Save results to JSON file')
    args = parser.parse_args()

    print(f"Starting crawl of {args.url}")
    print(f"Max depth: {args.depth}, Max pages: {args.limit}")
    print(f"Include patterns: {args.include}")
    print(f"Exclude patterns: {args.exclude}")
    print("=" * 60)

    results = crawl(
        args.url,
        max_depth=args.depth,
        max_pages=args.limit,
        delay=args.delay,
        include_patterns=args.include,
        exclude_patterns=args.exclude
    )

    print("\n" + "=" * 60)
    print(f"Crawl complete: {len(results)} pages visited")

    # Output summary
    for i, page in enumerate(results[:5], 1):
        print(f"\n{i}. {page['title'] or 'No title'}")
        print(f"   URL: {page['url']}")
        print(f"   Depth: {page['depth']}, Status: {page['status']}")

    if len(results) > 5:
        print(f"\n... and {len(results) - 5} more pages")

    # Save to file
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {args.output}")


if __name__ == '__main__':
    main()
