# Kompletny Przewodnik Konfiguracji - ARR Stack

## 🎯 Status Aktualny

### ✅ Gotowe i Uruchomione
- **CT220 (ARR)**: 192.168.11.66
  - Sonarr (8989), Radarr (7878), Prowlarr (9696)
  - Bazarr (6767), Readarr (8787), Lidarr (8686)
  - Transmission (9091), Jellyseerr (5055)
  - **Sportarr (1867)** ← NOWE
  - **Tunarr (8000)** ← NOWE

- **CT230 (Jellyfin)**: 192.168.11.70
  - Jellyfin (8096)

---

## 1️⃣ Sportarr - PVR dla Sportu

### Web UI
URL: http://192.168.11.66:1867

### Konfiguracja krok po kroku

#### A. Pierwsze logowanie
1. Wejdź: http://192.168.11.66:1867
2. Utwórz konto admin (username + password)
3. Zapisz te dane - będą potrzebne do API

#### B. Media Management (Root Folder)
1. Settings → Media Management → Root Folders
2. Add Root Folder:
   - Path: `/sports`
   - Quality: Prefer WEB-DL 1080p
   - Zapisz

#### C. Download Client (Transmission)
1. Settings → Download Clients
2. Add → Transmission:
   - Host: `transmission` (container name)
   - Port: `9091`
   - Username: `transmission`
   - Password: `Test123`
   - Category: `sportarr-downloads`
   - Zapisz

