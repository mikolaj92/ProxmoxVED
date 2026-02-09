# Plan implementacji - Issue #2: Analiza "tabeli 1"

**Data:** 2026-02-06  
**Repo:** mikolaj92/msds-portal  
**Issue:** https://github.com/mikolaj92/msds-portal/issues/2

---

## 📊 Grupa 1: Page-break w tabelach (PRIORITY: HIGH)

### Problemy
- **Karta 354:** CAS na kolejnej stronie niż nazwa (nazwa s. 2/15, CAS s. 3/15)
- **Karta 563:** Substancja rozdzielona na 2 rekordy przez łamanie strony

### Root Cause
`section3_extractor/main.py:89-91` truncates section 3 to 10000 chars when it exceeds limit. This breaks tables that span across pages.

### Technical Approach
1. **Rozszerz `section3_extractor/main.py`**:
   - Zamiast hard truncate do 10000 chars, znajdź granice sekcji (Section 4 start)
   - Użyj `end_pos` z `batch_extractor.extract()` jako naturalnej granicy
   - Dodaj `PageBreakHandler` który łączy fragmenty tabel rozdzielonych stronami

2. **Nowy plik: `section3_extractor/page_break_handler.py`**:
   ```python
   class PageBreakHandler:
       """Łączy fragmenty tabel rozdzielonych przez łamanie strony."""
       
       def merge_split_rows(self, markdown: str) -> str:
           # Detect table fragments:
           # - Header pattern only on first page
           # - Incomplete row (missing CAS) at page end
           # - Continuation on next page (starts with CAS, no name)
           pass
   ```

3. **Integracja z `pipeline.py`**:
   - Wywołaj `PageBreakHandler` przed `llm_extractor.extract()`
   - Emit span `"page_break_merge"` z statystykami (ilość scalonych wierszy)

### Pliki do zmiany
- `rudy-worker/src/rudy_worker/vendor/section3_extractor/section3_extractor/main.py` (line 89-91)
- `rudy-worker/src/rudy_worker/vendor/section3_extractor/section3_extractor/page_break_handler.py` (NEW)
- `rudy-worker/src/rudy_worker/pipeline.py` (dodaj `PageBreakHandler` do flow)

---

## 🤥 Grupa 2: Halucynacja danych (PRIORITY: MEDIUM)

### Problemy
- **Karta 32:** Odczytał "TiO2 <1%" mimo że nie było w tabeli ani z nr CAS

### Root Cause
LLM extrapolates from descriptive text outside Section 3 instead of stick-to-facts from table only.

### Technical Approach
1. **Ulepsz `llm_extractor/extractor.py` prompt**:
   - Dodaj explicit constraint: `ONLY extract substances that appear in a TABLE format`
   - Dodaj: `If information appears in prose but NOT in a table, ignore it`
   - Dodaj validation rule: `Every substance MUST have either CAS or explicit percentage from table`

2. **Dodaj post-processing w `normalizer.py`**:
   - Nowa funkcja `validate_hallucinations(substances, section3_text)`
   - Sprawdza czy nazwa substancji występuje w `section3_text`
   - Jeśli nie → flag `hallucinated: true` + usuń z wyników
   ```python
   def validate_hallucinations(substances: List[Substance], section3_text: str) -> List[Substance]:
       """Remove substances that don't appear in section 3 text (hallucinations)."""
       cleaned = []
       for sub in substances:
           # Simple substring match (fuzzy for typos)
           if sub.name.lower() in section3_text.lower():
               cleaned.append(sub)
           else:
               _log.warning(f"Removed hallucinated substance: {sub.name}")
       return cleaned
   ```

3. **Integracja z `pipeline.py`**:
   - Wywołaj `validate_hallucinations()` po `llm_extractor.extract()`
   - Emit span `"hallucination_check"` z liczbą usuniętych halucynacji

### Pliki do zmiany
- `rudy-worker/src/rudy_worker/vendor/llm_extractor/llm_extractor/extractor.py` (prompt constraints)
- `rudy-worker/src/rudy_worker/normalizer.py` (dodaj `validate_hallucinations()`)
- `rudy-worker/src/rudy_worker/pipeline.py` (integruj validation)

---

## 🌿 Grupa 3: Sekcja 9 - VOC / rozpuszczalniki (PRIORITY: LOW)

