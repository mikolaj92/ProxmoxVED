# ✅ xTeVe jest uruchomiony! Teraz dodamy tuner do Jellyfin.

## Status:
- ✅ xTeVe działa na http://192.168.11.66:34400/web/
- ✅ Polska playlista jest gotowa
- ❌ Tuner nie został jeszcze dodany do Jellyfin (problem z API)

---

## 🎯 Dodaj tuner ręcznie przez interfejs Jellyfin (3 minuty):

### Krok 1: Otwórz Jellyfin
**URL:** http://192.168.11.70:8096
Zaloguj się

### Krok 2: Otwórz Dashboard
Kliknij swój awatar (prawy górny róg) → **Dashboard**

### Krok 3: Live TV
Menu po lewej → przewiń w dół → **Live TV**

### Krok 4: Dodaj tuner
Jeśli widzisz "+ Add TV tuner" lub przycisk dodawania:
1. Kliknij **"+ Add TV tuner"**
2. Wybierz **"HDHomeRun"** lub **"M3U"**
3. Wpisz:
   - **Name:** `xTeVe IPTV`
   - **URL:** `http://192.168.11.66:34400`
4. Kliknij **"Save"**

### Krok 5: Poczekaj
Jellyfin skanuje xTeVe (~10-30 sekund)

### Krok 6: Sprawdź
Wróć do głównego ekranu → Menu po lewej → **Live TV** powinno być widoczne

---

## 📺 Jeśli nie widzisz opcji dodawania tunera:

### Opcja A: Włącz Live TV
1. Dashboard → **Live TV** (po lewej)
2. Może być przycisk **"Enable Live TV"** lub **"Add tuner"**
3. Kliknij i postępuj wg instrukcji

### Opcja B: Przez M3U Playlist (alternatywa)
Jeśli HDHomeRun nie działa, użyj M3U:
1. Dashboard → Live TV → **Add M3U tuner**
2. **Name:** `Polska TV`
3. **M3U URL:** `http://192.168.11.66:34400/playlist.m3u`
   (lub po dodaniu playlisty: `http://192.168.11.66:34400/channels.m3u`)
4. **XMLTV URL:** `http://192.168.11.66:34400/xmltv.xml`
5. Kliknij **"Save"**

---

## 🔧 Dodaj playlistę do xTeVe (jeśli jeszcze nie jest):

### Przez interfejs web:
1. Otwórz **http://192.168.11.66:34400/web/**
2. Zaloguj się (domyślne hasło jeśli ustawione)
3. **Settings** → **Playlist**
4. **Add M3U URL** lub **Add File**
5. URL/Path: `/config/poland.m3u`
6. **Save & Fetch**
7. Poczekaj 1-2 minuty
8. Sprawdź **Channels** → czy są polskie kanały

---

## ❓ Problem nadal?

Sprawdź:
1. **Czy xTeVe działa?** → http://192.168.11.66:34400/web/
2. **Czy Jellyfin działa?** → http://192.168.11.70:8096
3. **Jestem zalogowany jako admin?**

Zrób zrzut ekranu z Dashboard → Live TV i pokaż mi! 😊
