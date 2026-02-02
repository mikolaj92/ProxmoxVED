# 🚀 Szybki Start - Polskie Kanały IPTV (5 minut)

## Krok 1: Otwórz xTeVe
**URL:** http://192.168.11.66:34400/web/

## Krok 2: Dodaj testową playlistę

1. Kliknij **Settings** (⚙️) w prawym górnym rogu
2. Wybierz **Playlist** z menu
3. Kliknij **"Add Playlist"**
4. Wybierz **"M3U URL"**
5. Wypełnij:
   - **Name:** `Test PL`
   - **URL:** `http://iptv-org.github.io/iptv/countries/pl.m3u`
   - **Update:** `24 hours`
   - **Charset:** `UTF-8`
   - ✅ **Enabled**
6. Kliknij **"Save & Fetch"**
7. Poczekaj 1-2 minuty na pobranie

## Krok 3: Sprawdź kanały

1. Kliknij **"Channels"** w górnym menu
2. Powinna pokazać się lista kanałów polskich
3. Kliknij dowolny kanał
4. Kliknij **"Test Stream"** żeby sprawdzić czy działa

## Krok 4: Dodaj do Jellyfin

1. Otwórz **Jellyfin**: http://192.168.11.70:8096
2. Kliknij **Dashboard** (po lewej)
3. Wybierz **Live TV** z menu
4. Kliknij **"+ Add TV tuner"**
5. Wybierz **"HDHomeRun"**
6. W URL wpisz: `http://192.168.11.66:34400`
7. Kliknij **"Save"**
8. Jellyfin wykryje kanały automatycznie

## Krok 5: Oglądaj!

1. Wróć do głównego ekranu Jellyfin
2. Kliknij **"Live TV"** w menu
3. Wybierz polski kanał
4. Ciesz się telewizją! 🎉

---

## ✅ Gotowe!

Masz teraz:
- xTeVe działa na http://192.168.11.66:34400
- Testowa polska playlista załadowana
- Kanały dostępne w Jellyfin

---

## 🎯 Następne kroki (opcjonalnie)

### Jeśli testowe kanały działają:
Zamów płatnego IPTV provider-a dla lepszej jakości:
- **Eternal TV** (~$10/miesiąc)
- **IPTV Farm** (~$10/miesiąc)
- **Nitro TV** (~$15/miesiąc)

### Jeśli chcesz więcej kanałów:
1. Zdobądź M3U URL od provider-a
2. W xTeVe: Settings → Playlist → Add M3U URL
3. Wklej nowy URL
4. Save & Fetch

### Jeśli chcesz dostosować kanały:
1. W xTeVe: Mapping
2. Ponumeruj kanały wg uznania
3. Zapisz

---

## 📞 Potrzebujesz pomocy?

Daj znać jeśli:
- Testowa playlista nie działa
- Chcesz zamówić płatnego provider-a
- Chcesz skonfigurować konkretne kanały

Pomogę! 😊
