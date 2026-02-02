#!/usr/bin/env python3
"""
Advanced News Crawler: RSS + Newspaper3k for Full Content Extraction
Combines RSS feeds with Newspaper3k for complete article extraction
"""

import sys
import json
from datetime import datetime, timedelta
import feedparser
import requests
from newspaper import Article, Config
from bs4 import BeautifulSoup


# RSS feeds
RSS_SOURCES = {
    'yahoo_finance_gold': {
        'url': 'https://finance.yahoo.com/rss/u/gold',
        'name': 'Yahoo Finance Gold'
    },
    'yahoo_finance_tech': {
        'url': 'https://finance.yahoo.com/rss/u/technology',
        'name': 'Yahoo Finance Technology'
    },
    'cnbc': {
        'url': 'https://www.cnbc.com/id/10000664/device/rss/rss.html',
        'name': 'CNBC Markets'
    }
}


def fetch_rss_feed(feed_url):
    """Fetch RSS feed."""
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


def extract_full_article(url):
    """Extract full article using Newspaper3k."""
    try:
        config = Config()
        config.fetch_images = False
        config.memoize_articles = False
        
        article = Article(url, config=config)
        article.download()
        article.parse()
        
        if article.is_downloaded and article.is_parsed:
            return {
                'full_text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'keywords': article.keywords,
                'summary': article.summary
            }
        else:
            return None
            
    except Exception as e:
        print(f"    ✗ Error extracting {url}: {e}")
        return None


def process_rss_entry(entry, source_name, extract_content=False):
    """Process single RSS entry."""
    published = None
    if entry.get('published_parsed'):
        published = datetime(*entry['published_parsed'][:6])
    else:
        published = datetime.now()
    
    article_data = {
        'source': source_name,
        'title': entry.get('title', 'No title'),
        'url': entry.get('link'),
        'summary': entry.get('summary', '')[:500],
        'published': published.isoformat(),
        'scraped_at': datetime.now().isoformat()
    }
    
    # Extract full content if requested
    if extract_content and article_data['url']:
        print(f"    Extracting full content: {article_data['url'][:50]}...")
        full_content = extract_full_article(article_data['url'])
        
        if full_content:
            article_data['full_content'] = full_content['full_text']
            article_data['authors'] = full_content.get('authors', [])
            article_data['publish_date'] = full_content.get('publish_date')
            article_data['keywords'] = full_content.get('keywords', [])
            article_data['top_image'] = full_content.get('top_image')
            print(f"    ✓ Full content extracted ({len(full_content['full_text'])} chars)")
        else:
            print(f"    ✗ Failed to extract full content")
            article_data['full_content'] = None
    
    return article_data


def crawl_rss_source(feed_name, feed_config, max_articles=10, extract_content=False):
    """Crawl news from RSS source with optional full content extraction."""
    print(f"\nCrawling: {feed_config['name']}...")
    
    feed = fetch_rss_feed(feed_config['url'])
    
    if not feed:
        print(f"  ✗ No feed data")
        return []
    
    articles = []
    
    for i, entry in enumerate(feed.entries[:max_articles], 1):
        try:
            article = process_rss_entry(entry, feed_config['name'], extract_content)
            articles.append(article)
            
            if i % 5 == 0:
                print(f"  ✓ Processed {i}/{min(len(feed.entries), max_articles)} articles")
                
        except Exception as e:
            print(f"  ✗ Error processing entry {i}: {e}")
            continue
    
    print(f"  ✓ Complete: {len(articles)} articles")
    return articles


def filter_recent_articles(articles, hours=24):
    """Filter articles from last N hours."""
    cutoff = datetime.now() - timedelta(hours=hours)
    return [a for a in articles if datetime.fromisoformat(a['scraped_at']) >= cutoff]


