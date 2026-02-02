#!/usr/bin/env python3
"""
Crawl financial news from multiple sources for sentiment analysis.
Sources: Yahoo Finance, Reuters, Bloomberg, MarketWatch, Seeking Alpha
"""

import sys
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from macro_data import fetch_page


NEWS_SOURCES = {
    'yahoo_finance': {
        'url': 'https://finance.yahoo.com/news',
        'name': 'Yahoo Finance',
        'article_selector': 'div.js-stream-content',
        'title_selector': 'h3',
        'link_selector': 'a',
        'summary_selector': 'p'
    },
    'reuters': {
        'url': 'https://www.reuters.com/markets',
        'name': 'Reuters',
        'article_selector': 'article[data-testid="media-story-card"]',
        'title_selector': 'h3',
        'link_selector': 'a',
        'summary_selector': 'p'
    },
    'marketwatch': {
        'url': 'https://www.marketwatch.com/latest-news',
        'name': 'MarketWatch',
        'article_selector': 'div.article__content',
        'title_selector': 'h3',
        'link_selector': 'a',
        'summary_selector': 'p'
    },
    'seeking_alpha': {
        'url': 'https://seekingalpha.com/market-news',
        'name': 'Seeking Alpha',
        'article_selector': 'article',
        'title_selector': 'h3',
        'link_selector': 'a',
        'summary_selector': 'p'
    }
}


def crawl_source(source_name, source_config, max_articles=20):
    """Crawl news from a single source."""
    print(f"Crawling {source_name}...")

    try:
        response = fetch_page(source_config['url'])
        soup = BeautifulSoup(response.text, 'lxml')

        articles = []

        # Find article elements
        article_elements = soup.select(source_config['article_selector'])

        for i, elem in enumerate(article_elements[:max_articles]):
            try:
                # Extract title
                title_elem = elem.select_one(source_config['title_selector'])
                title = title_elem.get_text(strip=True) if title_elem else "No title"

                # Extract link
                link_elem = elem.select_one(source_config['link_selector'])
                link = link_elem.get('href') if link_elem else None

                # Make absolute URL if needed
                if link and not link.startswith('http'):
                    base_url = source_config['url'].split('/')[0] + '//' + source_config['url'].split('/')[2]
                    link = base_url + link

                # Extract summary
                summary_elem = elem.select_one(source_config['summary_selector'])
                summary = summary_elem.get_text(strip=True) if summary_elem else title

                # Extract timestamp if available
                time_elem = elem.select_one('time')
                timestamp = time_elem.get('datetime') if time_elem else datetime.now().isoformat()

                articles.append({
                    'source': source_name,
                    'title': title,
                    'url': link,
                    'summary': summary,
                    'timestamp': timestamp,
                    'scraped_at': datetime.now().isoformat()
                })

            except Exception as e:
                print(f"Error parsing article {i} from {source_name}: {e}")
                continue

        print(f"  ✓ Found {len(articles)} articles")
        return articles

    except Exception as e:
        print(f"  ✗ Error crawling {source_name}: {e}")
        return []


def crawl_all_sources(max_articles_per_source=20):
    """Crawl all configured news sources."""
    print("\n" + "=" * 70)
    print("CRAWLING FINANCIAL NEWS")
    print("=" * 70 + "\n")

    all_articles = []

    for source_name, source_config in NEWS_SOURCES.items():
        articles = crawl_source(source_name, source_config, max_articles_per_source)
        all_articles.extend(articles)

    print(f"\nTotal articles crawled: {len(all_articles)}")

    return all_articles


def filter_recent_articles(articles, hours=24):
    """Filter articles from last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours)
    return [a for a in articles if datetime.fromisoformat(a['scraped_at']) >= cutoff]


def deduplicate_articles(articles):
    """Remove duplicate articles (by title similarity)."""
    seen_titles = set()
    unique_articles = []

    for article in articles:
        title_lower = article['title'].lower()
        # Simple dedup by exact title match
        if title_lower not in seen_titles:
            seen_titles.add(title_lower)
            unique_articles.append(article)

    return unique_articles


def save_articles(articles, filepath=None):
    """Save articles to JSON file."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filepath, 'w') as f:
        json.dump(articles, f, indent=2)

    print(f"\nArticles saved to: {filepath}")
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
        print(f"\n{source.upper()}:")
        for i, article in enumerate(source_articles[:limit], 1):
            print(f"\n  {i}. {article['title']}")
            print(f"     URL: {article['url']}")
            print(f"     {article['summary'][:100]}...")

    print("\n" + "=" * 70)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Crawl financial news')
    parser.add_argument('--sources', '-s', nargs='+', help='Specific sources to crawl')
    parser.add_argument('--max', '-m', type=int, default=20, help='Max articles per source')
    parser.add_argument('--hours', type=int, default=24, help='Only recent articles (hours)')
    parser.add_argument('--save', action='store_true', help='Save to file')
    parser.add_argument('--summary', action='store_true', help='Display summary')

    args = parser.parse_args()

    # Filter sources if specified
    if args.sources:
        sources_to_crawl = {k: v for k, v in NEWS_SOURCES.items() if k in args.sources}
    else:
        sources_to_crawl = NEWS_SOURCES

    print(f"Crawling: {', '.join(sources_to_crawl.keys())}")

    # Crawl news
    articles = crawl_all_sources(args.max)

    # Filter and dedupe
    articles = filter_recent_articles(articles, args.hours)
    articles = deduplicate_articles(articles)

    print(f"After filtering: {len(articles)} unique articles from last {args.hours} hours")

    # Save if requested
    if args.save:
        filepath = save_articles(articles)

    # Display summary if requested
    if args.summary or not args.save:
        display_news_summary(articles, limit=5)

    print(f"\n✅ News crawl complete!")


if __name__ == '__main__':
    main()
