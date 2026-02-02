#!/usr/bin/env python3
"""
Simple Crawlee test crawler
"""

import asyncio
import sys
from pathlib import Path

from crawlee import PlaywrightCrawler


class SimpleCrawler(PlaywrightCrawler):
    """Simple test crawler."""

    async def start(self):
        """Start crawling."""
        print("Starting crawler...")
        
        # Add request handler
        @self.router.default_handler
        async def request_handler(context, request):
            print(f"Processing: {request.url}")
            
            # Wait a bit (human-like)
            await asyncio.sleep(2)
            
            # Extract some data
            page = await context.new_page()
            await page.goto(request.url)
            
            # Get title
            title = await page.title()
            print(f"Title: {title}")
            
            # Extract some links
            links = await page.locator('a[href]').count()
            print(f"Found {links} links")
            
            await page.close()

        # Start crawling
        await self.run(['https://finance.yahoo.com/news'])


async def main():
    """Main execution."""
    print("=" * 70)
    print("CRAWLEE TEST CRAWLER")
    print("=" * 70)
    
    crawler = SimpleCrawler(
        max_requests_per_crawl=5,
        headless=True  # Try headless first
    )
    
    try:
        await crawler.start()
        print("\n✅ Crawl complete!")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
