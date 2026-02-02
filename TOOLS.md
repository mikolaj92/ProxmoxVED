# Python Development

## Package Manager: `uv` (ZAWSZE używaj UV!)

**Dlaczego UV > pip:**
- **10-100x szybszy** dla instalacji
- Lepsze rozwiązywanie zależności
- Lockfiles dla reprodukowalności
- Nowoczesne zarządzanie wersjami Pythona

**Instalacja:**
```bash
# Już zainstalowane: uv 0.9.26
# Check version: uv --version
```

**Instalacja pakietów:**
```bash
# ZAWSZE używaj UV!
uv pip install streamlit pandas

# Instalacja z requirements.txt
uv pip install -r requirements.txt

# W workspace z pyproject.toml:
cd workspaces/my-workspace
uv sync  # Zainstaluje wszystkie zależności
```

**Uruchamianie:**
```bash
# Ze środowiskiem wirtualnym
uv run streamlit run app.py
uv run python script.py

# Lub aktywacja środowiska
source .venv/bin/activate
streamlit run app.py
```

**Project setup (najlepsza praktyka):**
```bash
# Nowy projekt
uv init
uv pip install package-name

# Eksisting project
uv add package-name  # Dodaje do pyproject.toml
```

**WAŻNE:**
- NIGDY nie używaj `pip install` bezpośrednio
- ZAWSZE używaj `uv pip install` lub `uv sync`
- To dotyczy WSZYSTKICH projektów Pythonowych
