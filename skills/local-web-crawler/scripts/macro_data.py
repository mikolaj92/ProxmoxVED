#!/usr/bin/env python3
"""
Macroeconomic data collector and analyzer.
Collects: GDP, Inflation (CPI), Interest Rates, Unemployment, PMI, etc.
"""

import sys
import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


# Data sources
SOURCES = {
    'fed_reserve': {
        'url': 'https://www.federalreserve.gov/newsevents/pressreleases/monetary',
        'name': 'Federal Reserve'
    },
    'trading_economics': {
        'url': 'https://tradingeconomics.com/united-states',
        'name': 'Trading Economics'
    },
    'fred': {
        'url': 'https://fred.stlouisfed.org',
        'name': 'FRED Economic Data'
    },
    'bls': {
        'url': 'https://www.bls.gov',
        'name': 'Bureau of Labor Statistics'
    }
}


MACRO_INDICATORS = {
    'GDP': 'Gross Domestic Product - overall economic health',
    'CPI': 'Consumer Price Index - inflation rate',
    'PPI': 'Producer Price Index - wholesale inflation',
    'Unemployment': 'Jobless rate - labor market health',
    'Fed Funds Rate': 'Federal Reserve interest rate',
    'PMI': 'Purchasing Managers Index - business activity',
    'Consumer Confidence': 'Consumer sentiment',
    'Durable Goods': 'Orders for long-lasting goods',
    'Housing Starts': 'New residential construction',
    'Retail Sales': 'Consumer spending',
    'Trade Balance': 'Imports vs exports'
}


def fetch_page(url, headers=None):
    """Fetch page with retry logic."""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    for attempt in range(3):
        try:
            response = requests.get(url, timeout=15, headers=headers)
            response.raise_for_status()
            return response
        except Exception as e:
            if attempt == 2:
                raise
            print(f"Retry {attempt + 1} for {url}...")
            import time
            time.sleep(2)


def extract_macro_data(soup, indicator):
    """Extract macro indicator value from page."""
    # This is a simplified version - real implementation would need
    # site-specific parsing logic
    return None


def get_fed_funds_rate():
    """Get current Fed Funds Rate from FRED API or scraping."""
    # FRED has a free API but requires a key
    # For now, return a placeholder
    return {
        'indicator': 'Fed Funds Rate',
        'current': None,
        'source': 'FRED',
        'last_updated': datetime.now().isoformat()
    }


def get_cpi_data():
    """Get CPI inflation data."""
    return {
        'indicator': 'CPI',
        'current': None,
        'yoy_change': None,
        'source': 'BLS',
        'last_updated': datetime.now().isoformat()
    }


def get_pmi_data():
    """Get PMI (Purchasing Managers Index)."""
    return {
        'indicator': 'PMI',
        'current': None,
        'interpretation': None,
        'source': 'ISM',
        'last_updated': datetime.now().isoformat()
    }


def get_unemployment_rate():
    """Get unemployment rate."""
    return {
        'indicator': 'Unemployment Rate',
        'current': None,
        'source': 'BLS',
        'last_updated': datetime.now().isoformat()
    }


def get_consumer_confidence():
    """Get consumer confidence index."""
    return {
        'indicator': 'Consumer Confidence',
        'current': None,
        'source': 'Conference Board',
        'last_updated': datetime.now().isoformat()
    }