#### D. Indexers (Prowlarr Integration)
**W Prowlarr (http://192.168.11.66:9696):**
1. Settings → Apps → Add App
2. Type: **Sonarr** (Sportarr używa Sonarr API)
3. Name: Sportarr
4. URL: `http://192.168.11.66:1867`
5. API Key: (weź z Sportarr → Settings → General)
6. Categories: **5000** (TV - includes Sports)
7. Enable: ✅
8. Test & Save

**W Sportarr:**
1. Settings → Indexers
2. Indexery powinny się zsynchronizować automatycznie z Prowlarr

#### E. Dodawanie lig/druzyn
1. Search → Wpisz nazwę ligi (np. "Premier League", "NBA", "UFC")
2. Wybierz → Add to Library
3. Ustaw jakości (np. 1080p)
4. Enable Monitoring

#### F. Integracja z Jellyfin
1. Settings → Connect → Jellyfin
2. URL: `http://192.168.11.70:8096`
3. API Key: `a3dd99094b9e4b38b5afd2e2cb4af390`
4. Test Connection
5. Enable Library Updates

---

## 2️⃣ Tunarr - Kanały TV z Twoich Mediów

### Web UI
URL: http://192.168.11.66:8000

### Status aktualny
✅ Jellyfin skonfigurowany jako źródło mediów
✅ Kanał "Movies 24/7" stworzony
⏳ Wymaga dodania programowania

### Konfiguracja krok po kroku

#### A. Sprawdź źródła mediów
1. http://192.168.11.66:8000
2. Settings → Media Sources
3. Powinny widnieć:
   - **Jellyfin Movies** ✅
   - **Jellyfin TV Shows** ✅

#### B. Dodaj programowanie do kanału
1. Channels → Kliknij "Movies 24/7"
2. Zakładka: **"Programming"**
3. Kliknij: **"Add Programming"**
4. Ustaw:
   - **Source**: Jellyfin Movies
   - **Type**: Flex (losowe programy)
   - **Start Time**: 00:00 (początek doby)
   - **Duration**: 24 hours
5. Kliknij "Add Programs"
6. Tunarr pobierze listę filmów z Jellyfin

#### C. Włącz kanał
1. Wróć do Channels
2. Toggle "Movies 24/7" → **ON**
3. Sprawdź XMLTV: http://192.168.11.66:8000/xmltv.xml
   - Powinien pokazywać programy filmowe

#### D. Integracja z Jellyfin

**Opcja A: HDHomeRun (zalecane)**
1. W Jellyfin: Dashboard → Live TV → Add TV tuner
2. Wybierz: **HDHomeRun**
3. Tunarr powinien zostać wykryty automatycznie
4. Zapisz

**Opcja B: M3U Playlist**
1. Upewnij się że kanał ma programowanie w Tunarr
2. Skopiuj URL M3U (pojawi się po dodaniu programowania):
   - http://192.168.11.66:8000/lineups.m3u
3. W Jellyfin: Dashboard → Live TV → Add M3U Tuner
4. Wklej URL
5. XMLTV URL: http://192.168.11.66:8000/xmltv.xml
6. Zapisz

#### E. Tworzenie dodatkowych kanałów (opcjonalnie)
**Kanał "Dla Dzieci":**
1. Channels → Create Channel
2. Name: "Kids TV"
3. Number: 2
4. Programming → Source: Jellyfin TV Shows → Filter by Genre: "Animation"
5. Enable

**Kanał "Serial TV":**
1. Channels → Create Channel
2. Name: "TV Series Marathon"
3. Number: 3
4. Programming → Source: Jellyfin TV Shows
5. Type: Sequential (odcinki po kolei)

---

## 3️⃣ IPTV - Polskie i Amerykańskie Kanały TV

### Opcje dostępu

#### Opcja A: IPTV Provider (płatny)
**Popularni providery z polskimi kanałami:**
- **IPTV-Subs** (https://iptvsubs.com)
- **Nitro TV** (https://nitrotv.com)
- **Sportz TV** (dla sportu)

**Ceny:** ~$10-20/miesiąc za setki kanałów

**Co dostajesz:**
- Polskie: TVN, Polsat, TVP, HBO Polska, Canal+ Polska
- Amerykańskie: ESPN, Fox, CNN, NBC, ABC
- Sport: Eleven Sports, Polsat Sport, ESPN, Fox Sports

#### Opcja B: Darmowe playlisty (niestabilne)
- Strony typu GitHub iptv-org
- Forum typu Reddit r/iptv
- ⚠️ Często niedziałające linki

#### Opcja C: Xtream Codes (najlepsza jakość)
- Konkretny provider dostarcza:
  - URL: `http://server.com:8080`
  - Username: `twoj_username`
  - Password: `twoje_haslo`

### Konfiguracja IPTV w Jellyfin (bezpośrednio)

**Metoda 1: Przez xTeVe (najlepsza dla IPTV)**
```bash
# Dodaj kontener xTeVe do CT220
docker run -d \
  --name xteve \
  --network host \
  -v /root/arr-stack/config/xteve:/config \
  -v /root/arr-stack/media:/media \
  -e TZ=Europe/Warsaw \
  --restart unless-stopped \
  ghcr.io/xteve-project/xteve:latest
```

1. Wejdź: http://192.168.11.66:34400
2. Settings → Playlist
3. Dodaj M3U URL od IPTV provider-a
4. Mapping → Map channels do EPG
5. W Jellyfin: Dashboard → Live TV → Add tuner → HDHomeRun
6. URL: http://192.168.11.66:34400

**Metoda 2: Bezpośrednio przez Tunarr**
1. Tunarr → Settings → Media Sources → Add IPTV
2. Wklej M3U URL
3. Stwórz kanał z źródła IPTV
4. Stream przez Tunarr do Jellyfin

### Przykładowy M3U URL (testowy)
```
http://iptv-org.github.io/iptv/countries/pl.m3u
```
⚠️ Tylko test - niestabilne

---

## 📋 Checklist - Kolejność Konfiguracji

### 1. Sportarr
- [ ] Utwórz konto admin
- [ ] Dodaj Root Folder (`/sports`)
- [ ] Skonfiguruj Transmission
- [ ] Dodaj w Prowlarr jako "Sonarr" app
- [ ] Dodaj pierwszą ligę do monitorowania
- [ ] Skonfiguruj Jellyfin connect

### 2. Tunarr
- [ ] Sprawdź źródła Jellyfin (Media Sources)
- [ ] Dodaj programowanie do "Movies 24/7"
- [ ] Włącz kanał
- [ ] Sprawdź XMLTV
- [ ] Dodaj HDHomeRun tuner w Jellyfin
- [ ] Stwórz dodatkowe kanały (opcjonalnie)

### 3. IPTV
- [ ] Zdecyduj: Provider vs Darmowe
- [ ] Zdobądź M3U URL (lub Xtream Codes)
- [ ] Zainstaluj xTeve lub użyj Tunarr
- [ ] Dodaj playlistę
- [ ] Skonfiguruj EPG (program TV)
- [ ] Dodaj tuner w Jellyfin

---

## 🔧 Troubleshooting

### Sportarr
- **Brak indexerów**: Sprawdź Prowlarr Apps → Sportarr sync
- **Nie pobiera**: Upewnij się że Transmission jest dostępny
- **Brak wydarzeń**: Dodaj ligi ręcznie przez Search

### Tunarr
- **Puste XMLTV**: Dodaj programowanie do kanału
- **Brak źródeł Jellyfin**: Sprawdź Settings → Media Sources
- **Kanał nie działa**: Upewnij się że jest włączony (toggle ON)

### IPTV
- **Kanały nie działają**: Zmień provider-a
- **Brak EPG**: Dodaj XMLTV source w xTeVe/Tunarr
- **Zwolnione streamy**: Sprawdź bandwidth serwera

---

## 📞 Dalsza pomoc

Jeśli potrzebujesz:
- Konfiguracji konkretnego IPTV provider-a
- Dodania konkretnych lig w Sportarr
- Tworzenia specyficznych kanałów w Tunarr

Daj znać - pomogę!
