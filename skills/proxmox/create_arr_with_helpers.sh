#!/bin/bash
# Create ARR Stack LXC using Proxmox VE Helper Scripts
# This runs on Proxmox host after installing helper scripts

CT_ID=220
CT_HOSTNAME="arr-stack"
PASSWORD="arrstack"  # Zmień na swoje hasło!
TEMPLATE="ubuntu-22.04-standard_22.04-1_amd64.tar.zst"

echo "============================================================"
echo "🎯 Creating ARR Stack LXC with Helper Scripts"
echo "============================================================"

# Check if scripts are installed
if ! command -v pct-create &> /dev/null; then
    echo "❌ Helper scripts not installed!"
    echo "   Run: bash -c \"\$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)\""
    exit 1
fi

echo ""
echo "📦 Creating LXC container..."
echo "   CT ID: $CT_ID"
echo "   Hostname: $CT_HOSTNAME"
echo "   Template: $TEMPLATE"
echo ""

# Create container with Docker
pct-create $CT_ID $TEMPLATE \
    $PASSWORD \
    2 \
    "0.0.0.0/0" \
    4 \
    8192 \
    "arr-stack,lxc,docker" \
    "$CT_HOSTNAME" \
    "" \
    "dockertestscript"

echo ""
echo "⏳ Waiting for container to start..."
sleep 10

# Check status
if pct status $CT_ID | grep -q "status: running"; then
    echo "✅ Container started successfully!"
else
    echo "❌ Container failed to start!"
    exit 1
fi

echo ""
echo "🐳 Installing Docker inside container..."
pct exec $CT_ID -- bash -c '
apt-get update && \
apt-get install -y curl git ca-certificates gnupg && \
install -m 0755 -d /etc/apt/keyrings && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
chmod a+r /etc/apt/keyrings/docker.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \
docker --version && \
docker compose version
'

echo "✅ Docker installed!"

echo ""
echo "📁 Creating directories..."
pct exec $CT_ID -- mkdir -p ~/arr-stack/config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}
pct exec $CT_ID -- mkdir -p ~/arr-stack/media/{tv,movies,music,books,downloads}

echo "✅ Directories created!"

echo ""
echo "📝 Creating docker-compose.yml..."
pct exec $CT_ID -- bash -c 'cat > ~/arr-stack/docker-compose.yml <<'"'"'EOF'"'"'
version: '"'"'3.8'"'"'
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/prowlarr:/config
    ports:
      - 9696:9696
    restart: unless-stopped
  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/sonarr:/config
      - ./media/tv:/tv
      - ./media/downloads:/downloads
    ports:
      - 8989:8989
    restart: unless-stopped
  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/radarr:/config
      - ./media/movies:/movies
      - ./media/downloads:/downloads
    ports:
      - 7878:7878
    restart: unless-stopped
  lidarr:
    image: lscr.io/linuxserver/lidarr:latest
    container_name: lidarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/lidarr:/config
      - ./media/music:/music
      - ./media/downloads:/downloads
    ports:
      - 8686:8686
    restart: unless-stopped
  readarr:
    image: lscr.io/linuxserver/readarr:latest
    container_name: readarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/readarr:/config
      - ./media/books:/books
      - ./media/downloads:/downloads
    ports:
      - 8787:8787
    restart: unless-stopped
  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/jellyfin:/config
      - ./media:/media
    ports:
      - 8096:8096
    restart: unless-stopped
EOF
'

echo "✅ docker-compose.yml created!"

echo ""
echo "📥 Pulling Docker images (this will take 5-10 min)..."
pct exec $CT_ID -- bash -c 'cd ~/arr-stack && docker compose pull'

echo "✅ Images pulled!"

echo ""
echo "▶️  Starting containers..."
pct exec $CT_ID -- bash -c 'cd ~/arr-stack && docker compose up -d'

echo "✅ Containers started!"
sleep 5

echo ""
echo "🔍 Getting container IP..."
IP=$(pct exec $CT_ID -- ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

echo ""
echo "============================================================"
echo "🎉 ARR STACK DEPLOYED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "📱 Access URLs:"
echo "   • Prowlarr (Indexer):  http://${IP}:9696"
echo "   • Sonarr (TV Shows):   http://${IP}:8989"
echo "   • Radarr (Movies):     http://${IP}:7878"
echo "   • Lidarr (Music):      http://${IP}:8686"
echo "   • Readarr (Books):     http://${IP}:8787"
echo "   • Jellyfin (Media):    http://${IP}:8096"
echo ""
echo "🔧 Next Steps:"
echo "   1. Open each URL in browser"
echo "   2. Create admin user for each service"
echo "   3. Configure Prowlarr (add indexers)"
echo "   4. Connect Prowlarr → Apps"
echo "   5. Add download client (Transmission/qBittorrent)"
echo "   6. Setup Jellyfin media libraries"
echo ""
echo "🐧 Manage Container:"
echo "   pct enter $CT_ID        # SSH into container"
echo "   pct start $CT_ID        # Start container"
echo "   pct stop $CT_ID         # Stop container"
echo "   pct shutdown $CT_ID     # Shutdown container"
echo "============================================================"
