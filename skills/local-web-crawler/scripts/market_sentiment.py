#!/usr/bin/env python3
"""
Market sentiment analysis and economic cycle archetypes.
Uses web crawling to gather sentiment data and determine market cycle position.
"""

import sys
import json
from datetime import datetime
from bs4 import BeautifulSoup
from macro_data import fetch_page


# Economic cycle archetypes
CYCLE_PHASES = {
    'early_expansion': {
        'description': 'Emerging from recession, growth picking up',
        'indicators': ['Falling unemployment', 'Rising PMI', 'Low rates', 'Improving sentiment'],
        'investment_strategy': 'Growth stocks, cyclical sectors, emerging markets',
        'risk_level': 'Medium'
    },
    'mid_expansion': {
        'description': 'Steady growth, low volatility, confidence high',
        'indicators': ['Low unemployment', 'Strong PMI', 'Moderate rates', 'High confidence'],
        'investment_strategy': 'Balanced portfolio, quality growth, dividend stocks',
        'risk_level': 'Low'
    },
    'late_expansion': {
        'description': 'Growth slowing, inflation rising, valuations high',
        'indicators': ['Rising inflation', 'Tight labor market', 'Higher rates', 'Overconfidence'],
        'investment_strategy': 'Defensive positioning, reduce risk, quality over growth',
        'risk_level': 'Medium-High'
    },
    'recession': {
        'description': 'Economic contraction, falling demand, rising unemployment',
        'indicators': ['Falling GDP', 'Rising unemployment', 'Deflation risk', 'Low sentiment'],
        'investment_strategy': 'Cash, bonds, defensive sectors, avoid leverage',
        'risk_level': 'High'
    },
    'trough': {
        'description': 'Bottom of cycle, maximum pessimism, bargains emerge',
        'indicators': ['Very low sentiment', 'Cheap valuations', 'Rate cuts expected', 'Capitulation'],
        'investment_strategy': 'Start buying, high-quality distressed assets, contrarian',
        'risk_level': 'High (but opportunity)'
    }
}


SENTIMENT_SOURCES = {
    'fear_greed': 'https://alternative.me/crypto/fear-and-greed-index/',
    'vix': 'https://www.cboe.com/products/vix-index/',
    'put_call_ratio': 'https://www.cboe.com/products/put-call-ratio/',
    'consumer_confidence': 'https://www.conference-board.org/data/consumerconfidence.cfm',
    'investor_intelligence': 'https://www.investorsintelligence.com/'
}


def get_fear_greed_index():
    """
    Get Fear & Greed Index (crypto version has free API).
    For traditional markets, would need to scrape.
    """
    try:
        # Crypto Fear & Greed API (free)
        response = fetch_page('https://api.alternative.me/fng/')
        data = response.json()

        if data and data.get('data'):
            latest = data['data'][0]
            return {
                'value': int(latest['value']),
                'classification': latest['value_classification'],
                'timestamp': latest['timestamp']
            }
    except:
        pass

    return {
        'value': None,
        'classification': 'Not available',
        'timestamp': None
    }


def interpret_fear_greed(value):
    """Interpret Fear & Greed index."""
    if value is None:
        return "No data available"

    if value <= 20:
        return f"Extreme Fear ({value}): Maximum pessimism, potential buying opportunity"
    elif value <= 40:
        return f"Fear ({value}): Negative sentiment, caution needed"
    elif value <= 60:
        return f"Neutral ({value}): Balanced sentiment, no clear direction"
    elif value <= 80:
        return f"Greed ({value}): Positive sentiment, watch for excess"
    else:
        return f"Extreme Greed ({value}): Euphoria, likely near peak, reduce risk"


def get_consumer_sentiment():
    """Get consumer sentiment indicators."""
    # Would need to scrape or use API
    return {
        'confidence': None,
        'trend': 'Not available'
    }


def get_institutional_sentiment():
    """Get institutional investor sentiment."""
    return {
        'bull_bear_spread': None,
        'cash_position': 'Not available'
    }


def get_news_sentiment_ticker(ticker=None):
    """
    Get news sentiment for specific ticker or general market.
    Would need NLP/model to analyze news headlines.
    """
    # This would integrate with news crawler + LM Studio for sentiment analysis
    return {
        'sentiment': 'neutral',
        'confidence': 0.5,
        'source': 'Manual analysis required'
    }


def analyze_sentiment_signals():
    """Gather all sentiment signals."""
    print("Collecting market sentiment data...")

    signals = {
        'fear_greed': get_fear_greed_index(),
        'consumer': get_consumer_sentiment(),
        'institutional': get_institutional_sentiment()
    }

    return signals


