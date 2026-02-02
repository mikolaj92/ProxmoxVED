#!/usr/bin/env python3
"""
Sector-Specific Market Intelligence Agent
Focus: GOLD + TECH sectors
Uses: RSS feeds, FRED API, LM Studio sentiment analysis
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class SectorMarketAgent:
    """Market intelligence agent focused on specific sectors."""

    def __init__(self, workspace="/Users/mini-m4-1/clawd"):
        self.workspace = workspace
        self.news_file = None
        self.sentiment_file = None
        self.macro_file = None
        self.today_dir = workspace + f"/.learnings/daily/{datetime.now().strftime('%Y%m%d')}"
        Path(self.today_dir).mkdir(parents=True, exist_ok=True)

    def crawl_news(self, sources=None, sector=None, max_articles=20):
        """Crawl news using RSS feeds."""
        print("\n" + "=" * 70)
        print("STEP 1: CRAWLING NEWS (RSS)")
        print("=" * 70)

        # Default sources for GOLD + TECH
        if sources is None:
            sources = ['yahoo_finance_gold', 'yahoo_finance_tech']

        cmd = f"cd {self.workspace} && source venv/bin/activate && "
        cmd += f"python3 skills/local-web-crawler/scripts/rss_news_crawler.py "
        cmd += f"--sources {' '.join(sources)} "
        if sector:
            cmd += f"--sector {sector} "
        cmd += f"--max {max_articles} --save --summary"

        os.system(cmd)

        # Find latest news file
        news_files = sorted(Path(self.workspace + "/.learnings").glob("rss_news_*.json"))
        if news_files:
            self.news_file = str(news_files[-1])
            print(f"\n✓ News saved to: {self.news_file}")

    def fetch_macro_data(self, api_key=None):
        """Fetch macro data from FRED API."""
        print("\n" + "=" * 70)
        print("STEP 2: FETCHING MACRO DATA (FRED API)")
        print("=" * 70)

        cmd = f"cd {self.workspace} && source venv/bin/activate && "
        if api_key:
            cmd += f"FRED_API_KEY={api_key} "
        cmd += f"python3 skills/local-web-crawler/scripts/fred_api.py --save"

        os.system(cmd)

        # Find latest macro file
        macro_files = sorted(Path(self.workspace + "/.learnings").glob("macro_*.json"))
        if macro_files:
            self.macro_file = str(macro_files[-1])
            print(f"\n✓ Macro data saved to: {self.macro_file}")

    def analyze_sentiment(self, limit=50):
        """Analyze sentiment using LM Studio."""
        if not self.news_file:
            print("\n✗ No news file available. Run crawl_news() first.")
            return

        print("\n" + "=" * 70)
        print("STEP 3: ANALYZING SENTIMENT WITH AI")
        print("=" * 70)

        cmd = f"cd {self.workspace} && source venv/bin/activate && "
        cmd += f"python3 skills/local-web-crawler/scripts/sentiment_analyzer.py "
        cmd += f"--news-file {self.news_file} --limit {limit} --save"

        os.system(cmd)

        # Find latest sentiment file
        sentiment_files = sorted(Path(self.workspace + "/.learnings").glob("sentiment_*.json"))
        if sentiment_files:
            self.sentiment_file = str(sentiment_files[-1])
            print(f"\n✓ Sentiment saved to: {self.sentiment_file}")

    def load_sentiment(self):
        """Load latest sentiment analysis."""
        if not self.sentiment_file:
            return None

        with open(self.sentiment_file) as f:
            return json.load(f)

    def load_macro(self):
        """Load latest macro data."""
        if not self.macro_file:
            return None

        with open(self.macro_file) as f:
            return json.load(f)

    def determine_cycle_archetype(self, sentiment_data, macro_data):
        """
        Determine cycle archetype using sentiment + macro.
        Returns: archetype, investment_strategy, risk_level
        """
        sentiment_score = 0
        macro_score = 0

        # Sentiment score
        if sentiment_data:
            aggregate = sentiment_data.get('aggregate', {})
            sentiment_score = aggregate.get('weighted_sentiment_score', 0)

        # Macro health score
        if macro_data:
            health = macro_data.get('health_score', {})
            macro_score = health.get('score', 0)

        # Combined score (60% sentiment, 40% macro)
        combined_score = (sentiment_score * 0.6) + (macro_score * 0.4)

        # Archetype mapping
        if combined_score > 40:
            archetype = "LATE EXPANSION / PEAK"
            strategy = "REDUCE RISK - Trim positions, increase cash, defensive sectors"
            risk_level = "HIGH (Euphoria)"

        elif combined_score > 20:
            archetype = "MID-TO-LATE EXPANSION"
            strategy = "MODERATE - Balanced exposure, rotate to defensives"
            risk_level = "MEDIUM-HIGH"

        elif combined_score > 0:
            archetype = "MID EXPANSION"
            strategy = "HEALTHY - Continue balanced portfolio, quality growth"
            risk_level = "MEDIUM"

        elif combined_score > -20:
            archetype = "EARLY EXPANSION / CORRECTION"
            strategy = "OPPORTUNISTIC - Look for quality dips, start accumulating"
            risk_level = "MEDIUM"

        elif combined_score > -40:
            archetype = "EARLY RECOVERY / TROUGH"
            strategy = "ACCUMULATE - Buy quality on weakness, contrarian"
            risk_level = "HIGH (but measured)"

        else:
            archetype = "DEEP RECESSION / EXTREME FEAR"
            strategy = "AGGRESSIVE - Maximum pessimism, buy quality aggressively"
            risk_level = "HIGH (opportunity)"

        return {
            'archetype': archetype,
            'strategy': strategy,
            'risk_level': risk_level,
            'combined_score': combined_score,
            'sentiment_score': sentiment_score,
            'macro_score': macro_score
        }

    def get_sector_recommendation(self, archetype):
        """Get sector-specific recommendations."""
        strategy_map = {
            'LATE EXPANSION / PEAK': {
                'GOLD': "Reduce - Safe haven not needed, rotate to defensives",
                'TECH': "Reduce - Valuations stretched, lock in profits"
            },
            'MID-TO-LATE EXPANSION': {
                'GOLD': "Small allocation - Inflation hedge",
                'TECH': "Moderate - Focus on quality, avoid hype"
            },
            'MID EXPANSION': {
                'GOLD': "Small - Inflation risk modest",
                'TECH': "Increase - Growth favorable, add quality names"
            },
            'EARLY EXPANSION / CORRECTION': {
                'GOLD': "Moderate - Safe haven allocation",
                'TECH': "Hold - Wait for clear signals"
            },
            'EARLY RECOVERY / TROUGH': {
                'GOLD': "Significant - Safe haven demand high",
                'TECH': "Selectively - Quality tech on weakness"
            },
            'DEEP RECESSION / EXTREME FEAR': {
                'GOLD': "Maximum - Ultimate safe haven",
                'TECH': "Aggressive - Maximum pessimism, buy quality"
            }
        }

        archetype_key = archetype.split('/')[0].strip().upper()
        return strategy_map.get(archetype, {
            'GOLD': "Evaluate based on cycle position",
            'TECH': "Evaluate based on cycle position"
        })

    def save_daily_report(self, report):
        """Save daily report."""
        # Save to today's folder
        today_file = self.today_dir + "/sector_report.json"
        with open(today_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Daily report saved to: {today_file}")

    def display_daily_dashboard(self, report):
        """Display comprehensive dashboard."""
        print("\n" + "=" * 70)
        print("SECTOR-SPECIFIC MARKET INTELLIGENCE")
        print("=" * 70)

        # Sentiment
        if report.get('sentiment'):
            aggregate = report['sentiment']['aggregate']
            print(f"\n📰 NEWS SENTIMENT (AI)")
            print(f"  Articles: {aggregate['total_articles']}")
            print(f"  Bullish: {aggregate['bullish_pct']:.1f}%")
            print(f"  Bearish: {aggregate['bearish_pct']:.1f}%")
            print(f"  Score: {aggregate['weighted_sentiment_score']:+.1f}/100")

        # Macro
        if report.get('macro'):
            health = report['macro']['health_score']
            print(f"\n📊 MACRO DATA (FRED)")
            print(f"  Health Score: {health['score']:+.1f}/100")
            print(f"  Phase: {health['interpretation']}")

        # Archetype
        archetype = report['archetype']
        print(f"\n🎯 CYCLE ARCHETYPE")
        print(f"  Phase: {archetype['archetype']}")
        print(f"  Combined Score: {archetype['combined_score']:+.1f}/100")
        print(f"    Sentiment: {archetype['sentiment_score']:+.1f}")
        print(f"    Macro: {archetype['macro_score']:+.1f}")
        print(f"  Risk Level: {archetype['risk_level']}")
        print(f"  Strategy: {archetype['strategy']}")

        # Sector recommendations
        if report.get('sector_recommendations'):
            sectors = report['sector_recommendations']
            print(f"\n💼 SECTOR RECOMMENDATIONS")
            for sector, recommendation in sectors.items():
                print(f"  {sector.upper()}: {recommendation}")

        print("\n" + "=" * 70)
        print(f"Report generated at: {report['timestamp']}")
        print(f"Files saved to: {self.today_dir}")
        print("=" * 70)

    def run_daily_analysis(self, sectors=['GOLD', 'TECH'], api_key=None):
        """Run complete daily analysis for specific sectors."""
        print("\n" + "=" * 70)
        print("SECTOR MARKET INTELLIGENCE AGENT")
        print("=" * 70)
        print(f"Sectors: {', '.join(sectors)}")
        print(f"Analysis for: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 1. Crawl news by sector
        self.crawl_news(sector=sectors[0].lower(), max_articles=20)
        self.crawl_news(sector=sectors[1].lower(), max_articles=20)

        # 2. Fetch macro data
        self.fetch_macro_data(api_key=api_key)

        # 3. Analyze sentiment
        self.analyze_sentiment(limit=50)

        # 4. Load data
        sentiment_data = self.load_sentiment()
        macro_data = self.load_macro()

        # 5. Determine archetype
        archetype = self.determine_cycle_archetype(sentiment_data, macro_data)

        # 6. Get sector recommendations
        sector_recommendations = self.get_sector_recommendation(archetype['archetype'])

        # 7. Compile report
        report = {
            'timestamp': datetime.now().isoformat(),
            'sectors': sectors,
            'sentiment': sentiment_data,
            'macro': macro_data,
            'archetype': archetype,
            'sector_recommendations': sector_recommendations
        }

        # 8. Save report
        self.save_daily_report(report)

        # 9. Display dashboard
        self.display_daily_dashboard(report)

        print("\n✅ Daily analysis complete!")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Sector-Specific Market Intelligence Agent')
    parser.add_argument('--api-key', '-k', help='FRED API key (or set FRED_API_KEY env var)')
    parser.add_argument('--sectors', '-s', nargs='+', default=['GOLD', 'TECH'])
    args = parser.parse_args()

    agent = SectorMarketAgent()
    agent.run_daily_analysis(sectors=args.sectors, api_key=args.api_key)


if __name__ == '__main__':
    main()
