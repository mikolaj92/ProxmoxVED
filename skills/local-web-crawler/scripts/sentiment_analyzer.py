#!/usr/bin/env python3
"""
AI-powered sentiment analysis using LM Studio.
Analyzes news headlines and text to determine market sentiment.
"""

import sys
import json
import requests
from datetime import datetime


# LM Studio endpoint
LM_STUDIO_URL = "http://localhost:1234/v1"
LM_STUDIO_MODEL = "qwen/qwen3-4b-2507"


def get_lm_studio_completion(prompt, temperature=0.3, max_tokens=200):
    """
    Get completion from LM Studio.
    Returns sentiment classification: bullish/bearish/neutral with confidence.
    """
    try:
        response = requests.post(
            f"{LM_STUDIO_URL}/chat/completions",
            json={
                "model": LM_STUDIO_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a financial sentiment analyst. Analyze the given text and classify it as:
- BULLISH: Positive for markets/stocks
- BEARISH: Negative for markets/stocks
- NEUTRAL: No clear bias or balanced

Respond in this JSON format:
{
  "sentiment": "BULLISH|BEARISH|NEUTRAL",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation"
}

Be concise and accurate."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            },
            timeout=30
        )

        response.raise_for_status()
        result = response.json()

        # Parse the completion
        content = result['choices'][0]['message']['content']

        # Try to extract JSON
        try:
            # Look for JSON in the response
            start = content.find('{')
            end = content.rfind('}') + 1
            json_str = content[start:end]
            return json.loads(json_str)
        except:
            # Fallback to simple keyword analysis
            content_lower = content.lower()
            if 'bullish' in content_lower or 'positive' in content_lower:
                return {'sentiment': 'BULLISH', 'confidence': 0.6, 'reasoning': content}
            elif 'bearish' in content_lower or 'negative' in content_lower:
                return {'sentiment': 'BEARISH', 'confidence': 0.6, 'reasoning': content}
            else:
                return {'sentiment': 'NEUTRAL', 'confidence': 0.5, 'reasoning': content}

    except Exception as e:
        print(f"Error getting LM Studio completion: {e}", file=sys.stderr)
        return None


def analyze_headline_sentiment(headline):
    """Analyze sentiment of a single headline."""
    prompt = f"Analyze the market sentiment of this news headline:\n\n\"{headline}\"\n\nIs this bullish, bearish, or neutral for the stock market?"

    return get_lm_studio_completion(prompt)


def analyze_articles_sentiment(articles, limit=50):
    """
    Analyze sentiment of multiple articles.
    Returns aggregated sentiment statistics.
    """
    print("\nAnalyzing sentiment with LM Studio...")

    results = []

    for i, article in enumerate(articles[:limit], 1):
        if i % 5 == 0:
            print(f"  Analyzed {i}/{min(limit, len(articles))} articles...")

        # Combine title and summary for analysis
        text = f"{article['title']}. {article.get('summary', '')}"

        analysis = analyze_headline_sentiment(text)

        if analysis:
            article['sentiment'] = analysis['sentiment']
            article['sentiment_confidence'] = analysis['confidence']
            article['sentiment_reasoning'] = analysis.get('reasoning', '')
            results.append(article)
        else:
            article['sentiment'] = 'NEUTRAL'
            article['sentiment_confidence'] = 0.0
            results.append(article)

    print(f"  ✓ Analyzed {len(results)} articles")
    return results


def calculate_aggregate_sentiment(articles):
    """Calculate aggregate sentiment statistics."""
    if not articles:
        return None

    # Count sentiments
    bullish = len([a for a in articles if a['sentiment'] == 'BULLISH'])
    bearish = len([a for a in articles if a['sentiment'] == 'BEARISH'])
    neutral = len([a for a in articles if a['sentiment'] == 'NEUTRAL'])
    total = len(articles)

    # Calculate weighted sentiment score
    # BULLISH = +1, NEUTRAL = 0, BEARISH = -1
    # Weight by confidence
    sentiment_scores = []

    for article in articles:
        sentiment_val = 0
        if article['sentiment'] == 'BULLISH':
            sentiment_val = 1
        elif article['sentiment'] == 'BEARISH':
            sentiment_val = -1

        # Weight by confidence
        weighted_score = sentiment_val * article.get('sentiment_confidence', 0.5)
        sentiment_scores.append(weighted_score)

    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0

    # Normalize to -100 to +100
    normalized_score = avg_sentiment * 100

    return {
        'total_articles': total,
        'bullish': bullish,
        'bearish': bearish,
        'neutral': neutral,
        'bullish_pct': (bullish / total * 100) if total > 0 else 0,
        'bearish_pct': (bearish / total * 100) if total > 0 else 0,
        'neutral_pct': (neutral / total * 100) if total > 0 else 0,
        'weighted_sentiment_score': normalized_score,
        'timestamp': datetime.now().isoformat()
    }


def interpret_sentiment_score(score):
    """Interpret sentiment score and return archetypal phase."""
    if score > 50:
        return "EXTREME EUPHORIA - Market likely near peak, reduce risk"
    elif score > 20:
        return "GREED - High optimism, watch for excess valuations"
    elif score > 0:
        return "POSITIVE - Healthy optimism, continue moderate exposure"
    elif score > -20:
        return "NEUTRAL - Balanced sentiment, watch for catalysts"
    elif score > -50:
        return "FEAR - Negative sentiment, opportunity emerging"
    else:
        return "EXTREME FEAR - Maximum pessimism, consider buying quality"


def display_sentiment_dashboard(aggregate):
    """Display sentiment analysis dashboard."""
    print("\n" + "=" * 70)
    print("AI-POWERED SENTIMENT ANALYSIS")
    print("=" * 70)

    print(f"\nAnalysis based on: {aggregate['total_articles']} news articles")
    print(f"Analyzed at: {aggregate['timestamp']}")

    print(f"\n📊 Sentiment Breakdown:")
    print(f"  🟢 Bullish: {aggregate['bullish_pct']:.1f}% ({aggregate['bullish']} articles)")
    print(f"  🔴 Bearish: {aggregate['bearish_pct']:.1f}% ({aggregate['bearish']} articles)")
    print(f"  ⚪ Neutral: {aggregate['neutral_pct']:.1f}% ({aggregate['neutral']} articles)")

    print(f"\n📈 Weighted Sentiment Score: {aggregate['weighted_sentiment_score']:+.1f}/100")

    # Interpretation
    interpretation = interpret_sentiment_score(aggregate['weighted_sentiment_score'])
    print(f"\n🎯 Market Archetype: {interpretation}")

    # Investment implication
    if aggregate['weighted_sentiment_score'] > 30:
        implication = "Reduce equity exposure, increase cash, look defensive"
    elif aggregate['weighted_sentiment_score'] > 0:
        implication = "Maintain balanced portfolio, monitor for excess"
    elif aggregate['weighted_sentiment_score'] > -30:
        implication = "Look for quality opportunities, start accumulating"
    else:
        implication = "Aggressive accumulation possible, focus on quality"

    print(f"\n💡 Investment Implication: {implication}")

    print("\n" + "=" * 70)


def save_sentiment_results(articles, aggregate, filepath=None):
    """Save sentiment analysis results."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        'aggregate': aggregate,
        'articles': articles,
        'saved_at': datetime.now().isoformat()
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nSentiment results saved to: {filepath}")
    return filepath


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='AI-powered sentiment analysis')
    parser.add_argument('--news-file', '-f', help='Load news from JSON file')
    parser.add_argument('--limit', '-l', type=int, default=50, help='Max articles to analyze')
    parser.add_argument('--save', action='store_true', help='Save results to file')
    args = parser.parse_args()

    # Load articles
    if args.news_file:
        print(f"Loading articles from {args.news_file}...")
        with open(args.news_file) as f:
            articles = json.load(f)
    else:
        print("No news file provided. Run financial_news_crawler.py first.")
        return

    # Analyze sentiment
    analyzed_articles = analyze_articles_sentiment(articles, args.limit)

    # Calculate aggregate sentiment
    aggregate = calculate_aggregate_sentiment(analyzed_articles)

    # Display dashboard
    display_sentiment_dashboard(aggregate)

    # Save results
    if args.save:
        save_sentiment_results(analyzed_articles, aggregate)

    print(f"\n✅ Sentiment analysis complete!")


if __name__ == '__main__':
    main()
