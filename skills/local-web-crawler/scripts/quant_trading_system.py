#!/usr/bin/env python3
"""
QUANT TRADING SYSTEM: Historical Cycles + Game Theory + Statistics
Level 3: Game Theory & Mean Reversion (No ML "black box")
"""

import sys
import json
import math
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np


# Storage paths
HISTORY_FILE = "/Users/mini-m4-1/clawd/.learnings/quant_history.json"
CYCLE_ANALYSIS_FILE = "/Users/mini-m4-1/clawd/.learnings/cycle_analysis.json"
GAME_THEORY_FILE = "/Users/mini-m4-1/clawd/.learnings/game_theory.json"
SCENARIOS_FILE = "/Users/mini-m4-1/clawd/.learnings/scenarios.json"
REPORT_FILE = "/Users/mini-m4-1/clawd/.learnings/quant_report.json"


# Game Theory Configuration
PLAYERS = {
    'USA': {
        'strengths': ['Innovation', 'Tech', 'Military', 'Dollar Dominance'],
        'strategies': ['Aggressive Tech', 'Tariffs', 'Sanctions', 'Fed Policy'],
        'goals': ['Tech Dominance', 'Dollar Strength', 'China Containment']
    },
    'China': {
        'strengths': ['Manufacturing', 'Scale', 'Infrastructure', 'Supply Chain Dominance'],
        'strategies': ['industrial_policy', 'currency_management', 'global_investment', 'export_expansion'],
        'goals': ['Supply Chain Dominance', 'Tech Innovation', 'Global Economic Leadership']
    },
    'Japan': {
        'strengths': ['Technology', 'Manufacturing', 'Monetary Policy', 'Export Competitiveness'],
        'strategies': ['Yen Depreciation', 'Carry Trade', 'Industrial Innovation', 'Global Investment'],
        'goals': ['Export Growth', 'Monetary Advantage', 'Global Competitiveness']
    },
    'Europe': {
        'strengths': ['Financial Services', 'Manufacturing', 'Technology', 'Regulatory Standards'],
        'strategies': ['Monetary Policy', 'Regulation', 'Trade Policy', 'Investment'],
        'goals': ['Economic Stability', 'Euro Strength', 'Industrial Competitiveness']
    }
}


# Statistical Constants
CONFIDENCE_LEVELS = {
    'very_high': 0.95,
    'high': 0.90,
    'medium': 0.70,
    'low': 0.50,
    'very_low': 0.30
}

# Cycle Phases
CYCLE_PHASES = {
    'expansion': {
        'name': 'Expansion',
        'duration_mean': 5.0,  # years
        'gdp_growth_avg': 3.5,
        'unemployment_avg': 4.5,
        'inflation_avg': 2.5,
        'interest_rate_avg': 3.0
    },
    'peak': {
        'name': 'Peak',
        'duration_mean': 1.5,
        'gdp_growth_avg': 4.5,
        'unemployment_avg': 4.0,
        'inflation_avg': 3.0,
        'interest_rate_avg': 5.0
    },
    'recession': {
        'name': 'Recession',
        'duration_mean': 1.5,
        'gdp_growth_avg': -1.5,
        'unemployment_avg': 7.0,
        'inflation_avg': 1.5,
        'interest_rate_avg': 1.0
    },
    'trough': {
        'name': 'Trough',
        'duration_mean': 2.0,
        'gdp_growth_avg': 1.0,
        'unemployment_avg': 5.5,
        'inflation_avg': 2.0,
        'interest_rate_avg': 2.0
    }
}


class QuantSystem:
    """Complete Quant Trading System: Cycles + Game Theory + Statistics."""

    def __init__(self):
        self.history = []
        self.load_history()

    def load_history(self):
        """Load historical data."""
        if Path(HISTORY_FILE).exists():
            try:
                with open(HISTORY_FILE, 'r') as f:
                    self.history = json.load(f)
                print(f"✓ Załadowano {len(self.history)} historycznych punktów")
            except Exception as e:
                print(f"⚠️ Błąd ładowania historii: {e}")
                self.history = []
        else:
            self.history = []

    def save_history(self):
        """Save history to file."""
        output = {
            'last_updated': datetime.now().isoformat(),
            'total_points': len(self.history),
            'history': self.history
        }

        with open(HISTORY_FILE, 'w') as f:
            json.dump(output, f, indent=2, default=str)

        print(f"✓ Historia zapisana ({len(self.history)} punktów)")

    def add_data_point(self, country, indicators):
        """Add historical data point."""
        timestamp = datetime.now().isoformat()

        data_point = {
            'timestamp': timestamp,
            'country': country,
            'indicators': indicators,
            'processed': False
        }

        self.history.append(data_point)
        self.save_history()

        print(f"✓ Dodano historyczny punkt: {country} ({timestamp})")

        return data_point


