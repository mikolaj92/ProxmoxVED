# 🎬 Media Server Dashboard

## 🖥️ ARR Stack (CT220: 192.168.11.66)

### Core Services
- [**Prowlarr**](http://192.168.11.66:9696) - Indexer Management (port 9696)
- [**Sonarr**](http://192.168.11.66:8989) - TV Shows (port 8989)
- [**Radarr**](http://192.168.11.66:7878) - Movies (port 7878)
- [**Bazarr**](http://192.168.11.66:6767) - Subtitles (port 6767)

### Additional Services
- [**Readarr**](http://192.168.11.66:8787) - Books (port 8787)
- [**Lidarr**](http://192.168.11.66:8686) - Music (port 8686)

### Request & Download
- [**Jellyseerr**](http://192.168.11.66:5055) - Media Requests (port 5055)
- [**Transmission**](http://192.168.11.66:9091) - Torrent Client (port 9091)

### 🆕 New Services
- [**Sportarr**](http://192.168.11.66:1867) - Sports PVR (port 1867)
- [**Tunarr**](http://192.168.11.66:8000) - Live TV Channels (port 8000)

---

## 📺 Jellyfin (CT230: 192.168.11.70)

### Main Interface
- [**Jellyfin Web UI**](http://192.168.11.70:8096) - Media Server (port 8096)

### Admin Dashboard
- [**Dashboard**](http://192.168.11.70:8096/web/index.html#/dashboard.html)
- [**Live TV**](http://192.168.11.70:8096/web/index.html#/livetv.html)
- [**Tasks**](http://192.168.11.70:8096/web/index.html#/tasks.html)

---

## 🔧 Configuration Links

### Tunarr Resources
- **XMLTV**: http://192.168.11.66:8000/xmltv.xml
- **M3U** (po dodaniu programowania): http://192.168.11.66:8000/lineups.m3u
- **API Status**: http://192.168.11.66:8000/api/status

### Sportarr API
- **Base URL**: http://192.168.11.66:1867/api/v1
- **Get API Key**: Settings → General → API Key

---

## 📝 Quick Setup Checklist

### Sportarr (Sports Events)
- [ ] Utwórz konto admin na http://192.168.11.66:1867
- [ ] Dodaj Root Folder: `/sports`
- [ ] Skonfiguruj Transmission
- [ ] Dodaj w Prowlarr jako "Sonarr" (Apps)
- [ ] Dodaj ligę do monitorowania

### Tunarr (Custom Channels)
- [ ] Otwórz http://192.168.11.66:8000
- [ ] Channels → "Movies 24/7" → Programming
- [ ] Add Programming → Source: Jellyfin Movies → Type: Flex
- [ ] Włącz kanał (toggle ON)
- [ ] Sprawdź XMLTV: http://192.168.11.66:8000/xmltv.xml
- [ ] Dodaj HDHomeRun tuner w Jellyfin

### IPTV (Live TV Channels)
- [ ] Zdobądź M3U URL od IPTV provider-a
- [ ] Uruchom xTeVe: `bash /Users/mini-m4-1/clawd/setup-iptv.sh`
- [ ] Otwórz http://192.168.11.66:34400
- [ ] Dodaj playlistę (Settings → Playlist)
- [ ] Dodaj tuner w Jellyfin (HDHomeRun)

---

## 📚 Documentation

- [Kompletny Przewodnik](memory/2026-02-01-kompletny-przewodnik.md)
- [Tunarr Auto Config](memory/2026-02-01-tunarr-auto-config.md)
- [Tunarr Setup](memory/2026-02-01-tunarr-setup.md)

---

## 🗄️ Storage Paths

### CT220
- Media: `/root/arr-stack/media/`
  - Movies: `/root/arr-stack/media/movies/`
  - TV: `/root/arr-stack/media/tv/`
  - Sports: `/root/arr-stack/media/sports/`
  - Downloads: `/root/arr-stack/media/downloads/`
- Config: `/root/arr-stack/config/`

### CT230
- Media: `/media/` (mount from host `/srv/media`)
- Config: `/config/data/` (mount from host `/srv/appdata/jellyfin`)

### Host (192.168.11.199)
- Shared Media: `/srv/media/`
- Jellyfin Config: `/srv/appdata/jellyfin/`

---

## 🔑 API Keys

### Prowlarr
- API: `8c6dca6adf3644ba9a7981b736ef636f`

### Bazarr
- API: `b081e213d5c6f981f2954277044e8454`

### Readarr
- API: `2d3e8dae98f644b992dc5327ebf2d992`

### Jellyfin
- API: `a3dd99094b9e4b38b5afd2e2cb4af390`

### Transmission
- Username: `transmission`
- Password: `Test123`

---

## 🚀 Quick Commands

### Restart Containers
```bash
ssh root@192.168.11.199 "pct exec 220 -- docker restart sportarr tunarr"
```

### View Logs
```bash
# Sportarr
ssh root@192.168.11.199 "pct exec 220 -- docker logs -f sportarr"

# Tunarr
ssh root@192.168.11.199 "pct exec 220 -- docker logs -f tunarr"
```

### Check Status
```bash
ssh root@192.168.11.199 "pct exec 220 -- docker ps --format 'table {{.Names}}\t{{.Status}}'"
```

---

## 📞 Need Help?

Jeśli potrzebujesz pomocy z:
- Konfiguracją konkretnego serwisu
- Dodawaniem lig/druzyn w Sportarr
- Tworzeniem kanałów w Tunarr
- Ustawieniem IPTV

Daj znać! 😊
