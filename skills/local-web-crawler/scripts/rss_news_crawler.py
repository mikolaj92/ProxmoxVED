#!/usr/bin/env python3
"""
RSS News Crawler - legal, rate-limit friendly way to get news.
Sources: Yahoo Finance, Financial Times, CNBC, etc.
"""

import sys
import json
from datetime import datetime, timedelta
import feedparser
from bs4 import BeautifulSoup
import requests


# RSS feeds (legal, no blocking)
RSS_SOURCES = {
    'yahoo_finance_markets': {
        'url': 'https://finance.yahoo.com/rss/',
        'name': 'Yahoo Finance Markets'
    },
    'yahoo_finance_gold': {
        'url': 'https://finance.yahoo.com/rss/u/gold',
        'name': 'Yahoo Finance Gold'
    },
    'yahoo_finance_tech': {
        'url': 'https://finance.yahoo.com/rss/u/technology',
        'name': 'Yahoo Finance Technology'
    },
    'cnbc_markets': {
        'url': 'https://www.cnbc.com/id/10000664/device/rss/rss.html',
        'name': 'CNBC Markets'
    },
    'ft_markets': {
        'url': 'https://www.ft.com/rss/world/us',
        'name': 'Financial Times'
    }
}


def fetch_rss_feed(feed_url):
    """Fetch RSS feed with error handling."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    try:
        response = requests.get(feed_url, headers=headers, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.text)
    except Exception as e:
        print(f"  ✗ Error fetching RSS: {e}")
        return None


def extract_article_content(url, timeout=10):
    """Extract full article content from URL."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # Remove scripts, styles
        for elem in soup(['script', 'style', 'nav', 'footer', 'aside']):
            elem.decompose()

        # Try different content selectors
        content = None

        # Try common article containers
        for selector in ['article', '[data-component="articleBody"]',
                        '.article-body', '.story-content', '.article__content']:
            elem = soup.select_one(selector)
            if elem:
                content = elem.get_text(separator=' ', strip=True)
                break

        # Fallback to body
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text(separator=' ', strip=True)

        return content[:2000] if content else None  # First 2000 chars

    except:
        return None


def process_rss_entry(entry, source_name):
    """Process single RSS entry into article dict."""
    published = entry.get('published_parsed')
    if published:
        published_dt = datetime(*published[:6])
    else:
        published_dt = datetime.now()

    return {
        'source': source_name,
        'title': entry.get('title', 'No title'),
        'url': entry.get('link'),
        'summary': entry.get('summary', ''),
        'published': published_dt.isoformat(),
        'scraped_at': datetime.now().isoformat()
    }


def crawl_rss_source(feed_name, feed_config, max_articles=20, fetch_content=False):
    """Crawl news from a single RSS source."""
    print(f"\nCrawling {feed_config['name']}...")

    feed = fetch_rss_feed(feed_config['url'])

    if not feed:
        print(f"  ✗ No feed data")
        return []

    articles = []

    for i, entry in enumerate(feed.entries[:max_articles], 1):
        try:
            article = process_rss_entry(entry, feed_config['name'])

            # Extract full content if requested
            if fetch_content:
                article['content'] = extract_article_content(article['url'])

            articles.append(article)

            print(f"  ✓ {i}: {article['title'][:60]}...")

        except Exception as e:
            print(f"  ✗ Error processing entry {i}: {e}")
            continue

    print(f"  ✓ Found {len(articles)} articles")
    return articles


