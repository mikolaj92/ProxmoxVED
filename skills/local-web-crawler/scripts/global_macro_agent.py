#!/usr/bin/env python3
"""
Global Macro Intelligence System
Collects and analyzes macro data from multiple countries
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path


# Storage paths
GLOBAL_MACRO_FILE = "/Users/mini-m4-1/clawd/.learnings/global_macro.json"
ANALYSIS_FILE = "/Users/mini-m4-1/clawd/.learnings/global_analysis.json"
PREDICTIONS_FILE = "/Users/mini-m4-1/clawd/.learnings/global_predictions.json"
GLOBAL_REPORT_FILE = "/Users/mini-m4-1/clawd/.learnings/global_report.json"


class GlobalMacroData:
    """Store and manage global macro data."""

    def __init__(self):
        self.data = {}
        self.load_data()

    def load_data(self):
        """Load existing data."""
        if Path(GLOBAL_MACRO_FILE).exists():
            try:
                with open(GLOBAL_MACRO_FILE, 'r') as f:
                    self.data = json.load(f)
                print(f"✓ Załadowano {len(self.data)} regionów")
            except Exception as e:
                print(f"⚠️ Błąd ładowania: {e}")
                self.data = {}
        else:
            self.data = {}

    def add_region_data(self, region_name, indicators):
        """Add/update region data."""
        timestamp = datetime.now().isoformat()

        if region_name not in self.data:
            self.data[region_name] = {
                'country': '',
                'indicators': {},
                'last_updated': timestamp
            }

        # Update indicators
        for indicator_name, value in indicators.items():
            self.data[region_name]['indicators'][indicator_name] = {
                'value': value,
                'timestamp': timestamp
            }

        self.data[region_name]['last_updated'] = timestamp
        self.save_data()

        print(f"✓ Zaktualizowano {region_name}: {', '.join(indicators.keys())}")

        return self.data[region_name]

    def save_data(self):
        """Save data to file."""
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_regions': len(self.data),
            'data': self.data
        }

        with open(GLOBAL_MACRO_FILE, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✓ Dane zapisane ({len(self.data)} regionów)")


class GlobalMacroAnalyzer:
    """Analyze global macro data for patterns."""

    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.analysis = {}
        self.load_analysis()

    def load_analysis(self):
        """Load previous analysis."""
        if Path(ANALYSIS_FILE).exists():
            try:
                with open(ANALYSIS_FILE, 'r') as f:
                    self.analysis = json.load(f)
                print(f"✓ Załadowano analizę: {len(self.analysis)} regionów")
            except Exception as e:
                print(f"⚠️ Błąd ładowania: {e}")
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

    def analyze_interest_rates(self):
        """Analyze interest rates across major central banks."""
        print(f"\n📊 ANALIZA STÓP PROCENTOWYCH")

        rates = {}
        for region, data in self.data_manager.data.items():
            if 'interest_rate' in data.get('indicators', {}):
                rate = data['indicators']['interest_rate']['value']
                currency = data['indicators']['interest_rate'].get('currency', 'N/A')
                rates[region] = {
                    'rate': rate,
                    'currency': currency,
                    'timestamp': data['indicators']['interest_rate']['timestamp']
                }

        if not rates:
            print("  ✗ Brak danych o stopach")
            return None

        # Display rates
        print(f"\n  Aktualne stopy:")
        for region, rate_data in rates.items():
            print(f"    {region.upper()}: {rate_data['rate']:.2f}% ({rate_data['currency']})")

        # Rate differentials
        analysis = {}
        usa_rate = rates.get('fed', {}).get('rate', 0)
        japan_rate = rates.get('boj', {}).get('rate', 0)
        china_rate = rates.get('pboc', {}).get('rate', 0)
        ecb_rate = rates.get('ecb', {}).get('rate', 0)

        analysis['rate_differentials'] = {}
        analysis['rate_differentials']['fed_vs_jpy'] = usa_rate - japan_rate
        analysis['rate_differentials']['fed_vs_cny'] = usa_rate - china_rate
        analysis['rate_differentials']['fed_vs_eur'] = usa_rate - ecb_rate

        # Carry trades
        analysis['carry_trades'] = {}
        if japan_rate < usa_rate:
            analysis['carry_trades']['jpy_long'] = f"Carry USD/JPY (Earn {usa_rate - japan_rate:.2f}%)"
        else:
            analysis['carry_trades']['jpy_long'] = f"Carry JPY/USD (Pay {japan_rate - usa_rate:.2f}%)"

        # Monetary stance
        analysis['monetary_stance'] = {}
        if usa_rate > 3:
            analysis['monetary_stance']['fed'] = "Tight (Hawkish)"
        elif usa_rate < 1:
            analysis['monetary_stance']['fed'] = "Loose (Dovish)"
        else:
            analysis['monetary_stance']['fed'] = "Neutral"

        # Save analysis
        self.analysis[f"interest_rates_{datetime.now().strftime('%Y%m%d')}"] = analysis
        self.save_analysis()

        return analysis


class GlobalMacroPredictor:
    """Make predictions based on global macro analysis."""

    def __init__(self, analyzer, data_manager):
        self.analyzer = analyzer
        self.data_manager = data_manager
        self.analysis = analyzer.analysis

    def predict_regional_growth(self, days_ahead=90):
        """Predict regional growth based on trends."""
        print(f"\n📈 PRZEWIDYWANIE WZROSTU REGIONALNEGO (dni: {days_ahead})")

        predictions = {}

        for region, data in self.data_manager.data.items():
            gdp_growth = None
            if 'gdp_growth' in data.get('indicators', {}):
                gdp_growth = data['indicators']['gdp_growth']['value']

            if gdp_growth:
                # Project forward with noise
                noise = (datetime.now().microsecond() % 100) / 500

                projected_growth = gdp_growth * (0.95 + (noise * 0.05))
                prediction_date = (datetime.now() + timedelta(days=days_ahead)).isoformat()

                predictions[region] = {
                    'country': data['country'],
                    'current_growth': gdp_growth,
                    'projected_growth': projected_growth,
                    'growth_trend': 'Accelerating' if projected_growth > gdp_growth else 'Decelerating',
                    'prediction_date': prediction_date,
                    'confidence': 0.6  # Simple model confidence
                }

        # Save predictions
        if predictions:
            prediction_data = {
                'generated_at': datetime.now().isoformat(),
                'type': 'regional_growth',
                'horizon_days': days_ahead,
                'predictions': predictions
            }

            with open(PREDICTIONS_FILE, 'w') as f:
                json.dump(prediction_data, f, indent=2)

            print(f"✓ Przewidywania: {len(predictions)} regionów")

        return predictions

    def generate_recommendations(self):
        """Generate global investment recommendations."""
        print(f"\n💼 GLOBALNE REKOMENDACJE")

        recommendations = {
            'overall_strategy': 'DIVERSIFIED GLOBAL PORTFOLIO',
            'regional_allocations': {},
            'currency_strategy': 'HEDGE AGAINST USD WEAKNESS',
            'commodities': {
                'gold': 'Benefit from USD weakness, inflation hedge',
                'oil': 'Supply constraints from sanctions, geopolitical risk',
                'metals': 'Infrastructure demand supports prices'
            },
            'tech': {
                'us_tech': 'Overvaluation risk, reduce exposure',
                'chinese_tech': 'Growth slowing but AI/semiconductors strong',
                'japanese_tech': 'Currency boost from carry trade'
            }
        }

        # Regional allocations
        recommendations['regional_allocations']['usa'] = 'Underweight (Late cycle)'
        recommendations['regional_allocations']['japan'] = 'Overweight (Carry trade opportunity)'
        recommendations['regional_allocations']['china'] = 'Underweight (Growth slowing)'
        recommendations['regional_allocations']['europe'] = 'Underweight (Recession risk)'
        recommendations['regional_allocations']['emerging_markets'] = 'Equal weight (Diversification)'

        return recommendations


class GlobalMacroAgent:
    """Complete global macro intelligence agent."""

    def __init__(self):
        self.data_manager = GlobalMacroData()
        self.analyzer = GlobalMacroAnalyzer(self.data_manager)
        self.predictor = GlobalMacroPredictor(self.analyzer, self.data_manager)

    def run_full_analysis(self, regions='all'):
        """Run complete global macro analysis."""
        print("\n" + "=" * 70)
        print("SYSTEM GLOBALNEGO MAKRO INTELLIGENCE")
        print("=" * 70)
        print(f"Analiza regionów: {regions}")

        # Collect data (mock for now)
        if regions == 'all' or 'usa' in regions:
            self.data_manager.add_region_data('usa', {
                'gdp_growth': 2.3,
                'interest_rate': 4.33,
                'inflation': 2.9,
                'unemployment': 4.1
            })

        if regions == 'all' or 'japan' in regions:
            self.data_manager.add_region_data('japan', {
                'gdp_growth': 1.0,
                'interest_rate': 0.25,
                'inflation': 2.5,
                'unemployment': 2.4
            })

        if regions == 'all' or 'china' in regions:
            self.data_manager.add_region_data('china', {
                'gdp_growth': 5.2,
                'interest_rate': 4.35,
                'inflation': 2.8,
                'unemployment': 5.1
            })

        if regions == 'all' or 'europe' in regions:
            self.data_manager.add_region_data('europe', {
                'gdp_growth': 1.1,
                'interest_rate': 4.00,
                'inflation': 2.7,
                'unemployment': 6.5
            })

        if regions == 'all' or 'iran' in regions:
            self.data_manager.add_region_data('iran', {
                'oil_price': 78.50,
                'sanctions': 'active'
            })

        # Analyze interest rates
        print("\n" + "=" * 70)
        print("ANALIZA GLOBALNA")
        print("=" * 70)
        rate_analysis = self.analyzer.analyze_interest_rates()

        # Generate growth predictions
        print("\n" + "=" * 70)
        print("PRZEWIDYWANIE WZROSTU")
        print("=" * 70)
        growth_predictions = self.predictor.predict_regional_growth(days_ahead=90)

        # Generate recommendations
        recommendations = self.predictor.generate_recommendations()

        # Compile report
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_points': len(self.data_manager.data),
            'rate_analysis': rate_analysis,
            'growth_predictions': growth_predictions,
            'recommendations': recommendations,
            'summary': {
                'regions_analyzed': len(self.data_manager.data),
                'prediction_horizon': 90,
                'strategy': recommendations['overall_strategy']
            }
        }

        # Save report
        with open(GLOBAL_REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Raport zapisany: {GLOBAL_REPORT_FILE}")

        # Display summary
        self.display_dashboard(report)

        return report

    def display_dashboard(self, report):
        """Display global macro dashboard."""
        print("\n" + "=" * 70)
        print("DASHBOARD GLOBALNY")
        print("=" * 70)

        # Rate analysis
        rate_analysis = report.get('rate_analysis', {})
        if rate_analysis:
            print(f"\n📊 STOPY PROCENTOWE:")
            print(f"  Fed (USA): {self.data_manager.data.get('usa', {}).get('indicators', {}).get('interest_rate', {}).get('value', 0):.2f}%")
            print(f"  BOJ (Japonia): {self.data_manager.data.get('japan', {}).get('indicators', {}).get('interest_rate', {}).get('value', 0):.2f}%")
            print(f"  PBOC (Chiny): {self.data_manager.data.get('china', {}).get('indicators', {}).get('interest_rate', {}).get('value', 0):.2f}%")
            print(f"  ECB (Europa): {self.data_manager.data.get('europe', {}).get('indicators', {}).get('interest_rate', {}).get('value', 0):.2f}%")

            if 'rate_differentials' in rate_analysis:
                diff = rate_analysis['rate_differentials']
                print(f"  Differentiał USA/Japan: {diff.get('fed_vs_jpy', 0):+.2f}%")

            if 'carry_trades' in rate_analysis:
                carry = rate_analysis['carry_trades']
                print(f"  Carry Trade: {carry.get('jpy_long', 'N/A')}")

            if 'monetary_stance' in rate_analysis:
                stance = rate_analysis['monetary_stance'].get('fed', 'N/A')
                print(f"  Stan Fed: {stance}")

        # Growth predictions
        growth_pred = report.get('growth_predictions', {})
        if growth_pred:
            print(f"\n📈 PRZEWIDYWANIA WZROSTU (90 dni):")
            for region, pred in growth_pred.get('predictions', {}).items():
                print(f"  {region.upper()}: {pred['current_growth']:+.1f}% → {pred['projected_growth']:+.1f}% ({pred['growth_trend']})")

        # Recommendations
        recommendations = report.get('recommendations', {})
        if recommendations:
            print(f"\n💼 REKOMENDACJE:")
            print(f"  Strategia ogólna: {recommendations['overall_strategy']}")
            print(f"  Strategia walutowa: {recommendations['currency_strategy']}")

            print(f"\n  Złoto: {recommendations['commodities']['gold']}")
            print(f"  Ropa: {recommendations['commodities']['oil']}")
            print(f"  Metale: {recommendations['commodities']['metals']}")

            print(f"\n  US Tech: {recommendations['tech']['us_tech']}")
            print(f"  Chiński Tech: {recommendations['tech']['chinese_tech']}")
            print(f"  Japoński Tech: {recommendations['tech']['japanese_tech']}")

            if 'regional_allocations' in recommendations:
                print(f"\n  Alokacje regionalne:")
                for region, alloc in recommendations['regional_allocations'].items():
                    print(f"    {region.upper()}: {alloc}")

        print("\n" + "=" * 70)
        print(f"Raport zapisany: {GLOBAL_REPORT_FILE}")
        print("=" * 70)


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("SYSTEM GLOBALNEGO MAKRO INTELLIGENCE")
    print("=" * 70)
    print("Analiza: USA, Japonia, Chiny, Europa, Iran")

    # Initialize agent
    agent = GlobalMacroAgent()

    # Run full analysis
    report = agent.run_full_analysis(regions='all')

    print("\n✅ System zakończony!")


if __name__ == '__main__':
    main()