def display_sentiment_dashboard(signals):
    """Display sentiment analysis."""
    print("\n" + "=" * 70)
    print("MARKET SENTIMENT DASHBOARD")
    print("=" * 70)

    # Fear & Greed
    fg = signals['fear_greed']
    print(f"\nFear & Greed Index: {fg['value'] or 'N/A'} ({fg['classification']})")
    print(f"Interpretation: {interpret_fear_greed(fg['value'])}")

    # Consumer sentiment
    print(f"\nConsumer Confidence: {signals['consumer']['trend']}")
    print(f"  Source: Conference Board")

    # Institutional sentiment
    print(f"\nInstitutional Sentiment: {signals['institutional']['bull_bear_spread'] or 'N/A'}")
    print(f"  Source: Investors Intelligence")

    print("\n" + "=" * 70)


def determine_cycle_phase_from_sentiment(signals, macro_data):
    """
    Determine where we are in the economic cycle using sentiment + macro.
    This is the "archetype" analysis Patryk wants.
    """
    fg_value = signals['fear_greed']['value']

    if fg_value is None:
        return "Cannot determine - missing sentiment data"

    # Archetype mapping based on Fear & Greed + macro context
    if fg_value <= 20:
        # Extreme fear could be:
        if macro_data == 'Contraction Phase':
            return "TROUGH - Maximum pessimism, look for bargains"
        else:
            return "Correction - Fear-driven sell-off, opportunity"

    elif fg_value <= 40:
        return "EARLY RECOVERY - Fear still present, but improving"

    elif fg_value <= 60:
        # Neutral - depends on macro phase
        if macro_data == 'Expansion Phase':
            return "MID EXPANSION - Healthy growth, balanced sentiment"
        elif macro_data == 'Contraction Phase':
            return "LATE CONTRACTION - Confusion, uncertainty"
        else:
            return "TRANSITION - Phase unclear, watch for catalysts"

    elif fg_value <= 80:
        return "LATE EXPANSION - Confidence high, but watch for excess"

    else:
        return "PEAK EUPHORIA - Extreme greed, likely near cycle top"


def get_investment_recommendation(cycle_phase):
    """Get investment strategy based on cycle phase."""
    # Map cycle phases to investment strategies
    strategies = {
        'TROUGH': {
            'allocation': 'Aggressive - Start building positions',
            'sectors': 'Quality, growth, cyclical, emerging markets',
            'timing': 'Dollar-cost average, buy the fear',
            'risk': 'High (but measured)'
        },
        'EARLY EXPANSION': {
            'allocation': 'Moderately aggressive - Continue building',
            'sectors': 'Technology, industrials, financials',
            'timing': 'Add to positions on dips',
            'risk': 'Medium'
        },
        'MID EXPANSION': {
            'allocation': 'Balanced - Quality growth + dividend',
            'sectors': 'Diversified across sectors',
            'timing': 'Rebalance periodically',
            'risk': 'Medium'
        },
        'LATE EXPANSION': {
            'allocation': 'Defensive - Reduce risk, take profits',
            'sectors': 'Consumer staples, healthcare, utilities',
            'timing': 'Trim positions, build cash',
            'risk': 'Medium-High'
        },
        'PEAK EUPHORIA': {
            'allocation': 'Conservative - Maximize cash, minimal equity',
            'sectors': 'Defensive sectors only',
            'timing': 'Reduce positions significantly',
            'risk': 'High'
        },
        'RECESSION': {
            'allocation': 'Defensive - Bonds, cash, minimal equity',
            'sectors': 'Utilities, consumer staples, healthcare',
            'timing': 'Wait for trough signals',
            'risk': 'High'
        },
        'CORRECTION': {
            'allocation': 'Opportunistic - Watch for entry points',
            'sectors': 'Quality, undervalued',
            'timing': 'Wait for fear to peak',
            'risk': 'Medium'
        }
    }

    # Match phase to strategy (fuzzy matching)
    for key, strategy in strategies.items():
        if key in cycle_phase.upper():
            return strategy

    return {
        'allocation': 'Assess and decide based on individual goals',
        'sectors': 'Diversified',
        'timing': 'Monitor for clear signals',
        'risk': 'Depends on individual circumstances'
    }


def main():
    """Main execution."""
    # Get sentiment data
    signals = analyze_sentiment_signals()

    # Display sentiment
    display_sentiment_dashboard(signals)

    # Get macro phase (simplified - would call macro_data.py)
    macro_phase = 'Transition/Neutral'  # Placeholder

    # Determine cycle archetype
    cycle_phase = determine_cycle_phase_from_sentiment(signals, macro_phase)

    print(f"\n🎯 CYCLE ARCHETYPE: {cycle_phase}")

    # Get investment strategy
    strategy = get_investment_recommendation(cycle_phase)

    print(f"\n📊 INVESTMENT STRATEGY:")
    print(f"  Allocation: {strategy['allocation']}")
    print(f"  Sectors: {strategy['sectors']}")
    print(f"  Timing: {strategy['timing']}")
    print(f"  Risk: {strategy['risk']}")

    print("\n" + "=" * 70)
    print("Note: This analysis combines sentiment data with economic cycle")
    print("theory to identify market archetypes and position portfolios")
    print("accordingly. For long-term investing, focus on cycle position")
    print("rather than timing the market perfectly.")
    print("=" * 70)


if __name__ == '__main__':
    main()
