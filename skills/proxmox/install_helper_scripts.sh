#!/bin/bash
# Install Proxmox VE Helper Scripts on Proxmox host
# Run this on Proxmox: (pve) → Shell

echo "📦 Installing Proxmox VE Helper Scripts..."

# Download and install
bash -c "$(wget -qLO - https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)" || \
bash -c "$(curl -sL https://github.com/tteck/Proxmox/raw/main/misc/post-pve-install.sh)"

echo "✅ Scripts installed!"
echo ""
echo "📚 Available commands:"
echo "   - pct-create     : Create LXC container"
echo "   - pct-update     : Update container"
echo "   - pct-backup     : Backup container"
echo "   - pct-restore    : Restore container"
echo "   - And many more!"
echo ""
echo "🔗 Docs: https://tteck.github.io/Proxmox/"
