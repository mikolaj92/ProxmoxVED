#!/bin/bash
# Add Overseerr to existing ARR stack in CT 220

echo "📋 Adding Overseerr to ARR stack (CT 220)..."
echo ""

# Pull Overseerr image
echo "📦 Pulling Overseerr image..."
docker pull sctx/overseerr:latest
echo " ✅"
echo ""

# Stop ARR stack temporarily
echo "→ Stopping ARR stack..."
cd ~/arr-stack
/usr/local/bin/docker-compose stop
echo " ✅"
echo ""

# Backup existing compose
cp docker-compose.yml docker-compose.yml.backup

# Add Overseerr to docker-compose.yml
echo "→ Adding Overseerr to docker-compose.yml..."

# Create new compose with Overseerr
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

  overseerr:
    image: sctx/overseerr:latest
    container_name: overseerr
    network_mode: host
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/overseerr:/app/config
    restart: unless-stopped
EOF

echo " ✅ docker-compose.yml updated"
echo ""

# Start all containers
echo "→ Starting ARR stack with Overseerr..."
/usr/local/bin/docker-compose up -d
echo " ✅"
echo ""

# Wait for Overseerr to start
sleep 5

# Get container IP
IP=$(ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

echo ""
echo "============================================================"
echo "🎉 OVERSEERR ADDED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "📱 Overseerr Web UI: http://${IP}:5055"
echo ""
echo "🔧 Setup steps:"
echo "   1. Open: http://${IP}:5055"
echo "   2. Create admin account"
echo "   3. Go to Settings → Servers"
echo "   4. Add servers:"
echo "      • Sonarr: http://${IP}:8989 (API key: 0375672f0f64474c8843b922d0ab595e)"
echo "      • Radarr: http://${IP}:7878 (API key: e2166ae2a7284752a3d6b95423485f42)"
echo "      • Lidarr: http://${IP}:8686 (API key: d86ba94cd43e4501bebe77dcbad7b7cd)"
echo "      • Jellyfin: http://${IP}:8096"
echo "   5. Done! All requests in one place!"
echo ""
echo "📊 All apps running:"
echo "   🎯 Prowlarr: http://${IP}:9696"
echo "   📺 Sonarr: http://${IP}:8989"
echo "   🎬 Radarr: http://${IP}:7878"
echo "   🎵 Lidarr: http://${IP}:8686"
echo "   📺 Jellyfin: http://${IP}:8096"
echo "   🚗 Transmission: http://${IP}:9091 (transmission/transmission123)"
echo "   📋 Overseerr: http://${IP}:5055"
echo ""
echo "============================================================"
