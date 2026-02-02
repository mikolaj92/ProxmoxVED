# 📺 Polskie Kanały IPTV - Kompletny Przewodnik

## ✅ xTeVe zainstalowany!

**Web UI:** http://192.168.11.66:34400/web/

xTeVe działa jako "most" między Twoim IPTV provider-em a Jellyfin.

---

## 🎯 Opcje dostępu do polskich kanałów

### Opcja 1: Płatni IPTV Providerzy (NAJLEPSZA jakość)

#### Top 3 providerzy z polskimi kanałami:

**1. Eternal TV (najlepszy stosunek jakości/ceny)**
- **Cena:** ~$8-12/miesiąc
- **Polskie kanały:** TVN, Polsat, TVP, HBO Polska, Canal+ Polska
- **Sport:** Eleven Sports, Polsat Sport, Eurosport Polska
- **Amerykańskie:** ESPN, Fox, CNN, NBC, ABC
- **Jak zamówić:** Szukaj "Eternal TV IPTV" na Google
- **Format:** M3U URL + Xtream Codes

**2. IPTV Farm**
- **Cena:** ~$10/miesiąc
- **Polskie kanały:** 50+ polskich kanałów
- **Sport:** Duży wybór sportowych
- **Jak zamówić:** https://iptvfarm.com

**3. Nitro TV**
- **Cena:** ~$15/miesiąc
- **Jakość:** Bardzo dobra
- **Polskie kanały:** Tak
- **Jak zamówić:** https://nitrotv.com

#### Co dostajesz od płatnego provider-a:
Po opłaceniu dostaniesz:
- **M3U URL**: np. `http://server.com:8080/get.php?username=twoj_user&password=twoje_haslo&type=m3u_plus&output=ts`
- **Xtream Codes**:
  - Server: `http://server.com:8080`
  - Username: `twoj_username`
  - Password: `twoje_haslo`

---

### Opcja 2: Darmowe playlisty (TESTOWE - niestabilne)

#### Przykładowe darmowe źródła:

**1. IPTV-Org (GitHub)**
```
M3U: http://iptv-org.github.io/iptv/countries/pl.m3u
XMLTV: http://iptv-org.github.io/iptv/countries/pl.epg.xml
```

**2. GitHub Playlists**
Szukaj na GitHub: "poland iptv m3u 2026"

**3. Free IPTV Lists**
- Strony typu: https://www.iptvsource.com
- Filtr: Poland

⚠️ **Uwaga:** Darmowe playlisty często:
- Mają niedziałające linki (30-70% działa)
- Zmieniają się codziennie
- Mają niską jakość
- Są wolne

---

## 🔧 Konfiguracja xTeVe krok po kroku

### Krok 1: Pierwsze logowanie
1. Otwórz: **http://192.168.11.66:34400/web/**
2. Utwórz hasło admin
3. Zaloguj się

### Krok 2: Dodaj playlistę M3U

**Opcja A: M3U URL (od provider-a)**

1. Settings (⚙️) → Playlist
2. "Add Playlist" → "M3U URL"
3. Wypełnij:
   - **Name:** np. "Mój IPTV"
   - **URL:** wklej M3U URL od provider-a
   - **Update:** co 24h
   - **Charset:** UTF-8
   - Zapoznacz: "Enabled"
4. "Save & Fetch"
5. Poczekaj na pobranie (może potrwać 1-2 minuty)

**Opcja B: Xtream Codes (od provider-a)**

1. Settings → Playlist
2. "Add Playlist" → "Xtream Codes"
3. Wypełnij:
   - **Name:** np. "Mój Xtream"
   - **Server URL:** np. `http://server.com:8080`
   - **Username:** twoj_username
   - **Password:** twoje_haslo
4. "Save & Fetch"

**Opcja C: Plik M3U (lokalny)**

1. Wrzuć plik `.m3u` do: `/root/arr-stack/config/xteve/`
2. Settings → Playlist
3. "Add Playlist" → "File"
4. Wybierz plik