def filter_by_sector(articles, sector=None):
    """Filter articles by sector keywords."""
    if not sector:
        return articles
    
    sector = sector.lower()
    keywords = {
        'gold': ['gold', 'xau', 'precious metal', 'bullion', 'safe haven'],
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
        # Search in title, summary, and full content
        text_to_search = f"{article['title']} {article.get('summary', '')} {article.get('full_content', '')}".lower()
        if any(kw in text_to_search for kw in sector_keywords):
            filtered.append(article)
    
    print(f"\n🔍 Filtered by '{sector}': {len(filtered)}/{len(articles)} articles")
    return filtered


def deduplicate_articles(articles):
    """Remove duplicates by URL."""
    seen_urls = set()
    unique = []
    
    for article in articles:
        url = article.get('url')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(article)
    
    print(f"\n🔎 Deduplication: {len(articles)} → {len(unique)} articles")
    return unique


def save_articles(articles, filepath=None):
    """Save articles to JSON."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/news_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filepath, 'w') as f:
        json.dump(articles, f, indent=2, default=str)
    
    print(f"\n📁 Articles saved to: {filepath}")
    return filepath


def display_news_summary(articles, limit=5):
    """Display summary of crawled news."""
    print("\n" + "=" * 70)
    print("NEWS SUMMARY (FULL CONTENT)")
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
            print(f"\n  {i}. {article['title'][:60]}...")
            print(f"     URL: {article['url']}")
            print(f"     Published: {article['published']}")
            
            # Show summary
            if article.get('summary'):
                print(f"     Summary: {article['summary'][:80]}...")
            
            # Show full content snippet
            if article.get('full_content'):
                print(f"     Full Content: {article['full_content'][:150]}...")
            else:
                print(f"     Full Content: [not extracted]")
            
            print("-" * 60)
    
    print("\n" + "=" * 70)


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced RSS + Newspaper3k News Crawler')
    parser.add_argument('--sources', '-s', nargs='+',
                       help='Specific RSS sources to crawl')
    parser.add_argument('--max', '-m', type=int, default=10, help='Max articles per source')
    parser.add_argument('--hours', type=int, default=24, help='Only recent articles (hours)')
    parser.add_argument('--sector', help='Filter by sector: gold, tech, crypto, energy, healthcare')
    parser.add_argument('--full', '-f', action='store_true',
                       help='Extract full article content with Newspaper3k (slower)')
    parser.add_argument('--save', action='store_true', help='Save to file')
    parser.add_argument('--summary', action='store_true', help='Display summary')
    args = parser.parse_args()
    
    # Filter sources
    if args.sources:
        sources_to_crawl = {k: v for k, v in RSS_SOURCES.items() if k in args.sources}
    else:
        sources_to_crawl = RSS_SOURCES
    
    print("\n" + "=" * 70)
    print("ADVANCED NEWS CRAWLER (RSS + Newspaper3k)")
    print("=" * 70)
    print(f"Crawling: {', '.join(sources_to_crawl.keys())}")
    print(f"Max articles: {args.max} per source")
    if args.full:
        print("Full content extraction: ENABLED (slower)")
    print("=" * 70)
    
    # Crawl all sources
    all_articles = []
    
    for feed_name, feed_config in sources_to_crawl.items():
        articles = crawl_rss_source(feed_name, feed_config, args.max, args.full)
        all_articles.extend(articles)
    
    # Filter
    articles = filter_recent_articles(all_articles, args.hours)
    articles = deduplicate_articles(articles)
    
    # Sector filter
    if args.sector:
        articles = filter_by_sector(articles, args.sector)
    
    print(f"\nTotal: {len(articles)} articles")
    
    # Stats
    full_content_count = len([a for a in articles if a.get('full_content')])
    print(f"With full content: {full_content_count}/{len(articles)}")
    
    # Save
    if args.save:
        filepath = save_articles(articles)
    
    # Display
    if args.summary or not args.save:
        display_news_summary(articles, limit=3)
    
    print(f"\n✅ Crawl complete!")


if __name__ == '__main__':
    main()