def interpret_indicator(data):
    """Interpret macro indicator value."""
    interpretations = []

    # PMI interpretation
    if data['indicator'] == 'PMI' and data['current']:
        if data['current'] > 50:
            interpretations.append(f"PMI {data['current']}: Expansion (bullish)")
        elif data['current'] < 50:
            interpretations.append(f"PMI {data['current']}: Contraction (bearish)")
        else:
            interpretations.append(f"PMI {data['current']}: Neutral")

    # Fed Funds Rate interpretation
    elif data['indicator'] == 'Fed Funds Rate' and data['current']:
        if data['current'] > 5:
            interpretations.append(f"High rates ({data['current']}%): Tight monetary policy (bearish)")
        elif data['current'] < 2:
            interpretations.append(f"Low rates ({data['current']}%): Easy monetary policy (bullish)")
        else:
            interpretations.append(f"Neutral rates ({data['current']}%)")

    # Unemployment interpretation
    elif data['indicator'] == 'Unemployment Rate' and data['current']:
        if data['current'] < 4:
            interpretations.append(f"Low unemployment ({data['current']}%): Tight labor market (inflation risk)")
        elif data['current'] > 6:
            interpretations.append(f"High unemployment ({data['current']}%): Economic weakness")
        else:
            interpretations.append(f"Moderate unemployment ({data['current']}%): Balanced labor market")

    # CPI interpretation
    elif data['indicator'] == 'CPI' and data.get('yoy_change'):
        if data['yoy_change'] > 4:
            interpretations.append(f"High inflation ({data['yoy_change']}% YoY): Pressure on economy")
        elif data['yoy_change'] < 1:
            interpretations.append(f"Low inflation ({data['yoy_change']}% YoY): Potential deflation risk")
        else:
            interpretations.append(f"Moderate inflation ({data['yoy_change']}% YoY): Healthy range")

    return interpretations


def collect_all_macro_data():
    """Collect all macro indicators."""
    print("Collecting macroeconomic data...")

    indicators = [
        get_fed_funds_rate(),
        get_cpi_data(),
        get_pmi_data(),
        get_unemployment_rate(),
        get_consumer_confidence()
    ]

    # Add interpretations
    for indicator in indicators:
        indicator['interpretations'] = interpret_indicator(indicator)

    return indicators


def display_macro_summary(indicators):
    """Display macro data summary."""
    print("\n" + "=" * 70)
    print("MACROECONOMIC DASHBOARD")
    print("=" * 70)

    for indicator in indicators:
        print(f"\n{indicator['indicator']}:")
        print(f"  Current: {indicator['current'] or 'Not available'}")
        print(f"  Source: {indicator['source']}")
        print(f"  Updated: {indicator['last_updated']}")

        if indicator.get('interpretations'):
            print(f"  Interpretation:")
            for interp in indicator['interpretations']:
                print(f"    • {interp}")

    print("\n" + "=" * 70)


def calculate_economic_phase(indicators):
    """
    Determine economic phase based on macro indicators.
    Phases: Expansion, Peak, Contraction, Trough
    """
    # This is a simplified analysis
    # Real implementation would use more sophisticated models

    scores = {
        'expansion': 0,
        'contraction': 0
    }

    # PMI
    pmi = next((i for i in indicators if i['indicator'] == 'PMI'), None)
    if pmi and pmi['current']:
        if pmi['current'] > 50:
            scores['expansion'] += 2
        else:
            scores['contraction'] += 2

    # Unemployment
    unemp = next((i for i in indicators if i['indicator'] == 'Unemployment Rate'), None)
    if unemp and unemp['current']:
        if unemp['current'] < 5:
            scores['expansion'] += 1
        else:
            scores['contraction'] += 1

    # Fed Funds Rate
    fed = next((i for i in indicators if i['indicator'] == 'Fed Funds Rate'), None)
    if fed and fed['current']:
        if fed['current'] < 4:
            scores['expansion'] += 1
        else:
            scores['contraction'] += 1

    # Determine phase
    if scores['expansion'] > scores['contraction']:
        return 'Expansion Phase'
    elif scores['contraction'] > scores['expansion']:
        return 'Contraction Phase'
    else:
        return 'Transition/Neutral'


def main():
    """Main execution."""
    indicators = collect_all_macro_data()

    display_macro_summary(indicators)

    phase = calculate_economic_phase(indicators)
    print(f"\n📊 Economic Phase: {phase}")

    print("\n" + "=" * 70)
    print("Note: This is a basic analysis. Real macro data requires")
    print("API access to FRED, BLS, or other data providers.")
    print("=" * 70)


if __name__ == '__main__':
    main()
