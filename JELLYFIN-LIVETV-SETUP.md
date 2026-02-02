# 📺 Dodawanie xTeVe Tuner do Jellyfin - Instrukcja

## Problem:
Nie widzisz "Live TV" w Jellyfin, bo nie został jeszcze dodany tuner.

## Rozwiązanie:
Dodaj xTeVe jako HDHomeRun tuner przez dashboard Jellyfin.

---

## 🎯 Krok po kroku:

### Krok 1: Otwórz Dashboard Jellyfin
1. Otwórz przeglądarkę
2. Wejdź: **http://192.168.11.70:8096**
3. Zaloguj się
4. Kliknij swój awatar (prawy górny róg)
5. Wybierz **"Dashboard"** z menu

### Krok 2: Otwórz Live TV
1. Po lewej stronie zobaczysz menu
2. Przewiń w dół do **"Live TV"**
3. Kliknij **"Live TV"**

### Krok 3: Dodaj tuner
1. W środku ekranu kliknij **"+ Add TV tuner"**
2. Wybierz typ tunera: **"HDHomeRun"**
3. Wypełnij:
   - **Device ID:** `xteve-1` (może być dowolne)
   - **Tuner Type:** HDHomeRun (zaznaczone)
   - **Host/URL:** `http://192.168.11.66:34400`
4. Kliknij **"Save"** lub **"Add"**

### Krok 4: Poczekaj na wykrycie
1. Jellyfin będzie skanował xTeVe (~10-30 sekund)
2. Powinien pokazać "1 tuner found" lub podobnie

### Krok 5: Sprawdź czy działa
1. Wróć do głównego ekranu Jellyfin
2. W menu po lewej powinien pojawić się **"Live TV"**
3. Kliknij **"Live TV"**
4. Powinna pokazać się lista kanałów

---

## 🔧 Jeśli nadal nie działa:

### Sprawdź xTeVe:
1. Otwórz: **http://192.168.11.66:34400/web/**
2. Zaloguj się
3. Czy widać kanały w **Channels**?
   - Jeśli nie → Dodaj playlistę najpierw (patrz niżej)

### Dodaj playlistę do xTeVe:
1. **Settings** → **Playlist** → **Add M3U URL**
2. Name: `Polska Test`
3. URL: `https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8`
4. **Save & Fetch**
5. Poczekaj 1-2 minuty
6. Sprawdź **Channels** → czy są kanały?

### Ponów dodawanie tunera w Jellyfin:
- Dashboard → Live TV → Add HDHomeRun
- URL: `http://192.168.11.66:34400`

---

## 🎯 Szybki test:

Jeśli nie chcesz czekać na playlistę z Free-TV, użyj testowej:

**W xTeVe:**
1. Settings → Playlist → Add M3U URL
2. URL: `http://iptv-org.github.io/iptv/countries/pl.m3u`
3. Save & Fetch

**W Jellyfin:**
1. Dashboard → Live TV → Add HDHomeRun
2. URL: `http://192.168.11.66:34400`
3. Save

---

## 📱 Po dodaniu tunera:

### Live TV pojawi się w menu:
- Główny ekran Jellyfin → **Live TV** (po lewej)
- Kliknij → wybierz kanał
- Oglądaj!

---

## ❓ Problem nadal?

Sprawdź:
1. **Czy xTeVe działa?** → http://192.168.11.66:34400/web/
2. **Czy Jellyfin działa?** → http://192.168.11.70:8096
3. **Czy masz dostęp do Dashboard?** → Zaloguj jako admin

---

## 🆘 Pomoc:

Jeśli nadal nie działa:
- Daj zrzut ekranu z Dashboard → Live TV
- Albo napisz co widzisz po lewej stronie w menu
- Pomogę dalej! 😊
