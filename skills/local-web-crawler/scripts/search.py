#!/usr/bin/env python3
"""
Search for text within a fetched page.
Usage: python3 search.py <url> <search_term>
"""

import sys
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fetch import fetch_page, extract_content


def search_in_text(text, term, case_sensitive=False):
    """Search for term in text and return matches with context."""
    if not case_sensitive:
        text = text.lower()
        term = term.lower()

    matches = []
    lines = text.split('\n')

    for i, line in enumerate(lines):
        if term in line:
            # Get context (5 lines before and after)
            start = max(0, i - 5)
            end = min(len(lines), i + 6)
            context = '\n'.join(lines[start:end])

            matches.append({
                'line_number': i + 1,
                'line': line,
                'context': context
            })

    return matches


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 search.py <url> <search_term>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    search_term = sys.argv[2]
    case_sensitive = '--case-sensitive' in sys.argv

    try:
        response = fetch_page(url)
        soup = BeautifulSoup(response.text, 'lxml')

        # Search in content
        content = extract_content(soup)
        matches = search_in_text(content, search_term, case_sensitive)

        # Search in links
        link_matches = []
        for link in soup.find_all('a', href=True):
            text = link.get_text(strip=True)
            if search_term.lower() in text.lower():
                href = urljoin(url, link['href'])
                link_matches.append({'text': text, 'url': href})

        # Output
        print(f"Searching for '{search_term}' in {url}\n")
        print(f"Content matches: {len(matches)}")
        print(f"Link matches: {len(link_matches)}\n")

        if matches:
            print("=" * 60)
            print("CONTENT MATCHES")
            print("=" * 60)
            for match in matches[:10]:  # First 10 matches
                print(f"\n[Line {match['line_number']}]")
                print(f"{match['line']}")
                print(f"Context:\n{match['context']}")
                print("-" * 60)

        if link_matches:
            print("\n" + "=" * 60)
            print("LINK MATCHES")
            print("=" * 60)
            for match in link_matches[:10]:
                print(f"\n- {match['text']}")
                print(f"  {match['url']}")

        if not matches and not link_matches:
            print("No matches found.")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