### Problemy
- **Karty 32, 354, 56:** Sekcja 9.2 zawiera "VOC: 0%" lub "rozpuszczalniki organiczne: 2,9%"
- System ignoruje te dane
- Gdy VOC = 0%, można pominąć dalszą analizę (oszczędność czasu)

### Root Cause
Brak ekstraktora dla sekcji 9 (obecnie tylko sekcja 3)

### Technical Approach
1. **Nowy plik: `section9_extractor/extractor.py`**:
   ```python
   class Section9Extractor:
       """Extract Section 9 (VOC/solvents) from MSDS."""
       
       def extract(self, full_markdown: str) -> Dict[str, Any]:
           """Extract VOC and solvent info from section 9.2."""
           # Patterns:
           # - "VOC: 0%"
           # - "rozpuszczalniki organiczne: X%"
           # - "volatile organic compounds: X%"
           pass
   ```

2. **Integracja z `pipeline.py`**:
   - Wywołaj `Section9Extractor.extract()` po `Section3Extractor`
   - Jeśli `VOC == 0%` → emit span `"skip_db_lookup"` i pomiń `regulations_db` lookup
   - Zapisz `voc_info` w wynikach (do dashboardu)

3. **Prompt dla LLM**:
   - Dodaj do promptu: `Check section 9.2 for VOC info. If VOC = 0%, you can skip database lookup.`

### Pliki do zmiany
- `rudy-worker/src/rudy_worker/vendor/section9_extractor/section9_extractor/extractor.py` (NEW)
- `rudy-worker/src/rudy_worker/vendor/section9_extractor/section9_extractor/main.py` (NEW)
- `rudy-worker/src/rudy_worker/pipeline.py` (dodaj Section 9 extraction + skip logic)

---

## 📋 Implementacja Plan

### Faza 1: Page-break handler (2-3 dni)
1. Stwórz `page_break_handler.py` z heurystykami scalania tabel
2. Zmodyfikuj `section3_extractor/main.py` (usuń hard truncate)
3. Dodaj span emit dla page-break merge stats
4. Test na kartach 354, 563

### Faza 2: Anti-hallucination (1-2 dni)
1. Ulepsz prompt w `llm_extractor/extractor.py`
2. Dodaj `validate_hallucinations()` w `normalizer.py`
3. Integruj z `pipeline.py`
4. Test na karcie 32

### Faza 3: Section 9 VOC extraction (2-3 dni)
1. Stwórz `section9_extractor` package
2. Implementuj VOC extraction patterns
3. Dodaj skip logic w `pipeline.py` (jeśli VOC = 0%, pomiń regulations DB)
4. Test na kartach 32, 354, 56

### Faza 4: Testing & validation (1-2 dni)
1. Uruchom na wszystkich 4 problematycznych kartach
2. Porównaj wyniki przed/po
3. Dodaj logi/warnings dla edge cases
4. Zcommituj zmiany

---

## 🔍 Test Cases

### Karta 32 (halucynacja)
- **Oczekiwany:** TiO2 <1% usunięte (nie w tabeli)
- **Sekcja 9:** VOC = 0% → skip regulations DB

### Karta 354 (page-break)
- **Oczekiwany:** CAS połączony z nazwą (nawet jeśli na innej stronie)
- **Sekcja 9:** VOC = 0% → skip regulations DB

### Karta 56 (VOC pattern)
- **Oczekiwany:** "rozpuszczalniki organiczne: 2,9%" rozpoznane jako VOC

### Karta 563 (page-break)
- **Oczekiwany:** Substancja nie rozdzielona na 2 rekordy

---

## 💡 Dodatkowe uwagi

- **Rudy-worker vs rudy-worker-mlx:** Core extraction logic jest identyczny, zmiany apply do obu
- **Dashboard spans:** Nowe span types: `page_break_merge`, `hallucination_check`, `voc_extraction`, `skip_db_lookup`
- **Fallbacks:** Jeśli LLM nadal halucynuje, rozważ regex-only mode (już istnieje `regex_extractor.py`)
- **Monitoring:** Dodaj metrics: licznik scalonych page-breaków, usuniętych halucynacji, pominiętych DB lookups

---

**Szacowany czas:** 6-10 dni (1-2 tygodnie)  
**Risk:** Page-break handler może wymagać iteracji (heurystyki nie są idealne)  
**Priority:** Grupa 1 (page-break) > Grupa 2 (hallucynacje) > Grupa 3 (VOC)
