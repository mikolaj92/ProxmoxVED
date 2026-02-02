#!/bin/bash
# Install Overseerr using Proxmox VE Community Scripts
# This creates a new LXC container specifically for Overseerr

CT_ID=230
HOSTNAME="overseerr"
RAM=4096
STORAGE="local-lvm"
CORES=2

echo "============================================================"
echo "📋 Installing Overseerr (Media Request Manager)"
echo "============================================================"
echo ""
echo "Overseerr features:"
echo "  • Request movies/TV shows/music"
echo "  • Auto-sync with Sonarr/Radarr/Lidarr"
echo "  • User management & approvals"
echo "  • Media recommendations"
echo "  • Beautiful UI - all in one place!"
echo ""
echo "Creating container CT ${CT_ID}..."
echo ""

# Stop existing container if exists
pct stop $CT_ID 2>/dev/null
pct destroy $CT_ID 2>/dev/null

# Create container
pct create $CT_ID \
  local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst \
  --hostname $HOSTNAME \
  --cores $CORES \
  --memory $RAM \
  --swap 1024 \
  --storage $STORAGE \
  --rootfs $STORAGE:32 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --features nesting=1,keyctl=1 \
  --onboot 1 \
  --start 1

echo "✅ Container created!"
echo ""

# Wait for container to start
sleep 15

# Install Docker
echo "📦 Installing Docker..."
pct exec $CT_ID -- bash -c '
apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y curl git ca-certificates gnupg && \
install -m 0755 -d /etc/apt/keyrings && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
chmod a+r /etc/apt/keyrings/docker.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
apt-get update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io && \
docker --version
'

echo "✅ Docker installed!"
echo ""

# Pull and run Overseerr
echo "📋 Pulling Overseerr image..."
pct exec $CT_ID -- docker pull sctx/overseerr:latest

echo ""
echo "🚀 Starting Overseerr..."
pct exec $CT_ID -- docker run -d \
  --name overseerr \
  --restart unless-stopped \
  -p 5055:5055 \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Warsaw \
  -v ~/overseerr-config:/app/config \
  sctx/overseerr:latest

echo "✅ Overseerr started!"
echo ""

# Get IP
echo "🔍 Getting container IP..."
sleep 5
IP=$(pct exec $CT_ID -- ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

echo ""
echo "============================================================"
echo "🎉 OVERSEERR INSTALLED SUCCESSFULLY!"
echo "============================================================"
echo ""
echo "📱 Overseerr URL: http://${IP}:5055"
echo ""
echo "🔧 Setup steps:"
echo "   1. Open: http://${IP}:5055"
echo "   2. Create admin account"
echo "   3. Go to Settings → Servers"
echo "   4. Add servers:"
echo "      • Sonarr: http://192.168.11.66:8989 (API key: 0375672f0f64474c8843b922d0ab595e)"
echo "      • Radarr: http://192.168.11.66:7878 (API key: e2166ae2a7284752a3d6b95423485f42)"
echo "      • Lidarr: http://192.168.11.66:8686 (API key: d86ba94cd43e4501bebe77dcbad7b7cd)"
echo "      • Jellyfin: http://192.168.11.66:8096"
echo "   5. Done! All requests in one place!"
echo ""
echo "============================================================"
