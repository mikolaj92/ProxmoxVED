#!/bin/bash
# Skrypt pomocniczy do konfiguracji IPTV
# Użytkownik: root@192.168.11.199
# Container: CT220

echo "=== Konfiguracja xTeVe dla IPTV ==="

# Zatrzymaj jeśli istnieje
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "pct exec 220 -- docker stop xteve 2>/dev/null || true"
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "pct exec 220 -- docker rm xteve 2>/dev/null || true"

# Utwórz config directory
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "pct exec 220 -- mkdir -p /root/arr-stack/config/xteve"

# Uruchom xTeVe
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "pct exec 220 -- docker run -d \
  --name xteve \
  --network host \
  -v /root/arr-stack/config/xteve:/config \
  -v /root/arr-stack/media:/media \
  -e TZ=Europe/Warsaw \
  --restart unless-stopped \
  ghcr.io/xteve-project/xteve:latest"

echo "xTeVe uruchomiony na porcie 34400"
echo "Web UI: http://192.168.11.66:34400"
echo ""
echo "Następne kroki:"
echo "1. Otwórz http://192.168.11.66:34400"
echo "2. Settings → Playlist → Dodaj M3U URL od IPTV provider-a"
echo "3. W Jellyfin: Dashboard → Live TV → Add HDHomeRun tuner"
echo "4. URL: http://192.168.11.66:34400"
