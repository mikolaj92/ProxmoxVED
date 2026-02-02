#!/usr/bin/env python3
"""
Market Prediction History System
Aggregates, stores, and analyzes historical market data
Builds predictions based on macro cycles, sentiment, and patterns
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np


# Storage paths
HISTORY_FILE = "/Users/mini-m4-1/clawd/.learnings/market_history.json"
ANALYSIS_FILE = "/Users/mini-m4-1/clawd/.learnings/market_analysis.json"
PREDICTIONS_FILE = "/Users/mini-m4-1/clawd/.learnings/market_predictions.json"


class MarketHistory:
    """Store and manage historical market data."""

    def __init__(self):
        self.history = []
        self.load_history()

    def load_history(self):
        """Load historical data from file."""
        if Path(HISTORY_FILE).exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
                    print(f"✓ Załadowano {len(self.history)} historycznych wpisów")
            except Exception as e:
                print(f"⚠️  Błąd ładowania historii: {e}")
                self.history = []
        else:
            self.history = []

    def add_entry(self, entry_type, data):
        """Add new historical entry."""
        timestamp = datetime.now().isoformat()

        history_entry = {
            'timestamp': timestamp,
            'type': entry_type,  # 'daily_report', 'macro_snapshot', 'sentiment_snapshot'
            'data': data,
            'processed': False
        }

        self.history.append(history_entry)
        self.save_history()

        print(f"✓ Dodano: {entry_type} ({timestamp})")

        return history_entry

    def save_history(self):
        """Save history to file."""
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_entries': len(self.history),
            'entries': self.history
        }

        with open(HISTORY_FILE, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✓ Historia zapisana ({len(self.history)} wpisów)")

    def get_recent_entries(self, days=30):
        """Get entries from last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        return [e for e in self.history if datetime.fromisoformat(e['timestamp']) >= cutoff]

    def get_entries_by_type(self, entry_type):
        """Get all entries of specific type."""
        return [e for e in self.history if e['type'] == entry_type]


