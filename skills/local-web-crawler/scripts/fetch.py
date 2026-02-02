#!/usr/bin/env python3
"""
Fetch and extract content from a single URL.
Usage: python3 fetch.py <url> [--json] [--markdown] [--output <file>]
"""

import sys
import json
import argparse
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests


def fetch_page(url, timeout=10, headers=None):
    """Fetch page and return response."""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    response = requests.get(url, timeout=timeout, headers=headers)
    response.raise_for_status()
    return response


def extract_links(soup, base_url):
    """Extract all links from page."""
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute = urljoin(base_url, href)
        links.append({
            'text': link.get_text(strip=True),
            'url': absolute
        })
    return links


def extract_content(soup):
    """Extract clean text content."""
    # Remove script and style elements
    for script in soup(['script', 'style', 'nav', 'footer']):
        script.decompose()

    text = soup.get_text()
    # Clean whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def html_to_markdown(soup):
    """Convert HTML to Markdown (simplified)."""
    markdown = []

    # Title
    title = soup.find('title')
    if title:
        markdown.append(f"# {title.get_text()}\n")

    # Headings
    for i in range(1, 7):
        for heading in soup.find_all(f'h{i}'):
            markdown.append(f"{'#' * i} {heading.get_text()}\n")

    # Links
    for link in soup.find_all('a', href=True):
        text = link.get_text(strip=True)
        href = link['href']
        markdown.append(f"[{text}]({href})")

    return '\n'.join(markdown)


def main():
    parser = argparse.ArgumentParser(description='Fetch and extract content from a URL')
    parser.add_argument('url', help='URL to fetch')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--markdown', action='store_true', help='Convert to Markdown')
    parser.add_argument('--output', '-o', help='Save to file')
    args = parser.parse_args()

    try:
        response = fetch_page(args.url)
        soup = BeautifulSoup(response.text, 'lxml')

        result = {
            'url': args.url,
            'status': response.status_code,
            'title': soup.title.string if soup.title else None,
            'links': extract_links(soup, args.url),
            'content': extract_content(soup)[:5000]  # First 5k chars
        }

        if args.markdown:
            result['markdown'] = html_to_markdown(soup)

        if args.json:
            output = json.dumps(result, indent=2)
        else:
            output = f"URL: {result['url']}\n"
            output += f"Status: {result['status']}\n"
            output += f"Title: {result['title']}\n\n"
            output += f"Links found: {len(result['links'])}\n\n"
            output += f"Content:\n{result['content']}\n"
            if args.markdown:
                output += f"\nMarkdown:\n{result['markdown']}\n"

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Saved to {args.output}")
        else:
            print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