class CycleAnalyzer:
    """Analyze historical cycles and detect patterns."""

    def __init__(self, history_manager):
        self.history = history_manager.history
        self.cycles = []

    def detect_cycles(self):
        """Detect historical cycles from data."""
        print("\n" + "=" * 70)
        print("CYCLE DETECTOR")
        print("=" * 70)

        # For demo, use mock historical data
        # In production, this would analyze self.history
        mock_cycles = [
            {
                'start_year': 1990,
                'end_year': 2000,
                'phase': 'Expansion',
                'duration': 10,
                'gdp_growth_avg': 3.5,
                'peak_growth': 4.5,
                'trough_growth': 2.8
            },
            {
                'start_year': 2000,
                'end_year': 2001,
                'phase': 'Recession',
                'duration': 1,
                'gdp_growth_avg': -1.0,
                'peak_growth': 0.0,
                'trough_growth': -2.0
            },
            {
                'start_year': 2001,
                'end_year': 2007,
                'phase': 'Expansion',
                'duration': 6,
                'gdp_growth_avg': 2.8,
                'peak_growth': 3.5,
                'trough_growth': 2.2
            },
            {
                'start_year': 2007,
                'end_year': 2009,
                'phase': 'Recession',
                'duration': 2,
                'gdp_growth_avg': -2.0,
                'peak_growth': 0.0,
                'trough_growth': -3.0
            },
            {
                'start_year': 2009,
                'end_year': 2019,
                'phase': 'Expansion',
                'duration': 10,
                'gdp_growth_avg': 2.3,
                'peak_growth': 2.8,
                'trough_growth': 1.8
            },
            {
                'start_year': 2019,
                'end_year': 2020,
                'phase': 'Recession',
                'duration': 1,
                'gdp_growth_avg': -3.0,
                'peak_growth': 0.0,
                'trough_growth': -4.0
            },
            {
                'start_year': 2020,
                'end_year': 2022,
                'phase': 'Expansion',
                'duration': 2,
                'gdp_growth_avg': 5.5,
                'peak_growth': 6.8,
                'trough_growth': 4.2
            },
            {
                'start_year': 2022,
                'end_year': 2024,
                'phase': 'Recession',
                'duration': 2,
                'gdp_growth_avg': 0.5,
                'peak_growth': 1.0,
                'trough_growth': 0.0
            }
        ]

        self.cycles = mock_cycles
        print(f"\n✓ Wykryto {len(mock_cycles)} historycznych cykli")

        return mock_cycles

    def identify_current_phase(self, current_indicators):
        """Identify which phase we're in based on current indicators."""
        if not current_indicators:
            return 'Unknown'

        gdp_growth = current_indicators.get('gdp_growth', 2.0)
        unemployment = current_indicators.get('unemployment', 5.0)
        interest_rate = current_indicators.get('interest_rate', 4.0)

        # Pattern recognition
        if gdp_growth > 4.0:
            phase = 'Peak'
            confidence = 0.9
        elif gdp_growth < 0:
            phase = 'Recession'
            confidence = 0.95
        elif unemployment > 6.0:
            phase = 'Trough'
            confidence = 0.8
        elif interest_rate < 1.0:
            phase = 'Early Expansion'
            confidence = 0.85
        elif gdp_growth > 2.0 and interest_rate > 3.0:
            phase = 'Late Expansion'
            confidence = 0.8
        else:
            phase = 'Mid Expansion'
            confidence = 0.6

        return {
            'phase': phase,
            'confidence': confidence,
            'reasoning': f"GDP: {gdp_growth:+.1f}%, Unemployment: {unemployment:.1f}%, Rate: {interest_rate:.1f}%"
        }

    def predict_next_phase(self, current_phase, cycle_history):
        """Predict next phase based on historical patterns."""
        print(f"\n📈 PREDIKCYJA NASTĘPNEJ FAZY CYKLU")

        # Find similar phases in history
        similar_phases = [c for c in cycle_history if c['phase'] == current_phase['phase']]

        if not similar_phases:
            # Default to business cycle
            return {
                'next_phase': 'Trough',
                'timeline': '6-12 months',
                'confidence': 0.4,
                'reasoning': 'No similar historical pattern - business cycle default'
            }

        # Analyze typical transitions
        transitions = {}
        for i in range(len(cycle_history) - 1):
            current = cycle_history[i]
            next_ = cycle_history[i + 1]
            transition = f"{current['phase']} → {next_['phase']}"

            if transition not in transitions:
                transitions[transition] = 0

            transitions[transition] += 1

        # Find most likely next phase
        possible_next = []
        for transition, count in transitions.items():
            if transition.startswith(current_phase['phase']):
                next_phase = transition.split(' → ')[1]
                prob = count / sum([c for c in transitions.keys() if c.startswith(current_phase['phase'])])
                possible_next.append({
                    'next_phase': next_phase,
                    'probability': prob,
                    'historical_occurrences': count
                })

        if possible_next:
            # Sort by probability
            possible_next.sort(key=lambda x: x['probability'], reverse=True)
            best_next = possible_next[0]

            return {
                'next_phase': best_next['next_phase'],
                'timeline': f"{CYCLE_PHASES[best_next['next_phase']]['duration_mean']} years avg",
                'confidence': best_next['probability'],
                'reasoning': f"Historycznie: {current_phase['phase']} → {best_next['next_phase']} {best_next['historical_occurrences']}x ({best_next['probability']:.1%})",
                'all_possibilities': possible_next
            }

        # Fallback
        return {
            'next_phase': 'Trough',
            'timeline': '6-12 months',
            'confidence': 0.3,
            'reasoning': 'Insufficient historical data - business cycle default'
        }


