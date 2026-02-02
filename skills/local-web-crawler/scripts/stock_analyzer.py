#!/usr/bin/env python3
"""
Simple stock analyzer using yfinance.
Usage: python3 stock_analyzer.py <ticker> [period] [interval]
Example: python3 stock_analyzer.py AAPL 1y 1d
"""

import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def get_stock_data(ticker, period="1y", interval="1d"):
    """Fetch stock data from yfinance."""
    print(f"Fetching {ticker} data ({period}, {interval})...")

    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        print(f"No data found for {ticker}")
        return None, None

    # Get company info
    info = stock.info

    return data, info


def calculate_metrics(data):
    """Calculate basic technical metrics."""
    if data is None or data.empty:
        return {}

    # Basic metrics
    latest_price = data['Close'].iloc[-1]
    price_change = data['Close'].pct_change().iloc[-1] * 100
    price_change_abs = data['Close'].iloc[-1] - data['Close'].iloc[0]

    # Moving averages
    ma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    ma_200 = data['Close'].rolling(window=200).mean().iloc[-1]

    # Volatility (20-day standard deviation)
    volatility = data['Close'].pct_change().rolling(window=20).std().iloc[-1] * 100

    # RSI (simplified 14-day)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return {
        'latest_price': latest_price,
        'price_change_pct': price_change,
        'price_change_abs': price_change_abs,
        'ma_50': ma_50 if not pd.isna(ma_50) else None,
        'ma_200': ma_200 if not pd.isna(ma_200) else None,
        'volatility_20d': volatility if not pd.isna(volatility) else None,
        'rsi_14': rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else None,
        'volume_avg': data['Volume'].mean()
    }


def analyze_sentiment(metrics, info):
    """Simple sentiment analysis based on metrics."""
    sentiment = []

    if metrics.get('ma_50') and metrics['latest_price'] > metrics['ma_50']:
        sentiment.append("✅ Above 50-day MA (bullish)")
    else:
        sentiment.append("❌ Below 50-day MA (bearish)")

    if metrics.get('ma_200') and metrics['latest_price'] > metrics['ma_200']:
        sentiment.append("✅ Above 200-day MA (long-term bullish)")
    else:
        sentiment.append("❌ Below 200-day MA (long-term bearish)")

    if metrics.get('rsi_14'):
        if metrics['rsi_14'] > 70:
            sentiment.append(f"⚠️ RSI {metrics['rsi_14']:.1f} (overbought)")
        elif metrics['rsi_14'] < 30:
            sentiment.append(f"⚠️ RSI {metrics['rsi_14']:.1f} (oversold)")
        else:
            sentiment.append(f"✅ RSI {metrics['rsi_14']:.1f} (neutral)")

    if metrics.get('volatility_20d'):
        if metrics['volatility_20d'] > 5:
            sentiment.append(f"⚠️ High volatility ({metrics['volatility_20d']:.2f}%)")
        else:
            sentiment.append(f"✅ Low volatility ({metrics['volatility_20d']:.2f}%)")

    return sentiment


def display_results(ticker, data, info, metrics):
    """Display analysis results."""
    print("\n" + "=" * 70)
    print(f"STOCK ANALYSIS: {ticker}")
    print("=" * 70)

    # Company info
    if info:
        print(f"\nCompany: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 0) / 1e9:.2f}B")

    # Price data
    print(f"\nCurrent Price: ${metrics['latest_price']:.2f}")
    print(f"Change: {metrics['price_change_abs']:+.2f} ({metrics['price_change_pct']:+.2f}%)")

    # Technical metrics
    print(f"\nTechnical Indicators:")
    if metrics.get('ma_50'):
        print(f"  50-day MA: ${metrics['ma_50']:.2f}")
    if metrics.get('ma_200'):
        print(f"  200-day MA: ${metrics['ma_200']:.2f}")
    if metrics.get('volatility_20d'):
        print(f"  20-day Volatility: {metrics['volatility_20d']:.2f}%")
    if metrics.get('rsi_14'):
        print(f"  14-day RSI: {metrics['rsi_14']:.1f}")

    # Sentiment
    print(f"\nSentiment:")
    for item in analyze_sentiment(metrics, info):
        print(f"  {item}")

    # Fundamental data (if available)
    if info:
        print(f"\nFundamentals:")
        print(f"  P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"  EPS: ${info.get('trailingEps', 'N/A')}")
        print(f"  Dividend Yield: {info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 'N/A':.2f}%")


def plot_chart(ticker, data, save_path=None):
    """Plot price chart with moving averages."""
    plt.figure(figsize=(12, 6))

    # Price
    plt.plot(data.index, data['Close'], label='Price', linewidth=2)

    # Moving averages
    if len(data) >= 50:
        ma_50 = data['Close'].rolling(window=50).mean()
        plt.plot(data.index, ma_50, label='50-day MA', alpha=0.7)

    if len(data) >= 200:
        ma_200 = data['Close'].rolling(window=200).mean()
        plt.plot(data.index, ma_200, label='200-day MA', alpha=0.7)

    plt.title(f'{ticker} Price Chart')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"\nChart saved to {save_path}")
    else:
        plt.show()

    plt.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 stock_analyzer.py <ticker> [period] [interval]", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python3 stock_analyzer.py AAPL 1y 1d", file=sys.stderr)
        print("  python3 stock_analyzer.py TSLA 6mo 1h", file=sys.stderr)
        print("  python3 stock_analyzer.py BTC-USD 1mo 1d", file=sys.stderr)
        sys.exit(1)

    ticker = sys.argv[1].upper()
    period = sys.argv[2] if len(sys.argv) > 2 else "1y"
    interval = sys.argv[3] if len(sys.argv) > 3 else "1d"

    try:
        # Fetch data
        data, info = get_stock_data(ticker, period, interval)

        if data is None:
            sys.exit(1)

        # Calculate metrics
        metrics = calculate_metrics(data)

        # Display results
        display_results(ticker, data, info, metrics)

        # Plot chart
        chart_path = f"/Users/mini-m4-1/clawd/{ticker}_chart.png"
        plot_chart(ticker, data, chart_path)

        print("\n" + "=" * 70)
        print("Analysis complete! ✅")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
