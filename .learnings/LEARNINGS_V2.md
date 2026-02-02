# CLAWDBOT LEARNINGS
**Best practices for development with Clawdbot**

## 🐍 PYTHON PACKAGE MANAGEMENT

### Use `uv` Instead of `pip`
**From now on, ALWAYS use `uv` for Python packages**

**Why `uv` is better:**
- 🚀 **100x Faster** - Parallel downloads, caching
- 🔧 **Better Dependency Resolution** - Automatically solves version conflicts
- 🌍 **Better Virtual Environments** - Seamless integration with virtualenv
- 📦 **Modern & PEP 508 Compliant** - Better pyproject.toml handling
- 🎯 **Reliable** - Doesn't fail with cryptic error messages

### Basic `uv` Commands

**Create new project:**
```bash
uv init project-name
cd project-name
```

**Install dependencies:**
```bash
uv add pandas numpy
uv add scikit-learn
uv add openai
```

**Run scripts with uv:**
```bash
# Run script with current environment
uv run python script.py

# Execute command
uv pip install -e .  # Install project dependencies
```

**Update packages:**
```bash
uv add --upgrade package-name
```

**Remove packages:**
```bash
uv remove package-name
```

### Project Structure with `uv`

**Recommended project structure:**
```
my-project/
├── pyproject.toml       # Project config (instead of setup.py/requirements.txt)
├── .python-version       # Python version specification
├── src/                 # Source code
│   └── my_package/
├── scripts/              # Utility scripts
├── tests/               # Tests
└── README.md
```

**pyproject.toml Example:**
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.10"

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project.scripts]
cli = "my_package.cli:main"

[project.optional-dependencies]
dev = [
    "pytest",
    "black",
    "ruff"
]

[project.optional-dependencies]
docs = [
    "sphinx",
]

[project.urls]
Homepage = "https://github.com/username/my-project"

[tool.uv.sources]
index = "https://pypi.org/simple"

[tool.uv]
dev-dependencies = [
    "ruff",
    "pytest",
]
```

---

## 📊 RYNEK FINANSOWY - SYSTEMY THINKING

### Core Principle
**Quant Trading is about understanding systems, not predicting numbers.**

### Approach
1. **Data Collection** - Aggregate data from multiple sources
2. **Pattern Recognition** - Identify historical cycles (Expansion, Peak, Recession, Trough)
3. **Game Theory** - Analyze country strategies (USA vs China vs Japan)
4. **Scenario Analysis** - Generate "What If" scenarios (not predictions)
5. **Statistical Analysis** - Mean reversion, Z-score, confidence levels

### Data Sources
- ✅ **RSS Feeds** (Yahoo Finance, CNBC) - Legal, no API key
- ✅ **Local LLM** (LM Studio) - No external dependencies
- ✅ **Macro Data** (PRAWZIWE HISTORIĘ) - Not mock data
- ✅ **News Sentiment** - AI-analyzed in real-time

### System Components
- `skills/local-web-crawler/scripts/final_sector_agent.py` - Main agent
- `skills/local-web-crawler/scripts/rss_news_crawler.py` - News crawler
- `skills/local-web-crawler/scripts/sentiment_analyzer.py` - AI sentiment
- `skills/local-web-crawler/scripts/macro_api.py` - FRED API integration
- `skills/local-web-crawler/scripts/quant_system_v3.py` - Quant trading system (cycles + game theory)

### Key Files
- `.learnings/TRUE_MACRO_HISTORY.md` - Historical macro data
- `.learnings/WORLD_MODELING_SYSTEM.md` - World modeling architecture
- `.learnings/QUANT_SYSTEM_REPORT.json` - Quant trading reports

---

## 🌏 SYSTEMS THINKING APPROACH

### Level 1: Dependency Graphs
**Kto zależy od kogo?**
- USA: Depends on China (chips), Japan (carry trade)
- China: Depends on USA (technology), Australia (raw materials)
- Japan: Depends on USA (market), China (competition)
- Iran: Depends on global markets (oil prices), OPEC

### Level 2: Competition Matrices
**Kto z kim rywalizuje?**
- AI & Chips: USA (NVIDIA, OpenAI) vs China (Baidu, Alibaba)
- EVs: Tesla (USA) vs BYD (China) vs CATL (China)
- Solar: First Solar (USA) vs JA Solar (China)

### Level 3: Monetary Wars
**Kto ma przewagę?**
- USA: High rates → Strong dollar → Export disadvantage
- Japan: Negative rates → Weak Yen → Export advantage (carry trade)
- China: Managed rates → Competitive pricing

### Level 4: Scenario Engine
**Co jeśli X to zrobisz Y?**
- Scenario A: Fed rate cut → What happens to Yen?
- Scenario B: USA-China tech war → What happens to chip prices?
- Scenario C: Iran sanctions → What happens to oil prices?

---

## 🚀 WORKFLOW

### Daily Analysis Workflow
1. **0800** - News crawler fetches latest articles
2. **0805** - AI sentiment analyzes sentiment
3. **0810** - Macro data imported from history
4. **0815** - Cycle detection identifies current phase
5. **0820** - Game theory analyzes competition
6. **0825** - Scenario engine generates "What If" scenarios
7. **0830** - System generates final report & recommendations

### Key Components
- **News Sentiment Analysis** - Real-time AI-driven
- **Macro Historical Data** - True historical data (not mock)
- **Cycle Detection** - Identifies Expansion, Peak, Recession, Trough
- **Game Theory** - Nash Equilibrium for country strategies
- **Scenario Engine** - "What If" analysis for different outcomes

---

## 🎯 BEST PRACTICES

### Package Management
- ✅ **Use `uv add` instead of `pip install`**
- ✅ **Use `uv run python script.py`** for running scripts
- ✅ **Use `uv sync`** for environment synchronization
- ✅ **Use pyproject.toml** instead of requirements.txt**

### Development
- ✅ **Keep scripts modular** - One concern per script
- ✅ **Use JSON for data exchange** - Easy parsing and debugging
- ✅ **Log everything** - Save to `.learnings/` directory
- ✅ **Save reports to JSON** - Easy analysis and tracking

### Data Sources
- ✅ **Use RSS feeds** - Legal, no API keys
- ✅ **Use local LLMs** - No external dependencies
- ✅ **Use historical data** - True macro history (2020-2025)
- ✅ **No ML black boxes** - Transparent statistical analysis

### System Design
- ✅ **Modular architecture** - Each component independent
- ✅ **Clear data flow** - News → Sentiment → Macro → Analysis → Report
- ✅ **Version control** - Use Git for all changes
- ✅ **Backup data** - Always keep history in `.learnings/`

---

## 📚 REFERENCE

### ClawdHub Skills
- https://github.com/VoltAgent/awesome-clawdbot-skills - Browse and install skills
- Follow `Agent Skill convention` for consistency

### Key Skills for Quant Trading
- `rss_news_crawler` - Fetch news from Yahoo Finance, CNBC
- `sentiment_analyzer` - AI sentiment with LM Studio
- `macro_api` - FRED API integration (real data)
- `quant_system_v3` - Cycles + Game Theory + Statistics

### Documentation
- `SYSTEM_SUMMARY.md` - Complete system overview
- `TOOLS.md` - Commands and tools reference
- `LEARNINGS.md` - This file - Best practices

---

## 🔧 TROUBLESHOOTING

### Package Installation Issues
If `uv add package-name` fails:
1. Check Python version compatibility
2. Try `uv pip install package-name` (fallback to pip)
3. Check project configuration (pyproject.toml)

### Python Version
- **Recommended:** Python 3.10+ (for best `uv` compatibility)
- **Current:** 3.14.0 (Python 3.14 is bleeding edge, uv might have some issues)
- **Solution:** Python 3.10-3.13 is most stable

### Environment Issues
If scripts don't run:
1. Check Python version: `uv --version`
2. Check dependencies: `uv pip list`
3. Check environment: `uv venv status`

### Memory Issues
If LM Studio has memory issues:
1. Restart LM Studio app
2. Use smaller model (qwen/qwen3-4b-2507)
3. Reduce context window in script

---

## ✅ QUICK REFERENCE

### Essential Commands
```bash
# Create new project
uv init project-name
cd project-name

