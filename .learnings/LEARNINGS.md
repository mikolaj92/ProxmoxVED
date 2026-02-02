# Learnings & Best Practices

## Python Package Management

### Use `uv` instead of `pip`
- **Why**: Significantly faster, better dependency resolution, lockfiles
- **Commands**:
  - `uv venv .venv` - Create virtual environment
  - `uv pip install package` - Install packages
  - `uv run python script.py` - Run scripts
  - `uvx package` - Run packages without installation
- **Performance**: 10-100x faster than pip for installs

## Web Crawling

### Anti-Bot Protection Bypass
- **Problem**: Many financial sites (Yahoo, Reuters, MarketWatch) block simple scrapers
- **Solution**: Use **Crawlee** + **Playwright** for human-like crawling
  - Mimics human behavior (delays, realistic headers)
  - Supports proxy rotation
  - Works with headful browsers (easier debugging)
- **Alternative**: **RSS feeds** are legal and rarely blocked

### RSS Feeds
- **Legal and reliable** way to get news without scraping
- **Sources**: Yahoo Finance, CNBC, Financial Times
- **No blocking**: RSS endpoints are designed for public access

## FRED API
- **Endpoint**: https://api.stlouisfed.org/
- **Registration**: Free at https://fredaccount.stlouisfed.org/
- **Key**: 32-character alphanumeric string
- **Env var**: `FRED_API_KEY`
- **Key Series**: GDP, CPI, Unemployment, Fed Funds Rate, PMI

## LM Studio Integration
- **Endpoint**: http://localhost:1234/v1
- **Models**: `qwen/qwen3-4b-2507`, `text-embedding-nomic-embed-text-v1.5`
- **Use for**: Sentiment analysis, AI-powered insights
- **No API key needed**: 100% local, no costs

## Sector Focus
- **Primary sectors**: GOLD, TECH
- **GOLD**: Safe haven, inflation hedge
- **TECH**: Growth, innovation, AI plays
- **Cycle phases**: Different recommendations per phase