def filter_recent_articles(articles, hours=24):
    """Filter articles from last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours)
    return [a for a in articles if datetime.fromisoformat(a['published']) >= cutoff]


def filter_by_sector(articles, sector=None):
    """
    Filter articles by sector keywords.
    Sectors: gold, tech, crypto, energy, healthcare, etc.
    """
    if not sector:
        return articles

    sector = sector.lower()
    keywords = {
        'gold': ['gold', 'xau', 'precious metal', 'yellow metal', 'bullion'],
        'tech': ['technology', 'tech', 'software', 'ai', 'artificial intelligence',
                 'cloud', 'semiconductor', 'chip', 'saas', 'data'],
        'crypto': ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'blockchain', 'defi'],
        'energy': ['oil', 'gas', 'energy', 'petroleum', 'fossil fuel'],
        'healthcare': ['healthcare', 'pharma', 'biotech', 'medical', 'drug', 'fda']
    }

    if sector not in keywords:
        print(f"Unknown sector: {sector}. Available: {list(keywords.keys())}")
        return articles

    sector_keywords = keywords[sector]
    filtered = []

    for article in articles:
        text = f"{article['title']} {article['summary']}".lower()
        if any(kw in text for kw in sector_keywords):
            filtered.append(article)

    print(f"\n🔍 Filtered by '{sector}': {len(filtered)}/{len(articles)} articles")
    return filtered


def deduplicate_articles(articles):
    """Remove duplicate articles by URL."""
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article['url']
        if url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    print(f"\n🔎 Deduplication: {len(articles)} → {len(unique_articles)} articles")
    return unique_articles


def save_articles(articles, filepath=None):
    """Save articles to JSON file."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/rss_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filepath, 'w') as f:
        json.dump(articles, f, indent=2)

    print(f"\n📁 Articles saved to: {filepath}")
    return filepath


def display_news_summary(articles, limit=10):
    """Display summary of crawled news."""
    print("\n" + "=" * 70)
    print("NEWS SUMMARY")
    print("=" * 70)

    # Group by source
    by_source = {}
    for article in articles:
        source = article['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(article)

    for source, source_articles in by_source.items():
        print(f"\n{source.upper()} ({len(source_articles)} articles):")
        for i, article in enumerate(source_articles[:limit], 1):
            print(f"\n  {i}. {article['title']}")
            print(f"     URL: {article['url']}")
            print(f"     Published: {article['published']}")

    print("\n" + "=" * 70)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='RSS News Crawler')
    parser.add_argument('--sources', '-s', nargs='+',
                       help='Specific RSS sources to crawl (yahoo_finance_markets, yahoo_finance_gold, yahoo_finance_tech)')
    parser.add_argument('--max', '-m', type=int, default=20, help='Max articles per source')
    parser.add_argument('--hours', type=int, default=24, help='Only recent articles (hours)')
    parser.add_argument('--sector', help='Filter by sector: gold, tech, crypto, energy, healthcare')
    parser.add_argument('--content', '-c', action='store_true', help='Fetch full article content')
    parser.add_argument('--save', action='store_true', help='Save to file')
    parser.add_argument('--summary', action='store_true', help='Display summary')

    args = parser.parse_args()

    # Filter sources
    if args.sources:
        sources_to_crawl = {k: v for k, v in RSS_SOURCES.items() if k in args.sources}
    else:
        sources_to_crawl = RSS_SOURCES

    print("\n" + "=" * 70)
    print("RSS NEWS CRAWLER")
    print("=" * 70)
    print(f"Crawling: {', '.join(sources_to_crawl.keys())}")
    print(f"Max articles: {args.max} per source")

    # Crawl all sources
    all_articles = []

    for feed_name, feed_config in sources_to_crawl.items():
        articles = crawl_rss_source(feed_name, feed_config, args.max, args.content)
        all_articles.extend(articles)

    # Filter
    articles = filter_recent_articles(all_articles, args.hours)
    articles = deduplicate_articles(articles)

    # Sector filter
    if args.sector:
        articles = filter_by_sector(articles, args.sector)

    print(f"\nTotal: {len(articles)} articles")

    # Save
    if args.save:
        filepath = save_articles(articles)

    # Display
    if args.summary or not args.save:
        display_news_summary(articles, limit=5)

    print(f"\n✅ RSS crawl complete!")


if __name__ == '__main__':
    main()
