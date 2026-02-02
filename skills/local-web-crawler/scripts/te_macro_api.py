#!/usr/bin/env python3
"""
TradingEconomics API Integration
Free alternative to FRED API
Provides real-time macroeconomic data without API key
"""

import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path


# TradingEconomics API (free, no key needed)
TRADING_ECONOMICS_BASE = "https://api.tradingeconomics.com"
TE_API_KEY = "guest:guest"  # Free guest account


# Key macro indicators
INDICATORS = {
    'GDP': {
        'code': 'USGDPYOY',
        'name': 'US GDP YoY',
        'country': 'united states'
    },
    'CPI': {
        'code': 'USCPIYOY',
        'name': 'US CPI YoY',
        'country': 'united states'
    },
    'Unemployment': {
        'code': 'USUNR',
        'name': 'US Unemployment Rate',
        'country': 'united states'
    },
    'Fed_Funds_Rate': {
        'code': 'FDFR',
        'name': 'Fed Funds Rate',
        'country': 'united states'
    },
    'PMI_Manufacturing': {
        'code': 'USPMI',
        'name': 'US Manufacturing PMI',
        'country': 'united states'
    },
    'PMI_Services': {
        'code': 'USNOPMI',
        'name': 'US Non-Manufacturing PMI',
        'country': 'united states'
    },
    'Housing_Starts': {
        'code': 'USHOUST',
        'name': 'US Housing Starts',
        'country': 'united states'
    },
    'Retail_Sales': {
        'code': 'USRSL',
        'name': 'US Retail Sales',
        'country': 'united states'
    },
    'Consumer_Confidence': {
        'code': 'USCCCI',
        'name': 'US Consumer Confidence',
        'country': 'united states'
    }
}


