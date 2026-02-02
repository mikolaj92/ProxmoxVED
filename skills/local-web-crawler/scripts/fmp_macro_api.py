#!/usr/bin/env python3
"""
FMP API - Free Macro Data (250 req/day)
Financial Modeling Prep API provides real-time market data
"""

import sys
import json
import requests
from datetime import datetime


# FMP API Configuration
FMP_BASE_URL = "https://financialmodelingprep.com/api/v3"
FMP_API_KEY = "demo"  # Free demo account


# Key macro indicators
MACRO_INDICATORS = {
    'gdp': {
        'endpoint': '/federal-reserve/gdp',
        'name': 'GDP',
        'description': 'Gross Domestic Product'
    },
    'cpi': {
        'endpoint': '/economic-indicators/cpi',
        'name': 'CPI',
        'description': 'Consumer Price Index'
    },
    'unemployment': {
        'endpoint': '/economic-indicators/unemployment',
        'name': 'Unemployment Rate',
        'description': 'Unemployment Rate'
    },
    'fed_rate': {
        'endpoint': '/federal-reserve/rate',
        'name': 'Fed Funds Rate',
        'description': 'Federal Funds Rate'
    }
}


def fetch_macro_indicator(endpoint, name, description):
    """Fetch macro indicator from FMP API."""
    url = FMP_BASE_URL + endpoint
    
    params = {
        'apikey': FMP_API_KEY
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Extract latest value
        if data and len(data) > 0:
            latest = data[0]
            return {
                'value': latest.get('value', latest.get('rate', latest.get('value', 0))),
                'date': latest.get('date', latest.get('datetime', datetime.now().isoformat())),
                'source': 'FMP API (Free)'
            }
        return None
            
    except Exception as e:
        print(f"  ✗ Error fetching {name}: {e}")
        return None


def interpret_indicator(data, indicator_name):
    """Interpret economic indicator."""
    if not data:
        return "No data available"
    
    value = data['value']
    
    # GDP
    if 'GDP' in indicator_name.upper():
        if value > 3:
            return f"Mocny wzrost PKB (+{value-2:.1f}% YoY): Boom gospodarczy"
        elif value > 2:
            return f"Wzrost PKB (+{value-2:.1f}% YoY): Zdrowy wzrost"
        elif value < 0:
            return f"Kontrakcja PKB ({value:+.1f}% YoY): Recesja"
        else:
            return f"Umiarkowany wzrost PKB: {value:.2f}%"
    
    # Unemployment
    elif 'UNEMPLOYMENT' in indicator_name.upper():
        if value < 4:
            return f"Niskie bezrobocie ({value:.1f}%): Mocny rynek pracy (ryzyko inflacji)"
        elif value > 6:
            return f"Wysokie bezrobocie ({value:.1f}%): Słabość gospodarcza"
        else:
            return f"Umiarkowane bezrobocie ({value:.1f}%): Zbalansowany rynek pracy"
    
    # Fed Funds Rate
    elif 'FED' in indicator_name.upper() or 'RATE' in indicator_name.upper():
        if value > 5:
            return f"Wysokie stopy ({value:.2f}%): Ściśła polityka monetarna"
        elif value < 2:
            return f"Niskie stopy ({value:.2f}%): Luźna polityka monetarna"
        else:
            return f"Neutralne stopy ({value:.2f}%): Normalna polityka"
    
    # CPI
    elif 'CPI' in indicator_name.upper():
        if value > 4:
            return f"Wysoka inflacja ({value-2:.1f}% YoY): Wysokie ceny"
        elif value > 2:
            return f"Umiarkowana inflacja ({value-2:.1f}% YoY): Zdrowy zakres"
        elif value < 1:
            return f"Niska inflacja ({value-2:.1f}% YoY): Ryzyko deflacji"
        else:
            return f"CPI: {value:.2f}"
    
    else:
        return f"Wartość: {value:.2f}"


def calculate_economic_health_score(indicators):
    """Calculate economic health score (-100 to +100)."""
    if not indicators:
        return None
    
    score = 0
    factors = []
    
    # Unemployment (inverted - lower is better)
    unemp = indicators.get('unemployment')
    if unemp:
        unemp_value = unemp['value']
        if unemp_value < 4:
            unemp_score = -10  # Przegrzanie
        elif unemp_value > 6:
            unemp_score = -20  # Słabość
        else:
            unemp_score = 10  # Zdrowe
        score += unemp_score / 2
        factors.append(f"Bezrobocie: {interpret_indicator(unemp, 'UNEMPLOYMENT')}")
    
    # Fed Funds Rate (lower is stimulative)
    fed = indicators.get('fed_rate')
    if fed:
        fed_value = fed['value']
        if fed_value > 5:
            rate_score = -15  # Ściśła
        elif fed_value < 2:
            rate_score = 10  # Luźna
        else:
            rate_score = 0  # Neutralna
        score += rate_score / 2
        factors.append(f"Stopy Fed: {interpret_indicator(fed, 'FED RATE')}")
    
    # CPI (moderate is best)
    cpi = indicators.get('cpi')
    if cpi:
        cpi_value = cpi['value']
        if cpi_value > 4:
            cpi_score = -15  # Wysoka
        elif cpi_value < 1:
            cpi_score = -10  # Niska (deflacja)
        else:
            cpi_score = 5  # Zdrowa
        score += cpi_score / 5
        factors.append(f"Inflacja CPI: {interpret_indicator(cpi, 'CPI')}")
    
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
        return "WOLNY WZROST - Powyżej potencjału"
    elif score > -20:
        return "TRANSYZJA - Gospodarka zwalnia, możliwa recesja"
    elif score > -40:
        return "ŁAGODNA RECESEJA - Słabość gospodarcza"
    else:
        return "GŁĘBOKA RECESEJA - Ciężka kontrakcja"


def display_fmp_dashboard(indicators, health_score):
    """Display FMP API macro dashboard."""
    print("\n" + "=" * 70)
    print("MAKROEKONOMICZNY DASHBOARD (FMP API - DARMOWE)")
    print("=" * 70)
    
    # Health score
    print(f"\n📊 Wynik Zdrowia Gospodarki: {health_score['score']:+.1f}/100")
    print(f"🎯 Faza: {health_score['interpretation']}")
    
    # Indicators
    print(f"\n📈 Kluczowe Wskaźniki:")
    for key, data in indicators.items():
        if data:
            indicator_info = MACRO_INDICATORS.get(key, {})
            print(f"\n  {indicator_info['name']}:")
            print(f"    Wartość: {data['value']:.2f}")
            print(f"    Data: {data['date'][:10]}")
            print(f"    Interpretacja: {interpret_indicator(data, indicator_info['name'])}")
    
    # Factors
    if health_score.get('factors'):
        print(f"\n📈 Wyniki Zdrowia Gospodarki:")
        for factor in health_score['factors']:
            print(f"  • {factor}")
    
    print("\n" + "=" * 70)
    print(f"Źródło: FMP API (Financial Modeling Prep)")
    print(f"Limit: 250 requestów/dzień")
    print("=" * 70)


def save_fmp_data(indicators, health_score, filepath=None):
    """Save FMP macro data to JSON."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/fmp_macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'source': 'FMP API (Free - 250 req/day)',
        'indicators': indicators,
        'health_score': health_score
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n📁 Dane zapisane do: {filepath}")
    return filepath


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("FMP API - MAKRO DANE (DARMOWE)")
    print("=" * 70)
    print("Pobieranie danych makro z Financial Modeling Prep API...")
    print(f"Limit: 250 requestów/dzień")
    print(f"API Key: {FMP_API_KEY} (demo)")
    print("=" * 70)
    
    # Fetch all indicators
    indicators = {}
    
    for key, indicator_info in MACRO_INDICATORS.items():
        print(f"\nPobieranie: {indicator_info['name']}...")
        data = fetch_macro_indicator(
            indicator_info['endpoint'],
            indicator_info['name'],
            indicator_info['description']
        )
        
        if data:
            indicators[key] = data
            print(f"  ✓ Wartość: {data['value']:.2f}")
    
    # Calculate health score
    if indicators:
        health_score = calculate_economic_health_score(indicators)
        
        # Display dashboard
        display_fmp_dashboard(indicators, health_score)
        
        # Save data
        save_fmp_data(indicators, health_score)
    else:
        print("\n✗ Nie udało się pobrać żadnych danych")
        print("  Możliwe przyczyny:")
        print("  - FMP API demo account ma ograniczenia")
        print("  - API key wymagany dla pełnego dostępu")
        print("  - Alternatywa: Użyj mock dane (działające)")


if __name__ == '__main__':
    main()
