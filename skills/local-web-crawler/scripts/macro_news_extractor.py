#!/usr/bin/env python3
"""
Macro Data Extraction from Yahoo Finance News
Parses macro indicators from news articles using pattern matching
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

import feedparser
import requests


# RSS feeds
RSS_SOURCES = {
    'yahoo_finance': {
        'url': 'https://finance.yahoo.com/rss',
        'name': 'Yahoo Finance'
    },
    'yahoo_finance_markets': {
        'url': 'https://finance.yahoo.com/rss/markets',
        'name': 'Yahoo Finance Markets'
    }
}


# Macro patterns to extract from articles
MACRO_PATTERNS = {
    'GDP': [
        r'GDP\s+grew\s+by\s+([\d.]+)%?',
        r'gross\s+domestic\s+product\s+increased\s+by\s+([\d.]+)%?',
        r'economic\s+growth\s+of\s+([\d.]+)%?'
    ],
    'CPI': [
        r' CPI\s+(of\s+)?([\d.]+)%',
        r'inflation\s+rate\s+of\s+([\d.]+)%?',
        r'consumer\s+price\s+index\s+rose\s+by\s+([\d.]+)%?',
        r'inflation\s+at\s+([\d.]+)%?'
    ],
    'Unemployment': [
        r'unemployment\s+rate\s+(?:at|of\s+)?([\d.]+)%?',
        r'jobless\s+rate\s+(?:at|of\s+)?([\d.]+)%?',
        r'([\d.]+)%?\s+unemployment'
    ],
    'Fed_Funds_Rate': [
        r'Fed\s+Funds\s+Rate\s+(?:at|of\s+)?([\d.]+)%?',
        r'interest\s+rate\s+(?:at|of\s+)?([\d.]+)%?',
        r'central\s+bank\s+rate\s+(?:at|of\s+)?([\d.]+)%?'
    ],
    'PMI_Manufacturing': [
        r'PMI\s+(?:manufacturing|factory)?\s+at\s+([\d.]+)',
        r'ISM\s+Manufacturing\s+at\s+([\d.]+)',
        r'factory\s+activity\s+at\s+([\d.]+)'
    ],
    'PMI_Services': [
        r'PMI\s+(?:services|non-manufacturing)\s+at\s+([\d.]+)',
        r'ISM\s+Services\s+at\s+([\d.]+)',
        r'service\s+sector\s+at\s+([\d.]+)'
    ]
}


def extract_macro_from_article(title, summary):
    """Extract macro indicators from article text."""
    full_text = f"{title} {summary}".lower()
    
    extracted = {}
    
    for indicator_name, patterns in MACRO_PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            
            if matches:
                # Extract numeric values
                for match in matches:
                    try:
                        if isinstance(match, tuple):
                            value = float(match[1])
                        elif isinstance(match, str):
                            value = float(match.replace('%', ''))
                        else:
                            value = float(match)
                        
                        # Store first match
                        if indicator_name not in extracted:
                            extracted[indicator_name] = {
                                'value': value,
                                'source': 'Yahoo Finance News',
                                'confidence': 'high' if len(matches) > 1 else 'medium'
                            }
                    except ValueError:
                        continue
    
    return extracted


def interpret_macro_value(indicator_name, value):
    """Interpret macro indicator value."""
    if indicator_name == 'GDP':
        if value > 3:
            return f"Mocny wzrost ({value:+.1f}% YoY): Boom gospodarczy"
        elif value > 2:
            return f"Wzrost ({value:+.1f}% YoY): Zdrowa gospodarka"
        elif value > 0:
            return f"Wolny wzrost ({value:+.1f}% YoY): Poniżej potencjału"
        elif value < 0:
            return f"Kontrakcja ({value:+.1f}% YoY): Recesja"
        else:
            return f"Stabilna gospodarka"
    
    elif indicator_name == 'CPI':
        if value > 4:
            return f"Wysoka inflacja ({value:.1f}% YoY): Wysokie ceny"
        elif value > 2:
            return f"Umiarkowana inflacja ({value:.1f}% YoY): Zdrowy zakres"
        elif value > 1:
            return f"Niska inflacja ({value:.1f}% YoY): Ryzyko deflacji"
        elif value < 1:
            return f"Deflacja ({value:.1f}% YoY): Spadek cen"
        else:
            return f"Stabilne ceny"
    
    elif indicator_name == 'Unemployment':
        if value < 4:
            return f"Niskie bezrobocie ({value:.1f}%): Mocny rynek pracy (ryzyko inflacji)"
        elif value < 5:
            return f"Umiarkowane bezrobocie ({value:.1f}%): Zbalansowany rynek pracy"
        elif value > 6:
            return f"Wysokie bezrobocie ({value:.1f}%): Słabość gospodarcza"
        else:
            return f"Normalne bezrobocie ({value:.1f}%)"
    
    elif indicator_name == 'Fed_Funds_Rate':
        if value > 5:
            return f"Wysokie stopy ({value:.2f}%): Ścisła polityka monetarna"
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
            return f"PMI {value:.1f}: Neutralna"
    
    else:
        return f"Wartość: {value}"


def fetch_rss_feed(feed_url):
    """Fetch RSS feed."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(feed_url, headers=headers, timeout=15)
        response.raise_for_status()
        return feedparser.parse(response.text)
    except Exception as e:
        print(f"  ✗ Error fetching RSS: {e}")
        return None


