#!/bin/bash
# Add Transmission to ARR stack
CONTAINER_IP="192.168.11.66"

echo "🚗 Adding Transmission to ARR stack..."
echo ""

# Create config directory
echo "→ Creating directories..."
mkdir -p ~/arr-stack/config/transmission
mkdir -p ~/arr-stack/downloads/complete
mkdir -p ~/arr-stack/downloads/incomplete
echo " ✅"
echo ""

# Stop ARR stack temporarily
echo "→ Stopping ARR stack..."
cd ~/arr-stack
/usr/local/bin/docker-compose stop
echo " ✅"
echo ""

# Add Transmission to docker-compose.yml
echo "→ Adding Transmission to docker-compose.yml..."

# Backup existing compose
cp docker-compose.yml docker-compose.yml.backup

# Create new compose with Transmission
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
EOF

echo " ✅ docker-compose.yml updated"
echo ""

# Pull Transmission image
echo "→ Pulling Transmission image..."
/usr/local/bin/docker-compose pull transmission
echo " ✅"
echo ""

# Start all containers
echo "→ Starting ARR stack with Transmission..."
/usr/local/bin/docker-compose up -d
echo " ✅"
echo ""

# Wait for Transmission to start
sleep 5

# Get container IP
IP=$(ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

echo ""
echo "============================================================"
echo "🎉 TRANSMISSION ADDED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "🚗 Transmission Web UI: http://${IP}:9091"
echo "   Username: transmission"
echo "   Password: transmission123"
echo ""
echo "📱 Download folder: ~/arr-stack/media/downloads/"
echo ""
echo "🔧 Next steps:"
echo "   1. Open Transmission: http://${IP}:9091"
echo "   2. Test with a small torrent"
echo "   3. Add Transmission to Sonarr/Radarr/Lidarr:"
echo "      → Settings → Download Client → Add"
echo "      → Type: Transmission"
echo "      → Host: ${IP}"
echo "      → Port: 9091"
echo "      → Username: transmission"
echo "      "Password: transmission123"
echo ""
echo "============================================================"
