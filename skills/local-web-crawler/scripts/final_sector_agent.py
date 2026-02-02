#!/usr/bin/env python3
"""
Final Sector Market Intelligence Agent
Combines: RSS News + FRED API + LM Studio Sentiment
Sector focus: GOLD + TECH
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path


class FinalSectorAgent:
    """Complete market intelligence agent."""

    def __init__(self, workspace="/Users/mini-m4-1/clawd"):
        self.workspace = workspace
        self.news_file = None
        self.sentiment_file = None
        self.macro_file = None
        self.today_dir = workspace + f"/.learnings/daily/{datetime.now().strftime('%Y%m%d')}"
        Path(self.today_dir).mkdir(parents=True, exist_ok=True)

    def run(self, sectors=['GOLD', 'TECH'], api_key=None):
        """Run complete daily analysis."""
        print("\n" + "=" * 70)
        print("FINAL SECTOR MARKET INTELLIGENCE AGENT")
        print("=" * 70)
        print(f"Sectors: {', '.join(sectors)}")
        print(f"Analysis for: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # STEP 1: Crawl news via RSS
        print("\n[1/4] CRAWLING NEWS (RSS)")
        self.crawl_news_rss(sectors)

        # STEP 2: Fetch macro data (FRED API or mock)
        print("\n[2/4] FETCHING MACRO DATA")
        self.fetch_macro_data(api_key)

        # STEP 3: Analyze sentiment with LM Studio
        print("\n[3/4] ANALYZING SENTIMENT (AI)")
        self.analyze_sentiment(limit=50)

        # STEP 4: Compile comprehensive report
        print("\n[4/4] COMPILING REPORT")
        self.compile_report(sectors)

        print("\n✅ Analysis complete!")

    def crawl_news_rss(self, sectors):
        """Crawl news via RSS feeds."""
        print("\n" + "-" * 70)
        print("CRAWLING NEWS VIA RSS FEEDS")
        print("-" * 70)

        # RSS sources for GOLD + TECH
        rss_sources = [
            ('yahoo_finance_gold', 'https://finance.yahoo.com/rss/u/gold', 'Yahoo Finance Gold'),
            ('yahoo_finance_tech', 'https://finance.yahoo.com/rss/u/technology', 'Yahoo Finance Tech'),
            ('cnbc', 'https://www.cnbc.com/id/10000664/device/rss/rss.html', 'CNBC Markets')
        ]

        all_articles = []

        for feed_id, feed_url, feed_name in rss_sources:
            print(f"\nFetching: {feed_name}...")
            cmd = f"cd {self.workspace} && source venv/bin/activate && "
            cmd += f"python3 skills/local-web-crawler/scripts/rss_news_crawler.py "
            cmd += f"--sources {feed_id} --max 10 --sector {sectors[0].lower()}"

            result = os.system(cmd)

            # Load latest RSS news
            rss_files = sorted(Path(self.workspace + "/.learnings").glob("rss_news_*.json"))
            if rss_files:
                with open(rss_files[-1]) as f:
                    articles = json.load(f)
                    all_articles.extend(articles)

        # Save all news
        if all_articles:
            news_file = f"{self.today_dir}/news.json"
            with open(news_file, 'w') as f:
                json.dump(all_articles, f, indent=2)

            print(f"\n✓ Saved {len(all_articles)} articles")
            self.news_file = news_file

    def fetch_macro_data(self, api_key):
        """Fetch macro data from FRED or use mock."""
        print("\n" + "-" * 70)
        print("FETCHING MACRO DATA")
        print("-" * 70)

        if api_key:
            print("Using FRED API...")
            cmd = f"cd {self.workspace} && source venv/bin/activate && "
            cmd += f"FRED_API_KEY={api_key} python3 skills/local-web-crawler/scripts/fred_api.py --save"

            os.system(cmd)

            # Find latest macro
            macro_files = sorted(Path(self.workspace + "/.learnings").glob("macro_*.json"))
            if macro_files:
                with open(macro_files[-1]) as f:
                    self.macro_data = json.load(f)
                print(f"✓ FRED data loaded")
                return
        else:
            print("Using MOCK macro data (FRED API key not provided)")

        # Use mock data
        self.macro_data = {
            'timestamp': datetime.now().isoformat(),
            'indicators': {
                'GDP': {
                    'value': 28372.5,
                    'date': '2024-12-01',
                    'interpretation': 'Moderate GDP growth (+2.1% YoY): Stable growth'
                },
                'CPI': {
                    'value': 314.14,
                    'date': '2024-12-01',
                    'interpretation': 'Moderate inflation (2.9% YoY): Healthy range'
                },
                'Unemployment': {
                    'value': 4.1,
                    'date': '2024-12-01',
                    'interpretation': 'Low unemployment (4.1%): Tight labor market'
                },
                'Fed_Funds_Rate': {
                    'value': 4.33,
                    'date': '2024-12-01',
                    'interpretation': 'Neutral rates (4.33%): Normal monetary stance'
                },
                'PMI_Manufacturing': {
                    'value': 48.5,
                    'date': '2024-12-01',
                    'interpretation': 'PMI 48.5: Contraction (bearish)'
                },
                'PMI_Services': {
                    'value': 52.3,
                    'date': '2024-12-01',
                    'interpretation': 'PMI 52.3: Expansion (bullish)'
                }
            },
            'health_score': {
                'score': 8.3,
                'interpretation': 'SLOW EXPANSION - Growth but below potential'
            }
        }

        macro_file = f"{self.today_dir}/macro.json"
        with open(macro_file, 'w') as f:
            json.dump(self.macro_data, f, indent=2)

        print(f"✓ Mock macro data loaded")

    def analyze_sentiment(self, limit=50):
        """Analyze sentiment with LM Studio."""
        print("\n" + "-" * 70)
        print("ANALYZING SENTIMENT WITH AI (LM Studio)")
        print("-" * 70)

        if not self.news_file:
            print("✗ No news file available")
            return

        cmd = f"cd {self.workspace} && source venv/bin/activate && "
        cmd += f"python3 skills/local-web-crawler/scripts/sentiment_analyzer.py "
        cmd += f"--news-file {self.news_file} --limit {limit} --save"

        os.system(cmd)

        # Load sentiment
        sentiment_files = sorted(Path(self.workspace + "/.learnings").glob("sentiment_*.json"))
        if sentiment_files:
            with open(sentiment_files[-1]) as f:
                self.sentiment_data = json.load(f)
            print(f"✓ Sentiment analysis loaded")
        else:
            self.sentiment_data = {'aggregate': {}}

    def compile_report(self, sectors):
        """Compile and display final report."""
        print("\n" + "=" * 70)
        print("FINAL MARKET INTELLIGENCE REPORT")
        print("=" * 70)

        # Sentiment
        aggregate = self.sentiment_data.get('aggregate', {})
        print(f"\n📰 NEWS SENTIMENT (AI)")
        print(f"  Articles: {aggregate.get('total_articles', 'N/A')}")
        print(f"  Bullish: {aggregate.get('bullish_pct', 0):.1f}%")
        print(f"  Bearish: {aggregate.get('bearish_pct', 0):.1f}%")
        print(f"  Score: {aggregate.get('weighted_sentiment_score', 0):+.1f}/100")

        # Macro
        health = self.macro_data.get('health_score', {})
        print(f"\n📊 MACRO DATA")
        print(f"  Health Score: {health.get('score', 0):+.1f}/100")
        print(f"  Phase: {health.get('interpretation', 'N/A')}")

        # Indicators
        print(f"\n📈 KEY MACRO INDICATORS:")
        indicators = self.macro_data.get('indicators', {})
        for key in ['GDP', 'CPI', 'Unemployment', 'Fed_Funds_Rate', 'PMI_Manufacturing', 'PMI_Services']:
            if key in indicators:
                ind = indicators[key]
                print(f"  {ind.get('name', key)}: {ind.get('value', 'N/A')} ({ind.get('interpretation', '')[:50]}...)")

        # Combined score
        sentiment_score = aggregate.get('weighted_sentiment_score', 0)
        macro_score = health.get('score', 0)
        combined = (sentiment_score * 0.6) + (macro_score * 0.4)

        print(f"\n🎯 CYCLE ARCHETYPE")
        print(f"  Sentiment: {sentiment_score:+.1f}")
        print(f"  Macro: {macro_score:+.1f}")
        print(f"  Combined Score: {combined:+.1f}/100")

        # Determine phase
        if combined > 40:
            phase = "LATE EXPANSION / PEAK"
            strategy = "REDUCE RISK - Trim positions, increase cash"
            risk = "HIGH (Euphoria)"
            gold_rec = "Reduce - Safe haven not needed"
            tech_rec = "Reduce - Valuations stretched, lock in profits"
        elif combined > 20:
            phase = "MID-TO-LATE EXPANSION"
            strategy = "MODERATE - Balanced, rotate to defensives"
            risk = "MEDIUM-HIGH"
            gold_rec = "Small - Inflation hedge"
            tech_rec = "Moderate - Focus on quality"
        elif combined > 0:
            phase = "MID EXPANSION"
            strategy = "HEALTHY - Continue balanced portfolio"
            risk = "MEDIUM"
            gold_rec = "Small - Modest inflation"
            tech_rec = "Increase - Growth favorable"
        elif combined > -20:
            phase = "EARLY EXPANSION / CORRECTION"
            strategy = "OPPORTUNISTIC - Buy on dips, start accumulating"
            risk = "MEDIUM"
            gold_rec = "Moderate - Safe haven demand"
            tech_rec = "Hold - Wait for signals"
        elif combined > -40:
            phase = "EARLY RECOVERY / TROUGH"
            strategy = "ACCUMULATE - Buy quality on weakness"
            risk = "HIGH (but measured)"
            gold_rec = "Significant - Safe haven demand high"
            tech_rec = "Selectively - Quality tech on weakness"
        else:
            phase = "DEEP RECESSION / EXTREME FEAR"
            strategy = "AGGRESSIVE - Maximum pessimism, buy quality"
            risk = "HIGH (opportunity)"
            gold_rec = "Maximum - Ultimate safe haven"
            tech_rec = "Aggressive - Maximum pessimism, buy quality"

        print(f"  Phase: {phase}")
        print(f"  Risk: {risk}")
        print(f"  Strategy: {strategy}")

        # Sector recommendations
        print(f"\n💼 SECTOR RECOMMENDATIONS:")
        print(f"  GOLD: {gold_rec}")
        print(f"  TECH: {tech_rec}")

        # Save report
        report_file = f"{self.today_dir}/final_report.json"
        report = {
            'timestamp': datetime.now().isoformat(),
            'sectors': sectors,
            'sentiment': aggregate,
            'macro': self.macro_data,
            'cycle': {
                'phase': phase,
                'strategy': strategy,
                'risk': risk,
                'combined_score': combined
            },
            'sectors_recommendations': {
                'GOLD': gold_rec,
                'TECH': tech_rec
            }
        }

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n📁 Report saved to: {report_file}")

        print("\n" + "=" * 70)


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Final Sector Market Intelligence Agent')
    parser.add_argument('--api-key', '-k', help='FRED API key (or set FRED_API_KEY env var)')
    parser.add_argument('--sectors', '-s', nargs='+', default=['GOLD', 'TECH'])
    args = parser.parse_args()

    agent = FinalSectorAgent()
    agent.run(sectors=args.sectors, api_key=args.api_key)


if __name__ == '__main__':
    main()
