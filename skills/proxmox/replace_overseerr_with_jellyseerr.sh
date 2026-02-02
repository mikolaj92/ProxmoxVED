#!/bin/bash
# Remove Overseerr and install Jellyseerr

echo "🔄 Usuwam Overseerr i instaluję Jellyseerr..."
echo ""

# Stop ARR stack
echo "→ Zatrzymuję ARR stack..."
cd ~/arr-stack
/usr/local/bin/docker-compose stop
echo " ✅"
echo ""

# Remove overseerr container
echo "→ Usuwam kontener Overseerr..."
docker rm overseerr 2>/dev/null
docker rmi sctx/overseerr:latest 2>/dev/null
echo " ✅"
echo ""

# Update docker-compose.yml
echo "→ Aktualizuję docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/prowlarr:/config
    restart: unless-stopped

  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/sonarr:/config
      - ./media/tv:/tv
      - ./media/downloads:/downloads
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/radarr:/config
      - ./media/movies:/movies
      - ./media/downloads:/downloads
    restart: unless-stopped

  lidarr:
    image: lscr.io/linuxserver/lidarr:latest
    container_name: lidarr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/lidarr:/config
      - ./media/music:/music
      - ./media/downloads:/downloads
    restart: unless-stopped

  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/jellyfin:/config
      - ./media:/media
    restart: unless-stopped

  transmission:
    image: lscr.io/linuxserver/transmission:latest
    container_name: transmission
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
      - USER=transmission
      - PASS=transmission123
    volumes:
      - ./config/transmission:/config
      - ./media/downloads:/downloads
      - ./media/downloads/incomplete:/incomplete
    restart: unless-stopped

  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
      - LOG_LEVEL=info
    volumes:
      - ./config/jellyseerr:/app/config
    restart: unless-stopped
EOF

echo " ✅ docker-compose.yml z Jellyseerr"
echo ""

# Start stack
echo "→ Uruchamiam ARR stack z Jellyseerr..."
/usr/local/bin/docker-compose up -d
echo " ✅"
echo ""

# Wait for Jellyseerr
sleep 10

# Get IP
IP=$(ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

echo ""
echo "============================================================"
echo "🎉 JELLYSEERR ZAINSTALOWANE!"
echo "============================================================"
echo ""
echo "📱 Jellyseerr URL: http://${IP}:5055"
echo ""
echo "🔧 Setup steps:"
echo "   1. Otwórz: http://${IP}:5055"
echo "   2. Utwórz konto admina"
echo "   3. Połącz z Jellyfin:"
echo "      → Settings → General → Jellyfin URL"
echo "      → http://${IP}:8096"
echo "   4. Połącz z Sonarr/Radarr/Lidarr:"
echo "      → Settings → Services"
echo "      → API keys są poniżej"
echo ""
echo "📊 API Keys:"
echo "   Sonarr: 0375672f0f64474c8843b922d0ab595e"
echo "   Radarr: e2166ae2a7284752a3d6b95423485f42"
echo "   Lidarr: d86ba94cd43e4501bebe77dcbad7b7cd"
echo ""
echo "============================================================"
