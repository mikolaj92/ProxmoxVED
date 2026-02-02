#!/bin/bash
# ARR Stack Auto-Installer using Proxmox VE Helper Scripts
# Run this in Proxmox Web UI: Datacenter → pve → Shell

echo "============================================================"
echo "🎯 ARR STACK AUTO-INSTALLER"
echo "============================================================"
echo ""
echo "This will install:"
echo "  • Prowlarr (CT 220)"
echo "  • Sonarr (CT 221)"
echo "  • Radarr (CT 222)"
echo "  • Lidarr (CT 223)"
echo "  • Jellyfin (CT 224)"
echo ""
echo "Press Enter to continue or Ctrl+C to cancel..."
read

# Common settings
CT_PASSWORD="arrstack"  # Change this!
STORAGE="local-lvm"
CORES=2
RAM=8192
BRIDGE="vmbr0"

# Install Prowlarr (CT 220)
echo ""
echo "📦 Installing Prowlarr..."
curl -sL https://github.com/tteck/Proxmox/raw/main/ct/prowlarr.sh | bash

# Install Sonarr (CT 221)
echo ""
echo "📦 Installing Sonarr..."
curl -sL https://github.com/tteck/Proxmox/raw/main/ct/sonarr.sh | bash

# Install Radarr (CT 222)
echo ""
echo "📦 Installing Radarr..."
curl -sL https://github.com/tteck/Proxmox/raw/main/ct/radarr.sh | bash

# Install Lidarr (CT 223)
echo ""
echo "📦 Installing Lidarr..."
curl -sL https://github.com/tteck/Proxmox/raw/main/ct/lidarr.sh | bash

# Install Jellyfin (CT 224)
echo ""
echo "📦 Installing Jellyfin..."
curl -sL https://github.com/tteck/Proxmox/raw/main/ct/jellyfin.sh | bash

echo ""
echo "============================================================"
echo "🎉 ARR STACK INSTALLATION COMPLETE!"
echo "============================================================"
echo ""
echo "Check container IPs with: pct config <CTID>"
echo "SSH into container: pct enter <CTID>"
echo "============================================================"