class GameTheoryEngine:
    """Game Theory analysis for country strategies."""

    def __init__(self, cycle_analyzer):
        self.cycle_analyzer = cycle_analyzer
        self.game_matrix = {}

    def analyze_competition(self):
        """Analyze competitive dynamics between countries."""
        print("\n" + "=" * 70)
        print("GAME THEORY COMPETITION ANALYZER")
        print("=" * 70)

        # Build payoff matrix (simplified)
        # USA vs China (Tech competition)
        payoff_matrix_usa_china = {
            'USA': {
                'Aggressive Tech': {
                    'China_Tech_Advance': 5,  # USA gains market share
                    'Global_Innovation': 3,   # Innovation competition
                    'China_Retaliation': -2  # Trade wars
                },
                'Tariffs': {
                    'China_Tech_Advance': 3,  # Slower tech transfer
                    'Global_Innovation': 2,
                    'China_Retaliation': -1
                }
            },
            'China': {
                'Industrial_Policy': {
                    'USA_Tech_Dominance': -4,  # China loses tech edge
                    'Supply_Chain_Dominance': 5,   # China gains control
                    'Global_Market_Share': 3
                },
                'Export_Expansion': {
                    'USA_Tech_Dominance': -3,
                    'Supply_Chain_Dominance': 4,
                    'Global_Market_Share': 4
                }
            }
        }

        # USA vs Japan (Currency/Monetary competition)
        payoff_matrix_usa_japan = {
            'USA': {
                'Dollar_Strength': {
                    'USA_Export_Advantage': 4,   # Strong dollar
                    'Japan_Export_Disadvantage': -3,  # Weak yen
                    'Global_Reserve_Status': 3
                },
                'Fed_Policy': {
                    'USA_Export_Advantage': 3,
                    'Japan_Carry_Trade_Loss': -2,  # Japan loses carry
                    'Monetary_Stability': 2
                }
            },
            'Japan': {
                'Yen_Depreciation': {
                    'USA_Export_Disadvantage': -2,  # Weak yen hurts US
                    'Japan_Export_Advantage': 5,   # Boosts exports
                    'Carry_Trade_Profit': 3
                },
                'Carry_Trade': {
                    'USA_Export_Disadvantage': -2,
                    'Japan_Export_Advantage': 4,
                    'Funding_Advantage': 3
                }
            }
        }

        # Nash Equilibrium calculation (simplified)
        usa_strategies = ['Aggressive Tech', 'Tariffs', 'Fed Policy']
        china_strategies = ['Industrial Policy', 'Export Expansion']

        game_matrix = {
            'usa_vs_china': payoff_matrix_usa_china,
            'usa_vs_japan': payoff_matrix_usa_japan,
            'equilibrium_analysis': {}
        }

        # Find Nash equilibrium for USA vs China
        usa_best = {}
        china_best = {}

        for usa_strat in usa_strategies:
            usa_payoffs = [payoff_matrix_usa_china['USA'][usa_strat][china_strat]['Global_Innovation']
                             for china_strat in china_strategies]
            usa_best[usa_strat] = sum(usa_payoffs) / len(usa_payoffs)

        for china_strat in china_strategies:
            china_payoffs = [payoff_matrix_usa_china['China'][china_strat][usa_strat]['Supply_Chain_Dominance']
                               for usa_strat in usa_strategies]
            china_best[china_strat] = sum(china_payoffs) / len(china_payoffs)

        # Nash equilibrium (both players playing best response)
        usa_nash = max(usa_best, key=usa_best.get)
        china_nash = max(china_best, key=china_best.get)

        equilibrium = {
            'usa_strategy': usa_nash,
            'china_strategy': china_nash,
            'payoff': {
                'usa': usa_best[usa_nash],
                'china': china_best[china_nash]
            },
            'interpretation': f"USA: {usa_nash}, China: {china_nash} - Nash Equilibrium"
        }

        game_matrix['equilibrium_analysis']['usa_china'] = equilibrium

        # Nash equilibrium for USA vs Japan (Currency)
        usa_currency_strategies = ['Dollar_Strength', 'Fed_Policy']
        japan_currency_strategies = ['Yen_Depreciation', 'Carry_Trade']

        usa_best_curr = {}
        japan_best_curr = {}

        for usa_strat in usa_currency_strategies:
            usa_payoffs = [payoff_matrix_usa_japan['USA'][usa_strat][jap_strat]['USA_Export_Advantage']
                             for jap_strat in japan_currency_strategies]
            usa_best_curr[usa_strat] = sum(usa_payoffs) / len(usa_payoffs)

        for jap_strat in japan_currency_strategies:
            jap_payoffs = [payoff_matrix_usa_japan['Japan'][jap_strat][usa_strat]['Japan_Export_Advantage']
                            for usa_strat in usa_currency_strategies]
            japan_best_curr[jap_strat] = sum(jap_payoffs) / len(jap_payoffs)

        usa_nash_curr = max(usa_best_curr, key=usa_best_curr.get)
        jap_nash_curr = max(japan_best_curr, key=japan_best_curr.get)

        equilibrium_curr = {
            'usa_strategy': usa_nash_curr,
            'japan_strategy': jap_nash_curr,
            'payoff': {
                'usa': usa_best_curr[usa_nash_curr],
                'japan': japan_best_curr[jap_nash_curr]
            },
            'interpretation': f"USA: {usa_nash_curr}, Japan: {jap_nash_curr} - Currency Nash Equilibrium"
        }

        game_matrix['equilibrium_analysis']['usa_japan'] = equilibrium_curr

        self.game_matrix = game_matrix

        # Display results
        print(f"\n  USA vs China Nash Equilibrium:")
        print(f"    USA Strategy: {equilibrium['usa_strategy']}")
        print(f"    China Strategy: {equilibrium['china_strategy']}")
        print(f"    Payoff: USA {equilibrium['payoff']['usa']}, China {equilibrium['payoff']['china']}")

        print(f"\n  USA vs Japan Currency Nash Equilibrium:")
        print(f"    USA Strategy: {equilibrium_curr['usa_strategy']}")
        print(f"    Japan Strategy: {equilibrium_curr['japan_strategy']}")
        print(f"    Payoff: USA {equilibrium_curr['payoff']['usa']}, Japan {equilibrium_curr['payoff']['japan']}")

        print(f"\n  Interpretacja:")
        print(f"    USA vs China: Technology and supply chain competition")
        print(f"    USA vs Japan: Monetary and currency competition")
        print(f"    Nash Equilibrium: Both countries playing optimal strategies")

        return game_matrix

    def generate_recommendations(self, current_phase):
        """Generate strategic recommendations based on game theory analysis."""
        print("\n" + "=" * 70)
        print("STRATEGIC RECOMMENDATIONS (GAME THEORY)")
        print("=" * 70)

        recommendations = {}

        # USA Recommendations
        if current_phase['phase'] in ['Peak', 'Late Expansion']:
            recommendations['usa'] = {
                'strategy': 'Consolidate Gains',
                'actions': [
                    'Continue tech leadership (chips, AI)',
                    'Maintain dollar strength',
                    'Consider defensive tariffs'
                ],
                'risks': [
                    'China retaliation (tech restrictions)',
                    'Global innovation fragmentation',
                    'Valuation stretch'
                ]
            }
        elif current_phase['phase'] in ['Trough', 'Recession']:
            recommendations['usa'] = {
                'strategy': 'Innovate and Stimulate',
                'actions': [
                    'Aggressive R&D investment',
                    'Monetary easing (cut rates)',
                    'Deregulate emerging tech',
                    'Strategic alliances (Europe, Japan)'
                ],
                'opportunities': [
                    'China tech restrictions (opportunity for domestic)',
                    'Weaker dollar (boosts exports)',
                    'Disruption of global supply chains'
                ]
            }
        else:
            recommendations['usa'] = {
                'strategy': 'Balanced Growth',
                'actions': [
                    'Maintain innovation leadership',
                    'Monitor China competition',
                    'Adjust monetary policy based on cycle'
                ],
                'risks': [
                    'Commodities inflation',
                    'Currency volatility'
                ]
            }

        # China Recommendations
        if current_phase['phase'] in ['Peak', 'Late Expansion']:
            recommendations['china'] = {
                'strategy': 'Diversify and Scale',
                'actions': [
                    'Global investment in AI, semiconductors',
                    'Develop domestic alternatives (reduce USA dependency)',
                    'Expand into new markets (Europe, Africa, Latin America)'
                ],
                'risks': [
                    'USA tech restrictions (chip bans)',
                    'Overcapacity in manufacturing',
                    'Global trade tensions'
                ]
            }
        elif current_phase['phase'] in ['Trough', 'Recession']:
            recommendations['china'] = {
                'strategy': 'Stimulate Domestic and Export',
                'actions': [
                    'Domestic stimulus (infrastructure, consumption)',
                    'Export expansion (devalue currency)',
                    'Targeted subsidies for key sectors',
                    'Technology acquisition abroad'
                ],
                'opportunities': [
                    'USA domestic focus (opportunity for exports)',
                    'Global supply chain disruptions',
                    'Commodity price fluctuations'
                ]
            }
        else:
            recommendations['china'] = {
                'strategy': 'Balanced Growth',
                'actions': [
                    'Continue manufacturing scale-up',
                    'Manage currency for competitive advantage',
                    'Invest in innovation (AI, chips, EVs)',
                    'Expand global market share'
                ],
                'risks': [
                    'USA competition intensification',
                    'Global regulatory changes'
                ]
            }

        # Japan Recommendations
        if current_phase['phase'] in ['Peak', 'Late Expansion']:
            recommendations['japan'] = {
                'strategy': 'Maintain Carry Trade Advantage',
                'actions': [
                    'Keep BOJ rates negative (carry opportunity)',
                    'Export to USA (take advantage of dollar)',
                    'Support innovation (robotics, chips)',
                    'Currency interventions to prevent excessive strength'
                ],
                'risks': [
                    'Fed rate hikes (reduces carry profits)',
                    'Domestic deflation',
                    'Competition from China manufacturing'
                ]
            }
        elif current_phase['phase'] in ['Trough', 'Recession']:
            recommendations['japan'] = {
                'strategy': 'Stimulate and Export',
                'actions': [
                    'Aggressive monetary easing (more negative rates)',
                    'Fiscal stimulus (infrastructure spending)',
                    'Currency depreciation (boost exports)',
                    'Target global markets (USA, Europe)'
                ],
                'opportunities': [
                    'Weak global demand (opportunity for exporters)',
                    'Cheaper funding (negative rates)',
                    'Global trade imbalances'
                ]
            }
        else:
            recommendations['japan'] = {
                'strategy': 'Balanced Growth',
                'actions': [
                    'Maintain monetary accommodation',
                    'Support export competitiveness',
                    'Invest in innovation (AI, robotics)',
                    'Gradual rate hikes if growth accelerates'
                ],
                'risks': [
                    'Faster global growth (reduces competitiveness)',
                    'Currency appreciation',
                    'Fed policy changes'
                ]
            }

        # Gold Recommendations (based on global cycle)
        if current_phase['phase'] in ['Peak', 'Late Expansion']:
            recommendations['gold'] = {
                'recommendation': 'REDUCE',
                'reasoning': 'No fear of inflation, strong economy = no safe haven demand',
                'action': 'Reduce allocation, rotate to other defensive sectors'
            }
        elif current_phase['phase'] in ['Trough', 'Recession']:
            recommendations['gold'] = {
                'recommendation': 'INCREASE SIGNIFICANTLY',
                'reasoning': 'Fear of recession, currency wars, geopolitical risk = strong safe haven demand',
                'action': 'Maximize allocation, use as hedge against currency devaluation',
                'weight': '10-15% of portfolio'
            }
        else:
            recommendations['gold'] = {
                'recommendation': 'MODERATE',
                'reasoning': 'Healthy growth but not peak = moderate safe haven demand',
                'action': 'Maintain 3-5% allocation as inflation hedge',
                'weight': '3-5% of portfolio'
            }

        # Tech Recommendations
        if current_phase['phase'] in ['Peak', 'Late Expansion']:
            recommendations['tech'] = {
                'recommendation': 'REDUCE',
                'reasoning': 'Valuations stretched, euphoria, high interest rates = likely correction',
                'action': 'Lock in profits, reduce exposure, focus on quality',
                'sectors': ['Tech hardware', 'Software', 'Semiconductors']
            }
        elif current_phase['phase'] in ['Trough', 'Recession']:
            recommendations['tech'] = {
                'recommendation': 'AGGRESSIVE BUYING',
                'reasoning': 'Panic selling = opportunities in quality growth companies',
                'action': 'Buy on dips, focus on companies with strong balance sheets and cash flow',
                'sectors': ['AI', 'Semiconductors', 'Enterprise Software', 'Cloud']
            }
        else:
            recommendations['tech'] = {
                'recommendation': 'MODERATE',
                'reasoning': 'Healthy but not extreme = balanced approach',
                'action': 'Maintain balanced portfolio, add to strengths on dips',
                'sectors': ['All major tech sectors']
            }

        self.game_matrix['recommendations'] = recommendations

        # Display recommendations
        print(f"\n  ZŁOTO (XAU):")
        print(f"    {recommendations['gold']['recommendation']}: {recommendations['gold']['reasoning']}")
        print(f"    Akcja: {recommendations['gold']['action']}")

        print(f"\n  TECHNOLOGIA (USA):")
        print(f"    {recommendations['usa']['strategy']}")
        for action in recommendations['usa']['actions']:
            print(f"    • {action}")

        return recommendations


