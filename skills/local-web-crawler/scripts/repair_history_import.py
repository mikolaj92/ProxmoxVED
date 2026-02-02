#!/usr/bin/env python3
"""
System Repair - Import Today's Data into History
Fixes the empty history issue
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
    print("SYSTEM REPAIR - IMPORTOWANIE DANYCH DO HISTORII")
    print("=" * 70)
    
    # Check if today's report exists
    if not Path(FINAL_REPORT_FILE).exists():
        print(f"⚠️  Brak raportu z dzisiaj: {FINAL_REPORT_FILE}")
        return False
    
    print(f"\n📂 Odczytywanie: {FINAL_REPORT_FILE}")
    
    # Load today's report
    try:
        with open(FINAL_REPORT_FILE, 'r') as f:
            today_data = json.load(f)
        print(f"✓ Załadowano raport z: {today_data['timestamp']}")
    except Exception as e:
        print(f"✗ Błąd ładowania: {e}")
        return False
    
    # Create history entry
    timestamp = datetime.now().isoformat()
    history_entry = {
        'timestamp': timestamp,
        'type': 'daily_import',
        'data': {
            'source': today_data.get('timestamp', '2026-01-26'),
            'sectors': today_data.get('sectors', []),
            'sentiment': today_data.get('sentiment', {}),
            'macro': today_data.get('macro', {}),
            'cycle': today_data.get('cycle', {}),
            'sector_recommendations': today_data.get('sectors_recommendations', {}),
            'notes': 'Imported from daily report - initial data point for prediction system'
        },
        'processed': False
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
        print("✓ Nowa historia została utworzona")
    
    # Add new entry
    history.append(history_entry)
    
    # Save history
    try:
        with open(MARKET_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2, default=str)
        print(f"✓ Historia zaktualizowana ({len(history)} wpisów)")
    except Exception as e:
        print(f"✗ Błąd zapisu historii: {e}")
        return False
    
    # Save as today's snapshot
    TODAY_SNAPSHOT_FILE = "/Users/mini-m4-1/clawd/.learnings/market_history.json"
    try:
        with open(TODAY_SNAPSHOT_FILE, 'w') as f:
            json.dump(history, f, indent=2, default=str)
        print(f"✓ Zapisano snapshot: {TODAY_SNAPSHOT_FILE}")
    except Exception as e:
        print(f"✗ Błąd zapisu snapshotu: {e}")
    
    print("\n" + "=" * 70)
    print("✅ SUKCES! Dane zaimportowane do historii")
    print("=" * 70)
    print(f"\n📊 Podsumowanie:")
    print(f"  Data: {today_data.get('timestamp')}")
    print(f"  Sektory: {', '.join(today_data.get('sectors', []))}")
    print(f"  Sentyment: {today_data.get('sentiment', {}).get('aggregate', {}).get('weighted_sentiment_score', 'N/A')}")
    print(f"  Makro: {today_data.get('macro', {}).get('health_score', {}).get('score', 'N/A')}")
    print(f"  Cykl: {today_data.get('cycle', {}).get('phase', 'N/A')}")
    print(f"\n📁 Historia: {MARKET_HISTORY_FILE}")
    print(f"  Snapshot: {TODAY_SNAPSHOT_FILE}")
    print("=" * 70)
    
    return True


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("SYSTEM REPAIR AGENT")
    print("=" * 70)
    print("Zaimportowuje dane z dzisiaj do systemu historii")
    print("To umożliwia systemowi prediction historyczny analizę")
    print("=" * 70)
    
    # Import data
    success = import_today_data()
    
    if success:
        print("\n✅ Gotowe! System historii ma teraz dane startowe.")
        print("\nDalsze kroki:")
        print("1. Codzienna analiza będzie dodawać kolejne wpisy")
        print("2. System prediction będzie analizować trend historyczny")
        print("3. Po 7-14 dni: faza cyklu zostanie przewidywana")
    else:
        print("\n✗ Nie udało się zaimportować danych")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