def crawl_macro_from_news():
    """Crawl news and extract macro indicators."""
    print("\n" + "=" * 70)
    print("MAKRO DANE Z NEWSÓW (YAHOO FINANCE)")
    print("=" * 70)
    
    all_articles = []
    extracted_macro = {}
    
    # Fetch RSS feeds
    for feed_name, feed_config in RSS_SOURCES.items():
        print(f"\nFetchng: {feed_config['name']}...")
        
        feed = fetch_rss_feed(feed_config['url'])
        if not feed:
            continue
        
        # Process entries
        for entry in feed.entries[:50]:
            title = entry.get('title', '')
            summary = entry.get('summary', '')
            
            # Extract macro from this article
            macro = extract_macro_from_article(title, summary)
            
            if macro:
                for indicator, data in macro.items():
                    if indicator not in extracted_macro:
                        extracted_macro[indicator] = {
                            'value': data['value'],
                            'source': data['source'],
                            'confidence': data['confidence'],
                            'found_in': entry.get('link', ''),
                            'count': 1
                        }
                    else:
                        # Multiple mentions = higher confidence
                        extracted_macro[indicator]['count'] += 1
                        if extracted_macro[indicator]['count'] >= 2:
                            extracted_macro[indicator]['confidence'] = 'high'
            
            article_data = {
                'title': title,
                'url': entry.get('link'),
                'published': entry.get('published', datetime.now().isoformat()),
                'macro_extracted': bool(macro)
            }
            
            all_articles.append(article_data)
            
            if len(all_articles) % 10 == 0:
                print(f"  Processed {len(all_articles)} articles...")
    
    print(f"\n✓ Processed {len(all_articles)} articles")
    
    # Format extracted macro data
    formatted_macro = {}
    for indicator, data in extracted_macro.items():
        indicator_info = {
            'value': data['value'],
            'date': datetime.now().isoformat(),
            'source': data['source'],
            'confidence': data['confidence'],
            'mentions': data['count'],
            'interpretation': interpret_macro_value(indicator, data['value'])
        }
        
        # Map to standard names
        if indicator == 'Fed_Funds_Rate':
            formatted_macro['Fed_Funds_Rate'] = indicator_info
        else:
            formatted_macro[indicator] = indicator_info
    
    print(f"\n📊 Wyekstraktowane wskaźniki makro: {len(formatted_macro)}")
    for name, data in formatted_macro.items():
        print(f"  {name}: {data['value']:.2f} ({data['interpretation']})")
    
    return formatted_macro