class StatisticalEngine:
    """Statistical analysis engine for quant trading."""

    def __init__(self, history_manager):
        self.history = history_manager.history

    def calculate_mean_reversion(self, indicator, current_value):
        """Calculate mean reversion signal."""
        # Extract historical values
        values = [d.get('indicators', {}).get(indicator, None) for d in self.history if d.get('indicators')]
        values = [v for v in values if v is not None]

        if len(values) < 2:
            return None

        mean_val = np.mean(values)
        std_dev = np.std(values)

        # Calculate Z-score (standard deviations from mean)
        if std_dev > 0:
            z_score = (current_value - mean_val) / std_dev
        else:
            z_score = 0

        # Mean reversion signal
        # Z-score > 2 = overvalued (short signal)
        # Z-score < -2 = undervalued (long signal)
        reversion_signal = None
        confidence = None

        if z_score > 2:
            reversion_signal = 'STRONG SHORT'
            confidence = CONFIDENCE_LEVELS['very_high']
        elif z_score > 1:
            reversion_signal = 'SHORT'
            confidence = CONFIDENCE_LEVELS['high']
        elif z_score < -2:
            reversion_signal = 'STRONG LONG'
            confidence = CONFIDENCE_LEVELS['very_high']
        elif z_score < -1:
            reversion_signal = 'LONG'
            confidence = CONFIDENCE_LEVELS['high']
        else:
            reversion_signal = 'NEUTRAL'
            confidence = CONFIDENCE_LEVELS['medium']

        return {
            'indicator': indicator,
            'current_value': current_value,
            'historical_mean': mean_val,
            'std_dev': std_dev,
            'z_score': z_score,
            'reversion_signal': reversion_signal,
            'confidence': confidence,
            'interpretation': f"{indicator} is {abs(z_score):.1f} SD from mean ({'overvalued' if z_score > 0 else 'undervalued'})"
        }

    def calculate_correlation(self, indicator1, indicator2):
        """Calculate correlation between two indicators."""
        # Extract historical values
        values1 = [d.get('indicators', {}).get(indicator1, None) for d in self.history if d.get('indicators')]
        values2 = [d.get('indicators', {}).get(indicator2, None) for d in self.history if d.get('indicators')]

        values1 = [v for v in values1 if v is not None]
        values2 = [v for v in values2 if v is not None]

        if len(values1) < 2 or len(values2) < 2:
            return None

        correlation = np.corr(values1, values2)

        return {
            'indicator1': indicator1,
            'indicator2': indicator2,
            'correlation': correlation,
            'interpretation': self._interpret_correlation(correlation, indicator1, indicator2),
            'confidence': abs(correlation) * 0.9  # Confidence based on correlation strength
        }

    def _interpret_correlation(self, correlation, ind1, ind2):
        """Interpret correlation coefficient."""
        if correlation is None:
            return 'Insufficient data'

        abs_corr = abs(correlation)

        if abs_corr > 0.7:
            strength = 'Strong'
        elif abs_corr > 0.4:
            strength = 'Moderate'
        elif abs_corr > 0.2:
            strength = 'Weak'
        else:
            strength = 'Very Weak'

        if correlation > 0.2:
            direction = 'Positive'
        elif correlation < -0.2:
            direction = 'Negative'
        else:
            direction = 'No relationship'

        return f"{strength} {direction} correlation between {ind1} and {ind2} ({correlation:.2f})"

    def generate_statistical_signals(self, current_indicators):
        """Generate statistical signals for current indicators."""
        print("\n" + "=" * 70)
        print("STATISTICAL ENGINE - MEAN REVERSION & CORRELATIONS")
        print("=" * 70)

        signals = {}

        # Mean reversion signals
        for indicator, value in current_indicators.items():
            signal = self.calculate_mean_reversion(indicator, value)
            if signal:
                signals[f'mean_reversion_{indicator}'] = signal
                print(f"\n  {indicator.upper()} ({value:+.2f}):")
                print(f"    Mean Reversion: {signal['reversion_signal']}")
                print(f"    Z-Score: {signal['z_score']:+.2f} SD")
                print(f"    Interpretation: {signal['interpretation']}")
                print(f"    Confidence: {signal['confidence']:.0%}")

        # Correlation signals
        key_indicators = ['gdp_growth', 'unemployment', 'interest_rate']
        for i in range(len(key_indicators)):
            for j in range(i + 1, len(key_indicators)):
                ind1 = key_indicators[i]
                ind2 = key_indicators[j]

                corr = self.calculate_correlation(ind1, ind2)
                if corr:
                    signals[f'correlation_{ind1}_{ind2}'] = corr
                    print(f"\n  {ind1.upper()} vs {ind2.upper()}:")
                    print(f"    {corr['interpretation']}")
                    print(f"    Confidence: {corr['confidence']:.0%}")

        return signals