class MarketAnalyzer:
    """Analyze historical data for patterns and predictions."""

    def __init__(self, history):
        self.history = history.history
        self.analysis = {}
        self.load_analysis()

    def load_analysis(self):
        """Load previous analysis."""
        if Path(ANALYSIS_FILE).exists():
            try:
                with open(ANALYSIS_FILE, 'r') as f:
                    self.analysis = json.load(f)
                    print(f"✓ Załadowano analizę: {len(self.analysis)} cykli/obserwacji")
            except Exception as e:
                print(f"⚠️  Błąd ładowania analizy: {e}")
                self.analysis = {}
        else:
            self.analysis = {}

    def save_analysis(self):
        """Save analysis to file."""
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_analyses': len(self.analysis),
            'analyses': self.analysis
        }

        with open(ANALYSIS_FILE, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✓ Analiza zapisana")

    def detect_cycles(self):
        """Detect market cycles from historical data."""
        cycles = []

        # Extract macro data points
        macro_data_points = []
        for entry in self.history:
            if entry['type'] == 'daily_report' and 'macro' in entry.get('data', {}):
                macro_data_points.append(entry['data']['macro'])

        if len(macro_data_points) < 2:
            return cycles

        # Analyze trends
        timestamps = [datetime.fromisoformat(d['health_score']['timestamp']) for d in macro_data_points if 'health_score' in d]
        health_scores = [d['health_score']['score'] for d in macro_data_points if 'health_score' in d]
        sentiment_scores = [d['sentiment']['aggregate']['weighted_sentiment_score'] for d in macro_data_points if 'sentiment' in d]

        # Detect cycles (up, down, sideways)
        if len(health_scores) >= 2:
            score_changes = np.diff(health_scores)

            # Identify cycle phases
            cycle = {
                'start_date': timestamps[0].isoformat(),
                'end_date': timestamps[-1].isoformat(),
                'trend': 'up' if health_scores[-1] > health_scores[0] else 'down',
                'volatility': np.std(health_scores) if len(health_scores) > 1 else 0,
                'avg_health': np.mean(health_scores),
                'min_health': np.min(health_scores),
                'max_health': np.max(health_scores)
            }

            cycles.append(cycle)

        return cycles

    def predict_next_phase(self):
        """Predict next market phase based on historical patterns."""
        if len(self.history) < 3:
            return None

        # Get recent cycles
        cycles = self.detect_cycles()

        if not cycles:
            return None

        # Simple prediction: trend continuation
        last_cycle = cycles[-1]
        if last_cycle['trend'] == 'up':
            predicted_trend = 'up'
            predicted_phase = 'Expansion continuing'
        elif last_cycle['trend'] == 'down':
            predicted_trend = 'down'
            predicted_phase = 'Contraction continuing'
        else:
            predicted_trend = 'sideways'
            predicted_phase = 'Consolidation'

        prediction = {
            'predicted_date': (datetime.now() + timedelta(days=7)).isoformat(),
            'predicted_trend': predicted_trend,
            'predicted_phase': predicted_phase,
            'confidence': 0.6,  # Simple model confidence
            'basis': f"Ostatni {last_cycle['trend']} trend ({last_cycle['start_date']} do {last_cycle['end_date']})"
        }

        return prediction

    def analyze_sentiment_patterns(self):
        """Analyze sentiment patterns over time."""
        sentiment_series = []

        for entry in self.history:
            if entry['type'] == 'daily_report' and 'sentiment' in entry.get('data', {}):
                sentiment = entry['data']['sentiment']['aggregate']
                sentiment_series.append({
                    'timestamp': sentiment['timestamp'],
                    'bullish_pct': sentiment['bullish_pct'],
                    'bearish_pct': sentiment['bearish_pct'],
                    'score': sentiment['weighted_sentiment_score']
                })

        if len(sentiment_series) < 2:
            return sentiment_series

        # Detect patterns
        timestamps = [datetime.fromisoformat(s['timestamp']) for s in sentiment_series]
        scores = [s['score'] for s in sentiment_series]

        # Calculate rolling average (7-day window)
        rolling_avg = []
        for i in range(len(scores)):
            start = max(0, i - 6)
            end = i + 1
            window = scores[start:end]
            rolling_avg.append(np.mean(window) if window else scores[i])

        # Identify sentiment shifts
        sentiment_shifts = []
        for i in range(len(rolling_avg) - 1):
            if abs(rolling_avg[i+1] - rolling_avg[i]) > 20:  # 20-point shift
                shift = {
                    'timestamp': timestamps[i+1].isoformat(),
                    'from_value': rolling_avg[i],
                    'to_value': rolling_avg[i+1],
                    'shift_amount': rolling_avg[i+1] - rolling_avg[i],
                    'type': 'significant' if abs(rolling_avg[i+1] - rolling_avg[i]) > 40 else 'moderate'
                }
                sentiment_shifts.append(shift)

        return {
            'series_length': len(sentiment_series),
            'average_sentiment': np.mean(scores) if scores else 0,
            'volatility': np.std(scores) if len(scores) > 1 else 0,
            'current_trend': 'increasing' if scores[-1] > scores[0] else 'decreasing',
            'sentiment_shifts': sentiment_shifts
        }

    def run_full_analysis(self):
        """Run comprehensive market analysis."""
        print("\n" + "=" * 70)
        print("MARKET PREDICTION HISTORY ANALYZER")
        print("=" * 70)

        # Detect cycles
        print("\n📈 DETEKCJA CYKLI:")
        cycles = self.detect_cycles()

        if cycles:
            for i, cycle in enumerate(cycles, 1):
                print(f"\n  Cykl #{i}:")
                print(f"    Okres: {cycle['start_date']} do {cycle['end_date']}")
                print(f"    Trend: {cycle['trend'].upper()}")
                print(f"    Średnia zdrowia: {cycle['avg_health']:.1f}/100")
                print(f"    Wartości: min={cycle['min_health']:.1f}, max={cycle['max_health']:.1f}")
                print(f"    Zmienność: {cycle['volatility']:.1f}")
        else:
            print("  Za mało danych do detekcji cykli")

        # Predict next phase
        print("\n🎯 PRZEWIDYWANIE PRZYSZŁOŚCI:")
        prediction = self.predict_next_phase()

        if prediction:
            print(f"\n  Przewidywana data: {prediction['predicted_date']}")
            print(f"  Przewidywany trend: {prediction['predicted_trend'].upper()}")
            print(f"  Przewidywana faza: {prediction['predicted_phase']}")
            print(f"  Pewność: {prediction['confidence']:.0%}")
            print(f"  Podstawa: {prediction['basis']}")

        # Analyze sentiment patterns
        print("\n📊 ANALIZA WZORCÓW SENTYMENTU:")
        sentiment_patterns = self.analyze_sentiment_patterns()

        if sentiment_patterns:
            print(f"\n  Długość serii: {sentiment_patterns['series_length']} dni")
            print(f"  Średni sentyment: {sentiment_patterns['average_sentiment']:+.1f}/100")
            print(f"  Zmienność: {sentiment_patterns['volatility']:.1f}")
            print(f"  Obecny trend: {sentiment_patterns['current_trend'].upper()}")

            if sentiment_patterns.get('sentiment_shifts'):
                print(f"\n  Istotne zmiany sentymentu:")
                for shift in sentiment_patterns['sentiment_shifts'][:5]:
                    print(f"    {shift['timestamp']}: {shift['from_value']:+.1f} → {shift['to_value']:+.1f}")
                    print(f"      {shift['shift_amount']:+.1f} ({shift['type']})")

        # Save analysis
        analysis_result = {
            'timestamp': datetime.now().isoformat(),
            'cycle_analysis': cycles,
            'sentiment_analysis': sentiment_patterns,
            'prediction': prediction,
            'summary': {
                'data_points': len(self.history),
                'cycles_detected': len(cycles) if cycles else 0,
                'sentiment_points': sentiment_patterns.get('series_length', 0)
            }
        }

        self.analysis[f"analysis_{datetime.now().strftime('%Y%m%d')}"] = analysis_result
        self.save_analysis()

        print(f"\n✓ Analiza zakończona i zapisana")

        return analysis_result


class MarketPredictor:
    """Make market predictions based on historical analysis."""

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.analysis = analyzer.analysis

    def predict(self, days_ahead=7, confidence_threshold=0.7):
        """Predict market conditions N days ahead."""
        if not self.analysis:
            print("⚠️  Brak analizy historycznej")
            return None

        latest_key = sorted(self.analysis.keys())[-1]
        latest_analysis = self.analysis[latest_key]

        if not latest_analysis.get('prediction'):
            print("⚠️  Brak przewidywań")
            return None

        prediction = latest_analysis['prediction']

        # Apply confidence filter
        if prediction['confidence'] < confidence_threshold:
            print(f"⚠️  Niska pewność przewidywania ({prediction['confidence']:.0%}) - wyniki mogą nie być wiarygodne")

        # Generate recommendations
        predictions = []

        for i in range(1, days_ahead + 1):
            future_date = datetime.now() + timedelta(days=i)

            # Simple trend-based prediction
            if prediction['predicted_trend'] == 'up':
                expected_score = min(100, prediction.get('basis_score', 50) + (i * 5))
                expected_phase = "Expansion accelerating"
            elif prediction['predicted_trend'] == 'down':
                expected_score = max(-100, prediction.get('basis_score', 50) - (i * 5))
                expected_phase = "Contraction deepening"
            else:
                expected_score = prediction.get('basis_score', 50)
                expected_phase = "Sideways consolidation"

            pred = {
                'date': future_date.isoformat(),
                'days_ahead': i,
                'expected_health_score': expected_score,
                'expected_phase': expected_phase,
                'confidence': max(0.1, prediction['confidence'] - (i * 0.05)),
                'factors': [prediction['predicted_trend'], prediction['predicted_phase']]
            }

            predictions.append(pred)

        # Save predictions
        predictions_data = {
            'generated_at': datetime.now().isoformat(),
            'basis_analysis': latest_key,
            'predictions': predictions,
            'summary': {
                'total_predictions': len(predictions),
                'horizon_days': days_ahead,
                'average_confidence': np.mean([p['confidence'] for p in predictions]) if predictions else 0
            }
        }

        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(predictions_data, f, indent=2)

        print(f"\n✓ Wygenerowano {len(predictions)} przewidywań (dni: 1-{days_ahead})")
        print(f"  Średnia pewność: {predictions_data['summary']['average_confidence']:.1%}")

        return predictions


def main():
    """Main execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Market Prediction History System')
    parser.add_argument('--days', '-d', type=int, default=30, help='Dni historii do analizy')
    parser.add_argument('--predict', '-p', type=int, default=7, help='Dni do przodu do przewidywania')
    parser.add_argument('--confidence', '-c', type=float, default=0.7, help='Próg pewności')
    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("SYSTEM HISTORII RYNKU I PRZEWIDYWANIA")
    print("=" * 70)
    print(f"Analiza ostatnich {args.days} dni")
    print(f"Przewidywanie na {args.predict} dni")
    print("=" * 70)

    # Initialize systems
    history = MarketHistory()
    analyzer = MarketAnalyzer(history)
    predictor = MarketPredictor(analyzer)

    # Get recent history
    recent_entries = history.get_recent_entries(args.days)

    if not recent_entries:
        print("\n⚠️  Brak historycznych danych")
        return

    print(f"\nZnaleziono {len(recent_entries)} historycznych wpisów")

    # Run full analysis
    analysis = analyzer.run_full_analysis(recent_entries)

    # Generate predictions
    predictions = predictor.predict(args.predict, args.confidence)

    if predictions:
        print("\n" + "=" * 70)
        print("PRZEWIDYWANIA")
        print("=" * 70)

        for i, pred in enumerate(predictions[:7], 1):
            print(f"\nDzień {pred['days_ahead']} ({pred['date'][:10]}):")
            print(f"  Faza: {pred['expected_phase']}")
            print(f"  Zdrowia: {pred['expected_health_score']:+.1f}/100")
            print(f"  Pewność: {pred['confidence']:.0%}")

        print("\n" + "=" * 70)

    print(f"\n✓ System zakończony!")

    print(f"\n" + "=" * 70)
    print("PLIKI:")
    print("=" * 70)
    print(f"Historia: {HISTORY_FILE}")
    print(f"Analiza: {ANALYSIS_FILE}")
    print(f"Przewidywania: {PREDICTIONS_FILE}")
    print("=" * 70)


if __name__ == '__main__':
    main()