def calculate_economic_health_score(macro_data):
    """Calculate economic health score from extracted macro."""
    if not macro_data:
        return {'score': 0, 'interpretation': 'No data', 'factors': []}
    
    score = 0
    factors = []
    
    # Unemployment (inverted)
    if 'Unemployment' in macro_data:
        unemp_value = macro_data['Unemployment']['value']
        if unemp_value < 4:
            unemp_score = -10
            factors.append(f"Bezrobocie: {macro_data['Unemployment']['interpretation']}")
        elif unemp_value > 6:
            unemp_score = -20
            factors.append(f"Bezrobocie: {macro_data['Unemployment']['interpretation']}")
        else:
            unemp_score = 10
            factors.append(f"Bezrobocie: {macro_data['Unemployment']['interpretation']}")
        score += unemp_score / 2
    
    # Fed Funds Rate (inverted - lower is stimulative)
    if 'Fed_Funds_Rate' in macro_data:
        fed_value = macro_data['Fed_Funds_Rate']['value']
        if fed_value > 5:
            rate_score = -15
            factors.append(f"Stopy Fed: {macro_data['Fed_Funds_Rate']['interpretation']}")
        elif fed_value < 2:
            rate_score = 10
            factors.append(f"Stopy Fed: {macro_data['Fed_Funds_Rate']['interpretation']}")
        else:
            rate_score = 0
            factors.append(f"Stopy Fed: {macro_data['Fed_Funds_Rate']['interpretation']}")
        score += rate_score / 2
    
    # PMI
    pmi_scores = []
    if 'PMI_Manufacturing' in macro_data:
        pmi_m = macro_data['PMI_Manufacturing']['value']
        pmi_score_m = (pmi_m - 50) * 3
        pmi_scores.append(f"PMI Produkcja: {macro_data['PMI_Manufacturing']['interpretation']}")
        score += pmi_score_m / 3
    
    if 'PMI_Services' in macro_data:
        pmi_s = macro_data['PMI_Services']['value']
        pmi_score_s = (pmi_s - 50) * 2
        pmi_scores.append(f"PMI Usługi: {macro_data['PMI_Services']['interpretation']}")
        score += pmi_score_s / 3
    
    if pmi_scores:
        factors.extend(pmi_scores)
    
    # Normalize to -100 to +100
    normalized_score = max(-100, min(100, score))
    
    # Determine phase
    if normalized_score > 50:
        phase = "MOCNA EKSPANSJA - Boom gospodarczy"
    elif normalized_score > 20:
        phase = "UMIARKOWANA EKSPANSJA - Zdrowy wzrost"
    elif normalized_score > 0:
        phase = "WOLNY WZROST - Powyżej potencjału"
    elif normalized_score > -20:
        phase = "TRANSYZJA - Gospodarka zwalnia, możliwa recesja"
    elif normalized_score > -40:
        phase = "ŁAGODNA RECESEJA - Słabość gospodarcza"
    else:
        phase = "GŁĘBOKA RECESEJA - Ciężka kontrakcja"
    
    return {
        'score': normalized_score,
        'interpretation': phase,
        'factors': factors
    }


def save_macro_data(macro_data, health_score, filepath=None):
    """Save macro data to JSON."""
    if filepath is None:
        filepath = f"/Users/mini-m4-1/clawd/.learnings/macro_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    data = {
        'timestamp': datetime.now().isoformat(),
        'source': 'Yahoo Finance News Extraction',
        'indicators': macro_data,
        'health_score': health_score
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n📁 Dane zapisane do: {filepath}")
    return filepath


def display_macro_dashboard(macro_data, health_score):
    """Display macro data dashboard."""
    print("\n" + "=" * 70)
    print("MAKRO DASHBOARD (YAHOO FINANCE NEWS)")
    print("=" * 70)
    
    print(f"\n📊 Wynik Zdrowia Gospodarki: {health_score['score']:+.1f}/100")
    print(f"🎯 Faza: {health_score['interpretation']}")
    
    print(f"\n📈 Wyekstraktowane Wskaźniki:")
    for name, data in macro_data.items():
        print(f"\n  {name}:")
        print(f"    Wartość: {data['value']:.2f}")
        print(f"    Data: {data['date'][:10]}")
        print(f"    Interpretacja: {data['interpretation']}")
        print(f"    Źródło: {data['source']} (wspomnienia: {data['mentions']})")
    
    if health_score.get('factors'):
        print(f"\n📈 Wyniki Zdrowia Gospodarki:")
        for factor in health_score['factors']:
            print(f"  • {factor}")
    
    print("\n" + "=" * 70)


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Macro Data from Yahoo Finance News')
    parser.add_argument('--save', action='store_true', help='Save to file')
    parser.add_argument('--summary', action='store_true', help='Display summary')
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("EKSTRAKTOR DANYCH MAKRO Z NEWSÓW")
    print("=" * 70)
    print("Parsuje artykuły Yahoo Finance i ekstraktuje wskaźniki makro:")
    print("  - PKB (GDP)")
    print("  - CPI (Inflacja)")
    print("  - Bezrobocie")
    print("  - Stopy Fed")
    print("  - PMI")
    print("=" * 70)
    
    # Crawl and extract macro
    macro_data = crawl_macro_from_news()
    
    if not macro_data:
        print("\n✗ Nie udało się wyekstraktować żadnych danych makro")
        print("Możliwe przyczyny:")
        print("  - Brak artykułów o gospodarce w newsach")
        print("  - Wzorce nie pasują do aktualnych tytułów")
        return
    
    # Calculate health score
    health_score = calculate_economic_health_score(macro_data)
    
    # Display dashboard
    if args.summary or not args.save:
        display_macro_dashboard(macro_data, health_score)
    
    # Save
    if args.save:
        save_macro_data(macro_data, health_score)
    
    print("\n✅ Ekstrakcja zakończona!")


if __name__ == '__main__':
    main()