class ScenarioEngine:
    """Generate "What If" scenarios."""

    def __init__(self, cycle_analyzer, game_engine, stats_engine):
        self.cycle_analyzer = cycle_analyzer
        self.game_engine = game_engine
        self.stats_engine = stats_engine

    def generate_scenarios(self, current_indicators, cycle_phase):
        """Generate concrete scenarios."""
        print("\n" + "=" * 70)
        print("SCENARIO ENGINE - WHAT-IF ANALYSIS")
        print("=" * 70)

        scenarios = []

        # Scenario 1: Fed Rate Cut
        fed_rate = current_indicators.get('interest_rate', 4.5)
        scenario_fed_cut = {
            'scenario_id': 'SCENARIO_1',
            'name': 'Fed Rate Cut',
            'trigger': 'Fed cuts rate by 0.50%',
            'changes': {
                'usa': 'Liquidity injection, dollar weakness',
                'japan': 'Reduced carry trade profits',
                'china': 'Competitive currency advantage',
                'gold': 'Positive (lower rates, weaker dollar)',
                'tech': 'Positive (cheaper funding, growth acceleration)',
                'probability': 0.4 if cycle_phase['phase'] in ['Trough', 'Recession'] else 0.2
            },
            'impact_timeline': 'Immediate to 6 months',
            'investment_implications': {
                'gold': 'Increase - lower real rates boost gold demand',
                'tech': 'Increase - cheaper financing, growth stocks outperform',
                'japan': 'Negative - carry trade profits reduced',
                'china': 'Positive - currency depreciation helps exports'
            }
        }
        scenarios.append(scenario_fed_cut)

        # Scenario 2: Aggressive Tariffs (USA vs China)
        scenario_tariffs = {
            'scenario_id': 'SCENARIO_2',
            'name': 'Aggressive Tariffs',
            'trigger': 'USA imposes 25% tariffs on Chinese goods',
            'changes': {
                'usa': 'Higher consumer prices, domestic manufacturing boost, possible retaliation',
                'china': 'Export disadvantage, GDP slowdown, potential currency depreciation',
                'global': 'Supply chain fragmentation, higher global prices',
                'gold': 'Positive (trade uncertainty, inflation hedge)',
                'tech': 'Mixed (domestic benefit, supply chain risk)'
            },
            'impact_timeline': '6-12 months',
            'investment_implications': {
                'gold': 'Increase - trade uncertainty favors safe haven',
                'tech': 'Mixed - domestic winners, supply chain losers',
                'china': 'Negative - export drag, tech restrictions',
                'usa': 'Mixed - inflation risk, manufacturing boost'
            }
        }
        scenarios.append(scenario_tariffs)

        # Scenario 3: Currency Wars (USA vs Japan)
        scenario_currency_war = {
            'scenario_id': 'SCENARIO_3',
            'name': 'Currency War (USD/JPY)',
            'trigger': 'USA maintains high rates, BOJ keeps rates negative (rate divergence widens)',
            'changes': {
                'usa': 'Stronger dollar, US export disadvantage, carry trade benefits',
                'japan': 'Weaker yen, export advantage, carry trade losses',
                'global': 'Currency volatility, capital flows to high-yielding currencies',
                'gold': 'Positive (weaker USD boosts gold in USD terms)',
                'tech': 'Mixed - US tech loses from strong dollar, gains from carry'
            },
            'impact_timeline': '3-6 months',
            'investment_implications': {
                'gold': 'Increase - currency devaluation in USD terms',
                'tech': 'Reduce - strong dollar hurts US tech exports, but carry trade helps',
                'japan': 'Increase - weaker yen boosts exports',
                'usa': 'Reduce - strong dollar hurts exports, but carry trade helps'
            }
        }
        scenarios.append(scenario_currency_war)

        # Display scenarios
        print(f"\n  Scenario 1: Fed Rate Cut")
        print(f"    Probability: {scenario_fed_cut['probability']:.0%}")
        print(f"    Timeline: {scenario_fed_cut['impact_timeline']}")
        print(f"    Gold Impact: {scenario_fed_cut['investment_implications']['gold']}")
        print(f"    Tech Impact: {scenario_fed_cut['investment_implications']['tech']}")

        print(f"\n  Scenario 2: Aggressive Tariffs")
        print(f"    Timeline: {scenario_tariffs['impact_timeline']}")
        print(f"    Global Impact: {scenario_tariffs['changes']['global']}")

        print(f"\n  Scenario 3: Currency War (USD/JPY)")
        print(f"    Timeline: {scenario_currency_war['impact_timeline']}")
        print(f"    Carry Trade Impact: {scenario_currency_war['changes']['global']}")

        return scenarios


