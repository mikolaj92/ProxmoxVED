# Open Source Investment Analysis Tools

List of free, open-source tools for financial analysis and trading.

## 📊 Trading Platforms (Bloomberg Terminal Alternatives)

### 1. **QuantConnect** (Python)
- **Stars**: ~15k
- **URL**: https://github.com/QuantConnect/Lean
- **Description**: Open-source algorithmic trading engine
- **Features**:
  - Live and historical data
  - Multi-asset backtesting
  - Python/C# algorithms
  - Cloud and self-hosted options
- **Use case**: Quantitative trading, backtesting

### 2. **Backtrader** (Python)
- **Stars**: ~12k
- **URL**: https://github.com/mementum/backtrader
- **Description**: Backtesting library with live trading
- **Features**:
  - Pandas integration
  - Multiple data sources
  - Visual plotting
  - Strategy development
- **Use case**: Strategy backtesting, paper trading

### 3. **VectorBT** (Python)
- **Stars**: ~2.5k
- **URL**: https://github.com/polakowo/vectorbt
- **Description**: Vectorized backtesting with Numba
- **Features**:
  - Super fast (vectorized)
  - 80+ indicators
  - Portfolio optimization
  - Event-driven backtesting
- **Use case**: High-performance backtesting

### 4. **Zipline** (Python)
- **Stars**: ~16k (archived)
- **URL**: https://github.com/quantopian/zipline
- **Description**: Historical backtesting from Quantopian
- **Status**: Archived but still used
- **Use case**: Classic algorithmic trading

## 📈 Data Analysis Tools

### 1. **FinPy** (Python)
- **Stars**: ~8k
- **URL**: https://github.com/radinformatic/finpy
- **Description**: Financial data analysis toolkit
- **Features**:
  - Technical indicators
  - Portfolio optimization
  - Risk analysis
  - Time series analysis

### 2. **TA-Lib** (C/Python)
- **Stars**: ~10k
- **URL**: https://github.com/TA-Lib/ta-lib
- **Description**: Technical Analysis Library
- **Features**:
  - 150+ indicators
  - Multiple language bindings
  - Industry standard
  - High performance
- **Use case**: Technical analysis foundation

### 3. **yfinance** (Python)
- **Stars**: ~12k
- **URL**: https://github.com/ranaroussi/yfinance
- **Description**: Yahoo Finance data downloader
- **Features**:
  - Historical data
  - Real-time quotes
  - Financial statements
  - Options data
- **Use case**: Free data source

## 📰 News & Sentiment Analysis

### 1. **FinBERT** (Python)
- **URL**: https://github.com/ProsusAI/finbert
- **Description**: Financial sentiment analysis with BERT
- **Features**:
  - Sentiment classification
  - Financial text analysis
  - Pre-trained models
- **Use case**: News sentiment, earnings calls

### 2. **News Scrapers**
- **finviz-scraper**: https://github.com/timgit/finviz-scraper
- **seeking-alpha-scraper**: Various implementations

## 🏦 Fundamental Analysis

### 1. **Fundamental Analysis** (Python)
- **URL**: https://github.com/jimmyadaro/Fundamental_Analysis_Python
- **Description**: Analyze stocks with financial statements
- **Features**:
  - Ratio analysis
  - Valuation metrics
  - Financial health scoring

### 2. **SEC EDGAR** (Python)
- **URL**: https://github.com/sec-edgar/sec-edgar
- **Description**: SEC filings downloader
- **Features**:
  - 10-K, 10-Q, 8-K filings
  - Company financials
  - Insider trading data

## 📊 Dashboards & Visualization

### 1. **FinPlot** (Python)
- **URL**: https://github.com/highfestiva/finplot
- **Description**: Fast financial plotting library
- **Features**:
  - Candlestick charts
  - Technical indicators
  - Real-time updates
  - Interactive zooming

### 2. **Plotly Finance**
- **URL**: https://github.com/plotly/plotly.py
- **Description**: Interactive financial charts
- **Features**:
  - Candlesticks, OHLC
  - Technical indicators
  - Subplots
  - Export to HTML

## 🔧 Complete Platforms

### 1. **TradingView Alternatives**
- **Chart.js**: Basic charting
- **ApexCharts**: Interactive charts
- **TradingView lightweight charts**: Free component

### 2. **Portfolio Trackers**
- **Ledger-cli**: Command-line accounting
- **Firefly III**: Self-hosted budgeting
- **GnuCash**: Full accounting suite

## 🤖 AI/ML for Finance

### 1. **FinRL** (Python)
- **Stars**: ~8k
- **URL**: https://github.com/AI4Finance-LLC/FinRL
- **Description**: Deep reinforcement learning for finance
- **Features**:
  - DRL algorithms
  - Trading environments
  - Backtesting
  - Paper trading

### 2. **PyTorch Geometric for Finance**
- Graph neural networks for market structure

## 📋 Recommended Stack for You

Based on your needs (free, local, Bloomberg terminal-like):

1. **Data Source**: `yfinance` (free, no API key)
2. **Backtesting**: `VectorBT` (fast, powerful)
3. **Technical Analysis**: `TA-Lib`
4. **Visualization**: `finplot` or `Plotly`
5. **Sentiment**: `FinBERT` (optional)
6. **Fundamentals**: `Fundamental_Analysis_Python`

## 🚀 Quick Start Commands

```bash
# Install core tools
pip install yfinance backtrader vectorbt ta-lib finplot plotly

# Install FinRL (optional)
pip install finrl

# Install FinBERT (optional)
pip install transformers torch
```

## 📚 Learning Resources

- **QuantStart**: quantstart.com
- **Investopedia**: investopedia.com
- **System Investor**: systematicinvestor.com
- **Finance Python**: finpy.org