# Install dependencies
uv add package-name

# Run script
uv run python script.py

# Update dependencies
uv add --upgrade package-name
```

### File Locations
- Scripts: `skills/local-web-crawler/scripts/`
- Documentation: `.learnings/`
- History: `.learnings/daily/`
- Reports: `.learnings/quant_reports/`

### Key Scripts
- `final_sector_agent.py` - Main daily analysis agent
- `rss_news_crawler.py` - News crawler (RSS)
- `sentiment_analyzer.py` - AI sentiment (LM Studio)
- `macro_api.py` - FRED API integration
- `quant_system_v3.py` - Quant trading system (cycles + game theory)

---

## 🎯 PRODUCYJNOŚĆ

### System Status
- ✅ **News Crawler** - Working perfectly (RSS)
- ✅ **AI Sentiment** - Working perfectly (LM Studio local)
- ✅ **Macro Data** - Using TRUE HISTORY (not mock)
- ✅ **Cycle Detection** - Working (Expansion/Peak/Recession/Trough)
- ✅ **Game Theory** - Working (USA vs China vs Japan)
- ✅ **Scenario Engine** - Working ("What If" scenarios)
- ✅ **Full Agent** - Working (daily reports at 8:00 AM)

### Daily Workflow
```
0800 AM - News crawler fetches latest articles
0810 AM - AI sentiment analyzes sentiment
0820 AM - Macro data imported from history
0830 AM - Cycle detection identifies current phase
0840 AM - Game theory analyzes competition
0850 AM - Scenario engine generates "What If" scenarios
0860 AM - System generates final report & recommendations
0870 AM - Report saved to .learnings/daily/YYYYMMDD/
0880 AM - System ready for next day
```

---

## 🚀 NEXT STEPS

### Short Term
1. ✅ Use `uv` for all Python package management
2. ✅ Continue using TRUE historical macro data (not mock)
3. ✅ Run `final_sector_agent.py` daily at 8:00 AM
4. ✅ Monitor for cycle phase changes (Recession, Peak, etc.)

### Medium Term
1. 🔄 Add more sectors (Energy, Healthcare, Crypto)
2. 🔄 Improve Game Theory engine (Nash Equilibrium calculation)
3. 🔄 Add more historical macro data points (earlier years)
4. 🔄 Implement automatic data updates from news (detect when Fed cuts rates)

### Long Term
1. 🌏 Build comprehensive World Modeling System (all countries, all sectors)
2. 🌏 Add predictive analytics (without ML black box)
3. 🌏 Implement automated trading signals (based on cycles + scenarios)
4. 🌏 Create dashboard UI (visualizing dependencies, competition, scenarios)

---

## ✅ SYSTEM READY

The quant trading system is **fully operational** with:
- ✅ **True historical macro data** (not mock)
- ✅ **Real-time news sentiment** (AI-analyzed)
- ✅ **Cycle detection** (Historical pattern recognition)
- ✅ **Game theory analysis** (Country strategies, Nash equilibrium)
- ✅ **Scenario engine** ("What If" analysis)
- ✅ **Investment recommendations** (GOLD, TECH, etc.)
- ✅ **Full automation** (Daily at 8:00 AM)

**Use `uv` for all future Python package management!**
