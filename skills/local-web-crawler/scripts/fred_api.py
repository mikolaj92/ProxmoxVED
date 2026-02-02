#!/usr/bin/env python3
"""
FRED API Integration - Free macroeconomic data.
Series: GDP, CPI, Unemployment, Fed Funds Rate, PMI
"""

import sys
import json
from datetime import datetime, timedelta
import requests


# FRED API configuration
FRED_API_URL = "https://api.stlouisfed.org/fred/"
FRED_API_KEY = None  # Set this or use env var FRED_API_KEY


# Key economic series IDs
SERIES_IDS = {
    'GDP': {
        'id': 'GDP',
        'name': 'Gross Domestic Product',
        'frequency': 'Quarterly',
        'units': 'Billions of Dollars',
        'description': 'Seasonally Adjusted Annual Rate'
    },
    'CPI': {
        'id': 'CPIAUCSL',
        'name': 'Consumer Price Index (All Items)',
        'frequency': 'Monthly',
        'units': 'Index 1982-1984=100',
        'description': 'Seasonally Adjusted'
    },
    'PPI': {
        'id': 'WPSFD49207',
        'name': 'Producer Price Index',
        'frequency': 'Monthly',
        'units': 'Index 2017=100',
        'description': 'Final Demand'
    },
    'Unemployment': {
        'id': 'UNRATE',
        'name': 'Unemployment Rate',
        'frequency': 'Monthly',
        'units': 'Percent',
        'description': 'Seasonally Adjusted'
    },
    'Fed_Funds_Rate': {
        'id': 'FEDFUNDS',
        'name': 'Federal Funds Rate',
        'frequency': 'Monthly',
        'units': 'Percent',
        'description': 'Effective Federal Funds Rate'
    },
    'PMI_Manufacturing': {
        'id': 'NAPM',
        'name': 'PMI Manufacturing',
        'frequency': 'Monthly',
        'units': 'Index',
        'description': 'ISM Manufacturing PMI'
    },
    'PMI_Services': {
        'id': 'NAPMPI',
        'name': 'PMI Services',
        'frequency': 'Monthly',
        'units': 'Index',
        'description': 'ISM Services PMI'
    },
    'Housing_Starts': {
        'id': 'HOUST',
        'name': 'Housing Starts',
        'frequency': 'Monthly',
        'units': 'Thousands of Units',
        'description': 'Seasonally Adjusted Annual Rate'
    },
    'Retail_Sales': {
        'id': 'RSXFS',
        'name': 'Advance Retail Sales',
        'frequency': 'Monthly',
        'units': 'Millions of Dollars',
        'description': 'Seasonally Adjusted'
    },
    'Consumer_Confidence': {
        'id': 'UMCSENT',
        'name': 'Consumer Sentiment',
        'frequency': 'Monthly',
        'units': 'Index',
        'description': 'University of Michigan'
    }
}


def get_api_key():
    """Get FRED API key from env or hardcoded."""
    import os
    return os.environ.get('FRED_API_KEY') or FRED_API_KEY


def fetch_fred_series(series_id, observation_start=None, observation_end=None):
    """Fetch economic series data from FRED."""
    api_key = get_api_key()

    if not api_key:
        raise ValueError("FRED_API_KEY not set. Set env var FRED_API_KEY or get free key from https://fred.stlouisfed.org/docs/api/api_key.html")

    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': observation_start or (datetime.now() - timedelta(days=365*5)).strftime('%Y-%m-%d'),
        'observation_end': observation_end or datetime.now().strftime('%Y-%m-%d')
    }

    response = requests.get(FRED_API_URL + 'series/observations', params=params)
    response.raise_for_status()
    return response.json()


def interpret_indicator(data, series_info):
    """Interpret economic indicator value."""
    series_name = series_info['name']
    latest_value = None

    if data.get('observations') and len(data['observations']) > 0:
        latest_value = float(data['observations'][-1]['value'])

    if series_name == 'Unemployment Rate':
        if latest_value < 4:
            return f"Low unemployment ({latest_value:.1f}%): Tight labor market"
        elif latest_value > 6:
            return f"High unemployment ({latest_value:.1f}%): Economic weakness"
        else:
            return f"Moderate unemployment ({latest_value:.1f}%): Balanced labor market"

    elif 'Fed Funds Rate' in series_name:
        if latest_value > 5:
            return f"High rates ({latest_value:.2f}%): Tight monetary policy"
        elif latest_value < 2:
            return f"Low rates ({latest_value:.2f}%): Easy monetary policy"
        else:
            return f"Neutral rates ({latest_value:.2f}%): Normal monetary stance"

    elif 'PMI' in series_name:
        if latest_value > 50:
            return f"PMI {latest_value:.1f}: Expansion (bullish)"
        elif latest_value < 50:
            return f"PMI {latest_value:.1f}: Contraction (bearish)"
        else:
            return f"PMI {latest_value:.1f}: Neutral"

    elif 'GDP' in series_name:
        growth_rate = None
        if len(data['observations']) >= 2:
            prev_value = float(data['observations'][-2]['value'])
            growth_rate = ((latest_value - prev_value) / prev_value) * 100

        if growth_rate:
            if growth_rate > 3:
                return f"Strong GDP growth ({growth_rate:+.1f}%): Economic boom"
            elif growth_rate < 0:
                return f"GDP contraction ({growth_rate:+.1f}%): Recession"
            else:
                return f"Moderate GDP growth ({growth_rate:+.1f}%): Stable growth"
        else:
            return f"GDP: {latest_value:.1f}B (insufficient data)"

    else:
        return f"{series_name}: {latest_value or 'N/A'}"