def fetch_indicator(indicator_code, country='united states'):
    """Fetch indicator from TradingEconomics."""
    url = f"{TRADING_ECONOMICS_BASE}/indicator"
    
    params = {
        'c': country,
        'i': indicator_code
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and len(data['data']) > 0:
            latest = data['data'][0]
            return {
                'code': indicator_code,
                'value': latest.get('Value'),
                'date': latest.get('DateTime'),
                'source': 'TradingEconomics'
            }
        else:
            return None
            
    except Exception as e:
        print(f"  ✗ Error fetching {indicator_code}: {e}")
        return None


def interpret_indicator(data, indicator_info):
    """Interpret economic indicator value."""
    if not data:
        return "No data available"
    
    indicator_name = indicator_info['name']
    value = data['value']
    
    if indicator_name == 'US Unemployment Rate':
        if value < 4:
            return f"Niskie bezrobocie ({value:.1f}%): Mocny rynek pracy (ryzyko inflacji)"
        elif value > 6:
            return f"Wysokie bezrobocie ({value:.1f}%): Słabość gospodarka"
        else:
            return f"Umiarkowane bezrobocie ({value:.1f}%): Zbalansowany rynek pracy"
    
    elif 'Funds Rate' in indicator_name:
        if value > 5:
            return f"Wysokie stopy ({value:.2f}%): Ściśła polityka monetarna"
        elif value < 2:
            return f"Niskie stopy ({value:.2f}%): Luźna polityka monetarna"
        else:
            return f"Neutralne stopy ({value:.2f}%): Normalna polityka"
    
    elif 'PMI' in indicator_name:
        if value > 50:
            return f"PMI {value:.1f}: Ekspansja (bullish)"
        elif value < 50:
            return f"PMI {value:.1f}: Kontrakcja (bearish)"
        else:
            return f"PMI {value:.1f}: Neutral"
    
    elif 'GDP' in indicator_name or 'CPI' in indicator_name:
        if 'YoY' in indicator_name:
            if value > 3:
                return f"Mocny wzrost ({value:+.1f}% YoY): Boom gospodarczy"
            elif value < 0:
                return f"Kontrakcja ({value:+.1f}% YoY): Recesja"
            else:
                return f"Umiarkowany wzrost ({value:+.1f}% YoY): Stabilna gospodarka"
        else:
            return f"Wartość: {value:.2f}"
    
    else:
        return f"Wartość: {value:.2f}"


def calculate_economic_health_score(indicators):
    """Calculate economic health score (-100 to +100)."""
    score = 0
    factors = []
    
    # PMI (major factor)
    pmi_man = indicators.get('PMI_Manufacturing')
    pmi_svc = indicators.get('PMI_Services')
    
    if pmi_man:
        pmi_score = (pmi_man['value'] - 50) * 3  # -150 do +150
        score += pmi_score / 3
        factors.append(f"PMI Produkcja: {interpret_indicator(pmi_man, INDICATORS['PMI_Manufacturing'])}")
    
    if pmi_svc:
        pmi_score = (pmi_svc['value'] - 50) * 2  # -100 do +100
        score += pmi_score / 3
        factors.append(f"PMI Usługi: {interpret_indicator(pmi_svc, INDICATORS['PMI_Services'])}")
    
    # Unemployment (inverted - lower is better)
    unemp = indicators.get('Unemployment')
    if unemp:
        if unemp['value'] < 4:
            unemp_score = -10  # Przegrzanie ryzyko
        elif unemp['value'] > 6:
            unemp_score = -20  # Słabość
        else:
            unemp_score = 10  # Zdrowe
        score += unemp_score / 2
        factors.append(f"Bezrobocie: {interpret_indicator(unemp, INDICATORS['Unemployment'])}")
    
    # Fed Funds Rate (lower is stimulative)
    fed = indicators.get('Fed_Funds_Rate')
    if fed:
        if fed['value'] > 5:
            rate_score = -15  # Ściśła
        elif fed['value'] < 2:
            rate_score = 10  # Luźna
        else:
            rate_score = 0  # Neutralna
        score += rate_score / 2
        factors.append(f"Stopy Fed: {interpret_indicator(fed, INDICATORS['Fed_Funds_Rate'])}")
    
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
        return "MOCNA EKSPANSJA - Boom gospodarczy, ryzyko przegrzania"
    elif score > 20:
        return "UMIARKOWANA EKSPANSJA - Zdrowy wzrost, dobre warunki"
    elif score > 0:
        return "WOLNY WZROST - Poniżej potencjału"
    elif score > -20:
        return "TRANSYZJA - Gospodarka zwalnia, możliwa recesja"
    elif score > -40:
        return "ŁAGODNA RECESEJA - Słabość gospodarcza"
    else:
        return "GŁĘBOKA RECESEJA - Ciężka kontrakcja"


def display_macro_dashboard(indicators, health_score):
    """Display macro dashboard."""
    print("\n" + "=" * 70)
    print("MAKROEKONOMICZNY DASHBOARD (TRADINGECONOMICS API)")
    print("=" * 70)
    
    # Health score
    print(f"\n📊 Wynik Zdrowia Gospodarki: {health_score['score']:+.1f}/100")
    print(f"🎯 Faza: {health_score['interpretation']}")
    
    # Indicators
    print(f"\n📈 Kluczowe Wskaźniki:")
    for key, data in indicators.items():
        indicator_info = INDICATORS.get(key)
        if data and indicator_info:
            print(f"\n  {indicator_info['name']}:")
            print(f"    Wartość: {data['value']:.2f}")
            print(f"    Data: {data['date']}")
            print(f"    Interpretacja: {interpret_indicator(data, indicator_info)}")
    
    # Factors
    if health_score.get('factors'):
        print(f"\n📈 Wyniki Zdrowia Gospodarki:")
        for factor in health_score['factors']:
            print(f"  • {factor}")
    
    print("\n" + "=" * 70)


def get_all_macro_data():
    """Fetch all key macro indicators."""
    print("\n" + "=" * 70)
    print("POBIERANIE DANYCH MAKRO (TRADINGECONOMICS API)")
    print("=" * 70)
    
    indicators = {}
    
    for key, indicator_info in INDICATORS.items():
        print(f"\nPobieranie: {indicator_info['name']}...")
        data = fetch_indicator(indicator_info['code'], indicator_info['country'])
        
        if data:
            indicators[key] = data
            print(f"  ✓ Wartość: {data['value']:.2f}")
        else:
            print(f"  ✗ Brak danych")
    
    # Calculate health score
    if indicators:
        health_score = calculate_economic_health_score(indicators)
    else:
        health_score = {'score': 0, 'interpretation': 'No data', 'factors': []}
    
    return indicators, health_score


def save_macro_data(indicators, health_score, filepath=None):
    """Save macro data to JSON."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/te_macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'source': 'TradingEconomics (Free API)',
        'indicators': indicators,
        'health_score': health_score
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n📁 Dane zapisane do: {filepath}")
    return filepath


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='TradingEconomics Macro Data (Free API)')
    parser.add_argument('--save', action='store_true', help='Save to file')
    args = parser.parse_args()
    
    # Fetch all macro data
    indicators, health_score = get_all_macro_data()
    
    # Display dashboard
    display_macro_dashboard(indicators, health_score)
    
    # Save
    if args.save:
        save_macro_data(indicators, health_score)
    
    print(f"\n✅ Pobieranie danych makro zakończone!")


if __name__ == '__main__':
    main()
