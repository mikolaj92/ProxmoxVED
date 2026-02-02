#!/usr/bin/env python3
"""
System Repair - Simple Data Import
Imports today's report into history (no analysis)
"""

import sys
import json
from datetime import datetime
from pathlib import Path


# Paths
FINAL_REPORT_FILE = "/Users/mini-m4-1/clawd/.learnings/daily/20260126/final_report.json"
MARKET_HISTORY_FILE = "/Users/mini-m4-1/clawd/.learnings/market_history.json"


def import_today_data():
    """Import today's report into history."""
    print("\n" + "=" * 70)
    print("SYSTEM REPAIR - PROSTE IMPORTOWANIE DANYCH")
    print("=" * 70)
    
    # Check if today's report exists
    if not Path(FINAL_REPORT_FILE).exists():
        print(f"⚠️ Brak raportu: {FINAL_REPORT_FILE}")
        return False
    
    print(f"📂 Odczytywanie: {FINAL_REPORT_FILE}")
    
    # Load today's report
    try:
        with open(FINAL_REPORT_FILE, 'r') as f:
            today_data = json.load(f)
        print(f"✓ Załadowano raport z: {today_data.get('timestamp', 'N/A')}")
    except Exception as e:
        print(f"✗ Błąd ładowania: {e}")
        return False
    
    # Create history entry
    timestamp = datetime.now().isoformat()
    history_entry = {
        'timestamp': timestamp,
        'type': 'daily_report',
        'source': today_data.get('timestamp', 'unknown'),
        'data': today_data
    }
    
    # Load existing history or create new
    if Path(MARKET_HISTORY_FILE).exists():
        try:
            with open(MARKET_HISTORY_FILE, 'r') as f:
                history = json.load(f)
            print(f"✓ Załadowano {len(history)} historycznych wpisów")
        except Exception as e:
            print(f"✗ Błąd ładowania historii: {e}")
            history = []
    else:
        history = []
        print("✓ Nowa historia utworzona")
    
    # Add new entry
    history.append(history_entry)
    
    # Save history
    try:
        with open(MARKET_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        print(f"✓ Historia zapisana ({len(history)} wpisów)")
    except Exception as e:
        print(f"✗ Błąd zapisu historii: {e}")
        return False
    
    # Save as latest snapshot
    try:
        with open("/Users/mini-m4-1/clawd/.learnings/market_history.json", 'w') as f:
            json.dump(history, f, indent=2)
        print(f"✓ Snapshot zapisany: /Users/mini-m4-1/clawd/.learnings/market_history.json")
    except Exception as e:
        print(f"✗ Błąd zapisu snapshotu: {e}")
    
    # Display summary
    print("\n" + "=" * 70)
    print("📊 PODSUMOWANIE")
    print("=" * 70)
    print(f"Data raportu: {today_data.get('timestamp', 'N/A')}")
    print(f"Zaimportowano: sentyment + makro + cykl + sektory")
    print(f"Historia: {len(history)} wpisów")
    print(f"Plik historii: {MARKET_HISTORY_FILE}")
    print(f"Snapshot: /Users/mini-m4-1/clawd/.learnings/market_history.json")
    
    # Display key data
    sentiment = today_data.get('sentiment', {})
    cycle = today_data.get('cycle', {})
    sectors = today_data.get('sectors_recommendations', {})
    
    print("\n📰 Sentyment:")
    if sentiment:
        print(f"  Artykuły: {sentiment.get('total_articles', 'N/A')}")
        print(f"  Score: {sentiment.get('weighted_sentiment_score', 'N/A')}/100")
        print(f"  Bullish: {sentiment.get('bullish_pct', 0):.1f}%")
        print(f"  Bearish: {sentiment.get('bearish_pct', 0):.1f}%")
    
    print(f"\n📊 Makro:")
    if cycle:
        print(f"  Wynik zdrowia: {cycle.get('combined_score', 'N/A')}/100")
        print(f"  Faza: {cycle.get('phase', 'N/A')}")
        print(f"  Ryzyko: {cycle.get('risk', 'N/A')}")
    
    print(f"\n💼 Sektory:")
    if sectors:
        for sector, rec in sectors.items():
            print(f"  {sector.upper()}: {rec}")
    
    print("\n" + "=" * 70)
    print("✅ IMPORT ZAKOŃCZONY!")
    print("=" * 70)
    
    return True


def main():
    """Main execution."""
    success = import_today_data()
    
    if success:
        print("\n🎯 System gotowy do analizy predykcyjnej!")
        print("Kolejne raporty będą automatycznie dodawane.")
    else:
        print("\n✗ Import nieudany")
        sys.exit(1)


if __name__ == '__main__':
    main()
