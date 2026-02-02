#!/usr/bin/env python3
"""
Global Macro Intelligence System (REPAIRED VERSION)
Analyzes global macro data: USA, Japan, China, Europe, Iran
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
import random


# Storage paths
GLOBAL_MACRO_FILE = "/Users/mini-m4-1/clawd/.learnings/global_macro.json"
GLOBAL_ANALYSIS_FILE = "/Users/mini-m4-1/clawd/.learnings/global_analysis.json"
GLOBAL_PREDICTIONS_FILE = "/Users/mini-m4-1/clawd/.learnings/global_predictions.json"
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
        """Add/update data for specific region."""
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
                'timestamp': timestamp,
                'source': 'Mock Data'
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
        if Path(GLOBAL_ANALYSIS_FILE).exists():
            try:
                with open(GLOBAL_ANALYSIS_FILE, 'r') as f:
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

        with open(GLOBAL_ANALYSIS_FILE, 'w') as f:
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

        # Analyze rate differentials
        usa_rate = rates.get('fed', {}).get('rate', 0)
        japan_rate = rates.get('boj', {}).get('rate', 0)
        china_rate = rates.get('pboc', {}).get('rate', 0)
        ecb_rate = rates.get('ecb', {}).get('rate', 0)

        analysis = {
            'rate_differentials': {},
            'monetary_stance': {},
            'carry_trades': {}
        }

        # Rate differentials
        if usa_rate > 0:
            analysis['rate_differentials']['fed_vs_jpy'] = usa_rate - japan_rate
            analysis['rate_differentials']['fed_vs_cny'] = usa_rate - china_rate
            analysis['rate_differentials']['fed_vs_eur'] = usa_rate - ecb_rate

        # Carry trades
        if japan_rate < usa_rate:
            analysis['carry_trades']['jpy_long'] = f"Carry USD/JPY (Earn {usa_rate - japan_rate:.2f}%)"
        else:
            analysis['carry_trades']['jpy_short'] = f"Carry JPY/USD (Pay {japan_rate - usa_rate:.2f}%)"

        # Monetary stance
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

    def analyze_cross_country_impacts(self):
        """Analyze cross-country macro impacts."""
        print(f"\n🌍 ANALIZA KRÓŻKRAJOWEGO WPŁYWU")

        impacts = {}

        # USD dominance impact
        usa_rate = None
        if 'fed' in self.data_manager.data:
            if 'interest_rate' in self.data_manager.data['fed']['indicators']:
                usa_rate = self.data_manager.data['fed']['indicators']['interest_rate']['value']

        if usa_rate is not None:
            # Japan (carry trade)
            japan_rate = None
            if 'boj' in self.data_manager.data:
                if 'interest_rate' in self.data_manager.data['boj']['indicators']:
                    japan_rate = self.data_manager.data['boj']['indicators']['interest_rate']['value']

            if japan_rate is not None:
                carry_diff = usa_rate - japan_rate
                if abs(carry_diff) > 2:
                    impacts['carry_trade_jpy'] = {
                        'direction': 'Long JPY/USD' if carry_diff < 0 else 'Long USD/JPY',
                        'magnitude': abs(carry_diff),
                        'impact': 'Strong carry trade opportunity'
                    }

            # China (competitive devaluation)
            china_gdp_growth = None
            if 'china' in self.data_manager.data:
                if 'gdp_growth' in self.data_manager.data['china']['indicators']:
                    china_gdp_growth = self.data_manager.data['china']['indicators']['gdp_growth']['value']

            if china_gdp_growth is not None and usa_rate is not None:
                if china_gdp_growth > 3 and usa_rate > 2:
                    impacts['competitive_devaluation'] = {
                        'china': 'Competitive advantage (high growth, lower rates)',
                        'usa': 'Competitive pressure',
                        'impact': 'Currency competition heating up'
                    }

        # Save analysis
        self.analysis[f"cross_impact_{datetime.now().strftime('%Y%m%d')}"] = impacts
        self.save_analysis()

        return impacts

    def analyze_global_monetary_conditions(self):
        """Analyze global monetary conditions."""
        print(f"\n💰 GLOBALNE WARUNKI MONETARNE")

        conditions = {}

        # Aggregate rate data
        major_rates = {
            'Fed': 0, 'ECB': 0, 'BOJ': 0, 'PBOC': 0
        }

        for region, data in self.data_manager.data.items():
            if 'interest_rate' in data['indicators']:
                rate = data['indicators']['interest_rate']['value']
                major_rates[region] = rate

        avg_global_rate = sum(major_rates.values()) / len(major_rates)

        # Global liquidity conditions
        if avg_global_rate > 4:
            conditions['liquidity'] = "Tight (Higher rates globally)"
        elif avg_global_rate < 1:
            conditions['liquidity'] = "Loose (Accommodative)"
        else:
            conditions['liquidity'] = "Neutral"

        # Currency strength assessment
        if major_rates['Fed'] > avg_global_rate:
            conditions['usd_strength'] = "Strong (Higher rates)"
        else:
            conditions['usd_strength'] = "Weak (Lower rates)"

        conditions['global_trend'] = "Tightening" if avg_global_rate > 2 else "Easing"

        # Save analysis
        self.analysis[f"global_monetary_{datetime.now().strftime('%Y%m%d')}"] = conditions
        self.save_analysis()

        return conditions


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
            if 'gdp_growth' in data['indicators']:
                gdp_growth = data['indicators']['gdp_growth']['value']

            if gdp_growth:
                # Project forward with noise
                noise = (random.random() * 200 - 100) / 1000  # Random noise +/- 0.1

                projected_growth = gdp_growth * (0.95 + (noise * 0.05))  # Slight adjustment

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

            with open(GLOBAL_PREDICTIONS_FILE, 'w') as f:
                json.dump(prediction_data, f, indent=2)

            print(f"✓ Przewidywania: {len(predictions)} regionów")

        return predictions

    def generate_recommendations(self):
        """Generate global investment recommendations."""
        print(f"\n💼 GLOBALNE REKOMENDACJE")

        recommendations = {
            'overall_strategy': 'DYWERSYFIKOWANY GLOBAL PORTFOLIO',
            'regional_allocations': {
                'usa': 'Underweight (Late cycle)',
                'japan': 'Overweight (Carry trade)',
                'china': 'Underweight (Slowing growth)',
                'europe': 'Underweight (Recession risk)',
                'emerging_markets': 'Equal weight (Dywersyfikacja)'
            },
            'currency_strategy': 'HEDGOWANIE SIŁY USD z JPY/EUR/CHF',
            'commodities': {
                'gold': 'Benefit z osłabnię USD, hedge inflacyjny',
                'oil': 'Ograniczenia podaży z sankcji (Iran), ryzyk geopolityczny'
            },
            'tech': {
                'us_tech': 'Overvaluation risk, zmniejsz ekspozycję',
                'chinese_tech': 'Zwolny wzrost, ale AI/konduktory są silne',
                'japanese_tech': 'Korzyść walutowa z carry trade'
            }
        }

        return recommendations


class GlobalMacroAgent:
    """Complete global macro intelligence agent."""

    def __init__(self):
        self.data_manager = GlobalMacroData()
        self.analyzer = GlobalMacroAnalyzer(self.data_manager)
        self.predictor = GlobalMacroPredictor(self.analyzer, self.data_manager)

    def collect_all_data(self, regions='all'):
        """Collect global macro data from all configured regions."""
        print("\n" + "=" * 70)
        print("GLOBAL MAKRO SYSTEM - ZBIERANIE DANYCH")
        print("=" * 70)
        print(f"Regiony: {regions}")

        # For demo, add mock data
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

        print(f"\n✓ Zebrano dane: {len(self.data_manager.data)} regionów")

    def analyze_all(self):
        """Run all analyses."""
        print("\n" + "=" * 70)
        print("GLOBAL MAKRO SYSTEM - ANALIZA")
        print("=" * 70)

        # Interest rates
        rate_analysis = self.analyzer.analyze_interest_rates()

        # Cross-country impacts
        impact_analysis = self.analyzer.analyze_cross_country_impacts()

        # Global monetary conditions
        monetary_analysis = self.analyzer.analyze_global_monetary_conditions()

        # Regional growth predictions
        growth_predictions = self.predictor.predict_regional_growth(days_ahead=90)

        # Currency impacts
        currency_analysis = self.predictor.generate_recommendations()

        # Compile report
        report = {
            'timestamp': datetime.now().isoformat(),
            'data_points': len(self.data_manager.data),
            'rate_analysis': rate_analysis,
            'impact_analysis': impact_analysis,
            'monetary_analysis': monetary_analysis,
            'currency_analysis': currency_analysis,
            'growth_predictions': growth_predictions,
            'recommendations': self.predictor.generate_recommendations()
        }

        return report

    def display_dashboard(self, report):
        """Display global macro dashboard."""
        print("\n" + "=" * 70)
        print("GLOBALNY DASHBOARD MAKRO")
        print("=" * 70)

        # Rate analysis
        print(f"\n📊 STOPY PROCENTOWE:")
        rates = report.get('rate_analysis', {})
        if rates and 'rate_differentials' in rates:
            diffs = rates['rate_differentials']
            print(f"  Fed vs JPY: {diffs.get('fed_vs_jpy', 0):+.2f}% (carry trade potential)")
            print(f"  Fed vs CNY: {diffs.get('fed_vs_cny', 0):+.2f}%")
            print(f"  Fed vs EUR: {diffs.get('fed_vs_eur', 0):+.2f}%")

        carry = rates.get('carry_trades', {})
        if carry:
            print(f"  Carry Trade: {carry.get('jpy_long', carry.get('jpy_short', 'Brak przewagi'))}")

        # Global monetary conditions
        monetary = report.get('monetary_analysis', {})
        if monetary:
            print(f"\n💰 GLOBALNE WARUNKI MONETARNE:")
            print(f"  Płynność: {monetary.get('liquidity', 'N/A')}")
            print(f"  Trend: {monetary.get('global_trend', 'N/A')}")
            print(f"  Siła USD: {monetary.get('usd_strength', 'N/A')}")

        # Growth predictions
        growth = report.get('growth_predictions', {})
        if growth and 'predictions' in growth:
            print(f"\n📈 PRZEWIDYWANIA WZROSTU (90 dni):")
            for region, pred in growth['predictions'][:4].items():
                print(f"  {region.upper()}: {pred['current_growth']:+.1f}% → {pred['projected_growth']:+.1f}% ({pred['growth_trend']})")

        # Recommendations
        recs = report.get('recommendations', {})
        if recs:
            print(f"\n💼 REKOMENDACJE INWESTYCYJNE:")
            print(f"  Strategia: {recs['overall_strategy']}")
            print(f"  Walutowa: {recs['currency_strategy']}")

            if 'commodities' in recs:
                commodities = recs['commodities']
                print(f"  Złoto: {commodities.get('gold', 'N/A')}")
                print(f"  Ropa: {commodities.get('oil', 'N/A')}")

            if 'tech' in recs:
                tech = recs['tech']
                print(f"  US Tech: {tech.get('us_tech', 'N/A')}")
                print(f"  Chiński Tech: {tech.get('chinese_tech', 'N/A')}")
                print(f"  Japoński Tech: {tech.get('japanese_tech', 'N/A')}")

            if 'regional_allocations' in recs:
                allocations = recs['regional_allocations']
                print(f"\n  Alokacje regionalne:")
                for region, alloc in allocations.items():
                    print(f"    {region.upper()}: {alloc}")

        print("\n" + "=" * 70)
        print(f"Raport zapisany: {GLOBAL_REPORT_FILE}")
        print("=" * 70)

    def run_full_analysis(self, regions='all'):
        """Run complete global macro analysis."""
        print("\n" + "=" * 70)
        print("GLOBAL MAKRO SYSTEM - PEŁNA ANALIZA")
        print("=" * 70)
        print(f"Regiony: {regions}")

        # Collect data
        self.collect_all_data(regions=regions)

        # Analyze
        report = self.analyze_all()

        # Display dashboard
        self.display_dashboard(report)

        # Save report
        with open(GLOBAL_REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n✅ Analiza zakończona!")

        return report


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("SYSTEM GLOBALNEGO MAKRO")
    print("=" * 70)
    print("Analiza: USA, Japonia, Chiny, Europa, Iran")
    print("=" * 70)

    # Initialize agent
    agent = GlobalMacroAgent()

    # Run full analysis
    report = agent.run_full_analysis(regions='all')

    print(f"\n" + "=" * 70)
    print("PLIKI:")
    print(f"  Dane makro: {GLOBAL_MACRO_FILE}")
    print(f"  Analiza: {GLOBAL_ANALYSIS_FILE}")
    print(f"  Przewidywania: {GLOBAL_PREDICTIONS_FILE}")
    print(f"  Raport: {GLOBAL_REPORT_FILE}")
    print("=" * 70)


if __name__ == '__main__':
    main()
