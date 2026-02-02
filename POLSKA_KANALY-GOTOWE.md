# 🎉 Polskie Kanały TV - Gotowe!

## ✅ Skonfigurowane:

1. **xTeVe** uruchomiony na http://192.168.11.66:34400/web/
2. **Polska playlista** utworzona z legalnych źródeł Free-TV/IPTV
3. Plik: `/root/arr-stack/config/xteve/poland.m3u`

---

## 📺 Dostępne kanały (12 kanałów):

### TVP (Telewizja Polska):
- **TVP1** - Główny kanał informacyjno-publicystyczny
- **TVP2** - Filmy, seriale, rozrywka
- **TVP3 Warszawa** - Regionalny kanał dla Mazowsza
- **TVP Polonia** - Kanał dla Polonii za granicą
- **TVP Info** - 24h informacyjny
- **Alfa TVP** - Kanał lifestylowy
- **TVP World** - Anglojęzyczny kanał o Polsce
- **TVP ABC 2** - Kanał dziecięcy
- **TVP Historia 2** - Filmy historyczne, dokumenty
- **TVP Kultura 2** - Sztuka, kultura, teatr

### Inne:
- **Belsat** - Kanał dla Białorusi w języku polskim
- **TV Republika** - Niezależny kanał informacyjny
- **4fun.tv** - Rozrywka, muzyka

---

## 🚀 Dodaj do xTeVe (2 minuty):

### Krok 1: Otwórz xTeVe
**URL:** http://192.168.11.66:34400/web/

### Krok 2: Dodaj playlistę
1. Kliknij **Settings** (⚙️) w prawym górnym rogu
2. Wybierz **Playlist** z menu
3. Kliknij **"Add Playlist"**
4. Wybierz **"M3U File"**
5. Wypełnij:
   - **Name:** `Polska - Free TV`
   - **URL/Path:** `/config/poland.m3u`
   - **Update:** `24 hours`
   - **Charset:** `UTF-8`
   - ✅ **Enabled**
6. Kliknij **"Save & Fetch"**
7. Poczekaj 1-2 minuty na załadowanie

### Krok 3: Sprawdź kanały
1. Kliknij **"Channels"** w górnym menu
2. Powinna pokazać się lista 12 polskich kanałów
3. Kliknij dowolny → **"Test Stream"** żeby sprawdzić czy działa

### Krok 4: Dodaj do Jellyfin
1. Otwórz **Jellyfin:** http://192.168.11.70:8096
2. Kliknij **Dashboard** (menu po lewej)
3. Wybierz **Live TV**
4. Kliknij **"+ Add TV tuner"**
5. Wybierz **"HDHomeRun"**
6. Wpisz URL: `http://192.168.11.66:34400`
7. Kliknij **"Save"**
8. Jellyfin wykryje kanały automatycznie

---

## 🎯 Gotowe!

Masz teraz:
- ✅ 12 legalnych polskich kanałów TV
- ✅ Darmowe (bez subskrypcji)
- ✅ Dostępne w Jellyfin
- ✅ Wysokiej jakości (HD)

---

## 📱 Jak oglądać:

### Przez Jellyfin Web:
1. Otwórz http://192.168.11.70:8096
2. Kliknij **"Live TV"** w menu
3. Wybierz polski kanał
4. Oglądaj! 🎉

### Przez aplikację Jellyfin:
- Smart TV: Zainstaluj aplikację Jellyfin
- Telefony/tablety: App Store / Google Play → "Jellyfin"
- Zaloguj się do http://192.168.11.70:8096
- Live TV → Wybierz kanał

---

## 🔄 Aktualizacja playlisty:

Playlista jest aktualizowana co 24h automatycznie przez xTeVe.

Jeśli chcesz odświeżyć ręcznie:
1. xTeVe → Settings → Playlist
2. Kliknij ikonę **odświeżania** 🔄 przy "Polska - Free TV"

---

## ❓ Co jeśli kanały nie działają?

### Sprawdź:
1. **Czy xTeVe działa?**
   - Otwórz http://192.168.11.66:34400/web/
   - Sprawdź czy możesz się zalogować

2. **Czy playlista jest załadowana?**
   - Settings → Playlist → Sprawdź czy "Polska - Free TV" ma kanały
   - Liczba kanałów powinna być ~12

3. **Test stream:**
   - Channels → Kliknij kanał → "Test Stream"
   - Powinien otworzyć się player

4. **Czy Jellyfin wykrył kanały?**
   - Jellyfin Dashboard → Live TV → Sprawdź czy są kanały

---

## 🆘 Potrzebujesz pomocy?

Daj znać jeśli:
- Playlista się nie ładuje
- Kanały nie działają
- Chcesz dodać więcej kanałów
- Chcesz zmienić kolejność

Pomogę! 😊
