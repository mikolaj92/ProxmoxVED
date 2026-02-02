#!/usr/bin/env python3
"""
Automated Market Intelligence Agent
Crawls news, analyzes sentiment, and determines market cycle position.
Runs periodically to track market mood shifts.
"""

import sys
import json
import os
from datetime import datetime, timedelta
from pathlib import Path


class MarketIntelligenceAgent:
    """Automated market intelligence agent."""

    def __init__(self, workspace="/Users/mini-m4-1/clawd"):
        self.workspace = workspace
        self.news_file = None
        self.sentiment_file = None
        self.history_file = workspace + "/.learnings/market_history.json"
        self.today_dir = workspace + f"/.learnings/daily/{datetime.now().strftime('%Y%m%d')}"
        Path(self.today_dir).mkdir(parents=True, exist_ok=True)

    def crawl_news(self, sources=['seeking_alpha'], max_articles=20):
        """Crawl financial news."""
        print("\n" + "=" * 70)
        print("STEP 1: CRAWLING NEWS")
        print("=" * 70)

        cmd = f"cd {self.workspace} && source venv/bin/activate && "
        cmd += f"python3 skills/local-web-crawler/scripts/financial_news_crawler.py "
        cmd += f"--sources {' '.join(sources)} --max {max_articles} --save --summary"

        os.system(cmd)

        # Find latest news file
        news_files = sorted(Path(self.workspace + "/.learnings").glob("news_*.json"))
        if news_files:
            self.news_file = str(news_files[-1])
            print(f"\n✓ News saved to: {self.news_file}")

    def analyze_sentiment(self, limit=50):
        """Analyze sentiment using LM Studio."""
        if not self.news_file:
            print("\n✗ No news file available. Run crawl_news() first.")
            return

        print("\n" + "=" * 70)
        print("STEP 2: ANALYZING SENTIMENT WITH AI")
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

    def determine_cycle_archetype(self, sentiment_data):
        """
        Determine economic cycle archetype based on sentiment + Fear & Greed.
        Returns: archetype, investment_strategy, risk_level
        """
        aggregate = sentiment_data.get('aggregate', {})
        sentiment_score = aggregate.get('weighted_sentiment_score', 0)

        # Archetype mapping
        if sentiment_score > 50:
            archetype = "LATE EXPANSION / PEAK"
            strategy = "REDUCE RISK - Trim positions, increase cash, defensive"
            risk_level = "HIGH (Euphoria)"

        elif sentiment_score > 20:
            archetype = "MID-TO-LATE EXPANSION"
            strategy = "MODERATE - Balanced exposure, watch for excess"
            risk_level = "MEDIUM-HIGH"

        elif sentiment_score > 0:
            archetype = "MID EXPANSION"
            strategy = "HEALTHY - Continue balanced portfolio, quality growth"
            risk_level = "MEDIUM"

        elif sentiment_score > -20:
            archetype = "EARLY EXPANSION / CORRECTION"
            strategy = "OPPORTUNISTIC - Look for quality dips, start accumulating"
            risk_level = "MEDIUM"

        elif sentiment_score > -50:
            archetype = "EARLY RECOVERY / TRÓG"
            strategy = "ACCUMULATE - Buy quality on weakness, contrarian"
            risk_level = "HIGH (but measured)"

        else:
            archetype = "EXTREME FEAR / DEEP TROUGH"
            strategy = "AGGRESSIVE - Maximum pessimism, buy quality aggressively"
            risk_level = "HIGH (opportunity)"

        return {
            'archetype': archetype,
            'strategy': strategy,
            'risk_level': risk_level,
            'sentiment_score': sentiment_score
        }

    def load_history(self):
        """Load historical market intelligence."""
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file) as f:
            return json.load(f)

    def save_daily_report(self, report):
        """Save daily report to history and today's folder."""
        # Append to history
        history = self.load_history()
        history.append(report)

        # Keep only last 90 days
        if len(history) > 90:
            history = history[-90:]

        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)

        # Save to today's folder
        today_file = self.today_dir + "/report.json"
        with open(today_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Daily report saved to: {today_file}")

    def check_for_significant_shift(self, current_score):
        """Check if sentiment has shifted significantly."""
        history = self.load_history()

        if not history:
            return None

        # Get previous 7 days
        recent_scores = [h.get('archetype', {}).get('sentiment_score', 0)
                       for h in history[-7:] if h.get('archetype')]

        if not recent_scores:
            return None

        avg_score = sum(recent_scores) / len(recent_scores)
        shift = current_score - avg_score

        # Significant shift = >30 points
        if abs(shift) > 30:
            direction = "UP" if shift > 0 else "DOWN"
            return {
                'detected': True,
                'shift_amount': shift,
                'direction': direction,
                'previous_avg': avg_score,
                'current': current_score,
                'significance': "MAJOR" if abs(shift) > 50 else "SIGNIFICANT"
            }

        return None

    def generate_alert(self, shift):
        """Generate alert for significant sentiment shift."""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'type': 'SENTIMENT_SHIFT',
            'severity': shift['significance'],
            'direction': shift['direction'],
            'shift_amount': shift['shift_amount'],
            'message': f"""
🚨 MARKET SENTIMENT SHIFT ALERT!

Direction: {shift['direction']}
Shift: {shift['shift_amount']:+.1f} points
Previous 7-day average: {shift['previous_avg']:.1f}
Current: {shift['current']:.1f}
Severity: {shift['significance']}

Action: Review portfolio and risk exposure.
"""
        }

        # Save alert
        alert_file = self.today_dir + "/ALERT.txt"
        with open(alert_file, 'w') as f:
            f.write(alert['message'])

        print(alert['message'])
        return alert

    def display_daily_dashboard(self, report):
        """Display comprehensive daily dashboard."""
        print("\n" + "=" * 70)
        print("MARKET INTELLIGENCE DASHBOARD")
        print("=" * 70)

        # Sentiment
        aggregate = report['sentiment']['aggregate']
        print(f"\n📊 SENTIMENT (AI-Analyzed)")
        print(f"  Articles: {aggregate['total_articles']}")
        print(f"  Bullish: {aggregate['bullish_pct']:.1f}%")
        print(f"  Bearish: {aggregate['bearish_pct']:.1f}%")
        print(f"  Score: {aggregate['weighted_sentiment_score']:+.1f}/100")

        # Archetype
        archetype = report['archetype']
        print(f"\n🎯 CYCLE ARCHETYPE")
        print(f"  Phase: {archetype['archetype']}")
        print(f"  Risk Level: {archetype['risk_level']}")
        print(f"  Strategy: {archetype['strategy']}")

        # Fear & Greed
        print(f"\n😱 FEAR & GREED INDEX")
        fg = report.get('fear_greed', {})
        print(f"  Value: {fg.get('value', 'N/A')}")
        print(f"  Classification: {fg.get('classification', 'N/A')}")

        # Shift Alert
        if report.get('shift_alert'):
            shift = report['shift_alert']
            print(f"\n⚠️  SIGNIFICANT SHIFT DETECTED")
            print(f"  {shift['significance']}: {shift['direction']} ({shift['shift_amount']:+.1f} points)")

        print("\n" + "=" * 70)
        print(f"Report generated at: {report['timestamp']}")
        print(f"Files saved to: {self.today_dir}")
        print("=" * 70)

    def run_daily_analysis(self):
        """Run complete daily analysis."""
        print("\n" + "=" * 70)
        print("AUTOMATED MARKET INTELLIGENCE AGENT")
        print("=" * 70)
        print(f"Analysis for: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 1. Crawl news
        self.crawl_news(sources=['seeking_alpha'], max_articles=20)

        # 2. Analyze sentiment
        self.analyze_sentiment(limit=50)

        # 3. Load sentiment data
        sentiment_data = self.load_sentiment()
        if not sentiment_data:
            print("\n✗ Sentiment analysis failed. Stopping.")
            return

        # 4. Determine cycle archetype
        archetype = self.determine_cycle_archetype(sentiment_data)

        # 5. Check for shifts
        sentiment_score = archetype['sentiment_score']
        shift_alert = self.check_for_significant_shift(sentiment_score)

        # 6. Generate alert if needed
        if shift_alert and shift_alert['detected']:
            self.generate_alert(shift_alert)

        # 7. Compile report
        report = {
            'timestamp': datetime.now().isoformat(),
            'sentiment': sentiment_data,
            'archetype': archetype,
            'shift_alert': shift_alert if shift_alert and shift_alert['detected'] else None
        }

        # 8. Save report
        self.save_daily_report(report)

        # 9. Display dashboard
        self.display_daily_dashboard(report)

        print("\n✅ Daily analysis complete!")


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Automated Market Intelligence Agent')
    parser.add_argument('--workspace', '-w', default='/Users/mini-m4-1/clawd')
    parser.add_argument('--sources', '-s', nargs='+', default=['seeking_alpha'])
    parser.add_argument('--max-articles', '-m', type=int, default=20)
    args = parser.parse_args()

    agent = MarketIntelligenceAgent(workspace=args.workspace)
    agent.crawl_news(sources=args.sources, max_articles=args.max_articles)
    agent.analyze_sentiment(limit=50)

    # Full daily analysis
    agent.run_daily_analysis()


if __name__ == '__main__':
    main()