### Krok 3: Sprawdź kanały
1. Menu: **Channels**
2. Powinna pokazać się lista kanałów
3. Kliknij kanał → "Test Stream" żeby sprawdzić czy działa

### Krok 4: Dodaj EPG (Program TV)

**Dla płatnych provider-ów:**
- Często EPG jest automatyczne (wspierane przez Xtream Codes)

**Dla darmowych playlist:**
1. Settings → EPG
2. "Add EPG Source"
3. URL: `http://iptv-org.github.io/iptv/countries/pl.epg.xml`
4. Zapisz

### Krok 5: Mapowanie kanałów
1. Menu: **Mapping**
2. Wybierz playlistę
3. Przypisz kanały do numerów (np. TVP1 → 1, Polsat → 2)
4. Zapisz

### Krok 6: Dodaj do Jellyfin
1. W Jellyfin: **Dashboard → Live TV → Add TV tuner**
2. Wybierz: **HDHomeRun**
3. URL: `http://192.168.11.66:34400`
4. Zapisz
5. Jellyfin powinien wykryć kanały

---

## 📋 Przykładowa konfiguracja (testowa)

### Testowa darmowa playlista

**W xTeVe:**
1. Settings → Playlist → Add M3U URL
2. Name: "Test PL"
3. URL: `http://iptv-org.github.io/iptv/countries/pl.m3u`
4. Save & Fetch

**Sprawdź:**
- Otwórz Channels
- Zobaczysz polskie kanały (jeśli działają)
- Kliknij dowolny → Test Stream

**W Jellyfin:**
- Dashboard → Live TV → Add HDHomeRun
- URL: `http://192.168.11.66:34400`
- Gotowe!

---

## 🎯 Polecana konfiguracja (produkcyjna)

### Dla płatnego IPTV provider-a:

**Krok 1: Zamów subskrypcję**
- Wybierz provider-a (np. Eternal TV)
- Zapłać
- Otrzymasz M3U URL lub Xtream Codes

**Krok 2: Skonfiguruj xTeVe**
1. http://192.168.11.66:34400/web/
2. Settings → Playlist → Dodaj URL od provider-a
3. Poczekaj na pobranie kanałów
4. Mapping → Ponumeruj kanały

**Krok 3: Dodaj do Jellyfin**
1. Jellyfin Dashboard → Live TV → Add HDHomeRun
2. URL: `http://192.168.11.66:34400`
3. Zapisz
4. Gotowe!

**Krok 4: Oglądaj**
- Otwórz Jellyfin
- Menu: **Live TV**
- Wybierz kanał polski

---

## 💰 Ceny porównawcze

### Płatni providerzy:
- **Eternal TV:** $8-12/miesiąc (~35-50 PLN)
- **IPTV Farm:** $10/miesiąc (~40 PLN)
- **Nitro TV:** $15/miesiąc (~60 PLN)

### Darmowe:
- **0 PLN** ale niestabilne i niska jakość

### Polska telewizja kablowa (dla porównania):
- **Cyfrowy Polsat:** 50-150 PLN/miesiąc
- **UPC:** 60-180 PLN/miesiąc
- **Orange:** 50-120 PLN/miesiąc

**Wniość:** IPTV jest **3-5x tańszy** niż kablowka!

---

## 🚀 Szybki start (5 minut)

### Szybki test z darmową playlistą:

1. **Otwórz xTeVe:** http://192.168.11.66:34400/web/
2. **Settings → Playlist → Add M3U URL**
3. **Name:** Test PL
4. **URL:** `http://iptv-org.github.io/iptv/countries/pl.m3u`
5. **Save & Fetch**
6. **Otwórz Channels** → zobacz listę
7. **Kliknij kanał** → Test Stream
8. **W Jellyfin:** Dashboard → Live TV → Add HDHomeRun → `http://192.168.11.66:34400`

Gotowe! Masz polskie kanały w Jellyfin! 🎉

---

## ❓ Pytanie?

Chcesz:
1. **Pomóc z zamówieniem** płatnego provider-a?
2. **Skonfigurować** konkretną playlistę?
3. **Dostosować** kanały w Jellyfin?

Daj znać! 😊