def get_all_macro_data():
    """Fetch all key macro indicators."""
    print("\n" + "=" * 70)
    print("FETCHING MACRO DATA FROM FRED")
    print("=" * 70)

    indicators = {}

    for series_key, series_info in SERIES_IDS.items():
        try:
            print(f"\nFetching {series_info['name']}...")

            data = fetch_fred_series(series_info['id'])

            # Extract latest value
            if data.get('observations'):
                latest = data['observations'][-1]
                indicators[series_key] = {
                    'series_id': series_info['id'],
                    'name': series_info['name'],
                    'value': float(latest['value']),
                    'date': latest['date'],
                    'units': series_info['units'],
                    'interpretation': interpret_indicator(data, series_info)
                }
                print(f"  ✓ {latest['date']}: {latest['value']} ({series_info['units']})")

        except ValueError as e:
            print(f"  ✗ {e}")
            return None
        except Exception as e:
            print(f"  ✗ Error fetching {series_key}: {e}")
            continue

    return indicators


def calculate_economic_health_score(indicators):
    """
    Calculate overall economic health score (-100 to +100).
    Based on multiple macro indicators.
    """
    if not indicators:
        return None

    score = 0
    factors = []

    # PMI (major factor)
    pmi_man = indicators.get('PMI_Manufacturing')
    pmi_svc = indicators.get('PMI_Services')

    if pmi_man:
        pmi_score = (pmi_man['value'] - 50) * 3  # -150 to +150
        score += pmi_score / 3
        factors.append(f"PMI Manufacturing: {pmi_man['interpretation']}")

    if pmi_svc:
        pmi_score = (pmi_svc['value'] - 50) * 2  # -100 to +100
        score += pmi_score / 3
        factors.append(f"PMI Services: {pmi_svc['interpretation']}")

    # Unemployment (inverted - lower is better)
    unemp = indicators.get('Unemployment')
    if unemp:
        # Ideal: 4-5%, below 4 is overheating, above 6 is weakness
        if unemp['value'] < 4:
            unemp_score = -10  # Overheating risk
        elif unemp['value'] > 6:
            unemp_score = -20  # Weakness
        else:
            unemp_score = 10  # Healthy
        score += unemp_score / 2
        factors.append(f"Unemployment: {unemp['interpretation']}")

    # Fed Funds Rate (lower is stimulative)
    fed = indicators.get('Fed_Funds_Rate')
    if fed:
        if fed['value'] > 5:
            rate_score = -15  # Tight
        elif fed['value'] < 2:
            rate_score = 10  # Stimulative
        else:
            rate_score = 0  # Neutral
        score += rate_score / 2
        factors.append(f"Fed Rate: {fed['interpretation']}")

    # Consumer Confidence
    conf = indicators.get('Consumer_Confidence')
    if conf:
        conf_score = (conf['value'] - 100) / 5  # -20 to +20
        score += conf_score / 5
        factors.append(f"Consumer Confidence: {conf['interpretation']}")

    # Normalize to -100 to +100
    normalized_score = max(-100, min(100, score))

    return {
        'score': normalized_score,
        'interpretation': interpret_health_score(normalized_score),
        'factors': factors
    }


def interpret_health_score(score):
    """Interpret economic health score."""
    if score > 50:
        return "STRONG EXPANSION - Boom conditions, watch for overheating"
    elif score > 20:
        return "MODERATE EXPANSION - Healthy growth, good environment"
    elif score > 0:
        return "SLOW EXPANSION - Growth but below potential"
    elif score > -20:
        return "TRANSITION - Economy slowing, possible recession"
    elif score > -50:
        return "MILD RECESSION - Economic weakness"
    else:
        return "DEEP RECESSION - Severe contraction"


def display_macro_dashboard(indicators, health_score):
    """Display comprehensive macro dashboard."""
    print("\n" + "=" * 70)
    print("MACROECONOMIC DASHBOARD (FRED API)")
    print("=" * 70)

    # Health score
    print(f"\n📊 Economic Health Score: {health_score['score']:+.1f}/100")
    print(f"🎯 Phase: {health_score['interpretation']}")

    print(f"\nKey Indicators:")
    for series_key, data in indicators.items():
        print(f"\n  {data['name']}:")
        print(f"    Value: {data['value']:.2f} {data['units']}")
        print(f"    Date: {data['date']}")
        print(f"    {data['interpretation']}")

    # Factors
    print(f"\n📈 Health Score Factors:")
    for factor in health_score['factors']:
        print(f"  • {factor}")

    print("\n" + "=" * 70)


def save_macro_data(indicators, health_score, filepath=None):
    """Save macro data to JSON file."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    data = {
        'timestamp': datetime.now().isoformat(),
        'indicators': indicators,
        'health_score': health_score
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n📁 Macro data saved to: {filepath}")
    return filepath


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='FRED API Macro Data')
    parser.add_argument('--api-key', '-k', help='FRED API key (or set FRED_API_KEY env var)')
    parser.add_argument('--save', action='store_true', help='Save to file')
    args = parser.parse_args()

    if args.api_key:
        import os
        os.environ['FRED_API_KEY'] = args.api_key

    # Fetch all macro data
    indicators = get_all_macro_data()

    if not indicators:
        print("\n✗ Failed to fetch macro data. Check API key.")
        return

    # Calculate health score
    health_score = calculate_economic_health_score(indicators)

    # Display dashboard
    display_macro_dashboard(indicators, health_score)

    # Save
    if args.save:
        save_macro_data(indicators, health_score)

    print(f"\n✅ Macro data analysis complete!")


if __name__ == '__main__':
    main()