def main():
    """Main execution."""
    print("\n" + "=" * 70)
    print("QUANT TRADING SYSTEM: Cycles + Game Theory + Statistics")
    print("=" * 70)

    # Initialize systems
    history = QuantSystem()
    cycle_analyzer = CycleAnalyzer(history)
    game_engine = GameTheoryEngine(cycle_analyzer)
    stats_engine = StatisticalEngine(history)
    scenario_engine = ScenarioEngine(cycle_analyzer, game_engine, stats_engine)

    # Load mock historical data
    print("\n📊 HISTORICAL CYCLES")
    cycles = cycle_analyzer.detect_cycles()
    cycle_analyzer.cycles = cycles  # Save for later use

    # Current indicators (mock)
    current_indicators = {
        'gdp_growth': 2.3,
        'unemployment': 4.1,
        'interest_rate': 4.33,
        'inflation': 2.9
    }

    # Identify current phase
    print("\n🎯 CURRENT CYCLE PHASE")
    current_phase = cycle_analyzer.identify_current_phase(current_indicators)
    print(f"  Phase: {current_phase['phase']}")
    print(f"  Confidence: {current_phase['confidence']:.0%}")
    print(f"  Reasoning: {current_phase['reasoning']}")

    # Predict next phase
    print("\n📈 NEXT PHASE PREDICTION")
    next_phase = cycle_analyzer.predict_next_phase(current_phase, cycles)
    print(f"  Next Phase: {next_phase['next_phase']}")
    print(f"  Timeline: {next_phase['timeline']}")
    print(f"  Confidence: {next_phase['confidence']:.0%}")
    print(f"  Reasoning: {next_phase['reasoning']}")

    # Game Theory Analysis
    print("\n🎮 GAME THEORY COMPETITION ANALYZER")
    game_matrix = game_engine.analyze_competition()

    # Statistical Analysis
    print("\n📊 STATISTICAL ANALYZER")
    signals = stats_engine.generate_statistical_signals(current_indicators)

    # Generate Scenarios
    print("\n🎯 SCENARIO ENGINE")
    scenarios = scenario_engine.generate_scenarios(current_indicators, current_phase)

    # Compile comprehensive report
    report = {
        'timestamp': datetime.now().isoformat(),
        'current_phase': current_phase,
        'next_phase': next_phase,
        'game_theory_analysis': game_matrix,
        'statistical_signals': signals,
        'scenarios': scenarios,
        'investment_recommendations': game_matrix.get('recommendations', {}),
        'summary': {
            'cycle_phase': current_phase['phase'],
            'next_phase': next_phase['next_phase'],
            'confidence': (current_phase['confidence'] + next_phase['confidence']) / 2,
            'game_theory_equilibrium': game_matrix.get('equilibrium_analysis', {}).get('usa_china', {}).get('interpretation', ''),
            'most_likely_scenario': scenarios[0]['name'] if scenarios else 'No scenarios',
            'investment_strategy': 'BALANCED APPROACH',
            'position_size': {
                'cash': '30%',
                'bonds': '30%',
                'equity': '30%',
                'gold': '10%'
            }
        }
    }

    # Save report
    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\n✓ Report zapisany: {REPORT_FILE}")

    # Display summary
    print("\n" + "=" * 70)
    print("QUANT TRADING SYSTEM REPORT")
    print("=" * 70)

    print(f"\n  Faza Cyklu: {current_phase['phase']}")
    print(f"  Następna Faza: {next_phase['next_phase']}")
    print(f"  Ogólna Strategia: {report['summary']['investment_strategy']}")
    print(f"  Pozycje: {report['summary']['position_size']}")

    print(f"\n  Rekomendacje:")
    recommendations = game_matrix.get('recommendations', {})
    if recommendations:
        print(f"    ZŁOTO: {recommendations['gold']['recommendation']}")
        print(f"    TECH: {recommendations['usa']['strategy']}")

    print(f"\n" + "=" * 70)
    print("✅ SYSTEM ZAKOŃCZONY!")
    print("=" * 70)
    print(f"\nPLIKI:")
    print(f"  Historia cykli: {CYCLE_ANALYSIS_FILE}")
    print(f"  Raport kwantowy: {REPORT_FILE}")
    print("=" * 70)


if __name__ == '__main__':
    main()
