#!/usr/bin/env python3
"""
Deploy ARR Stack to Proxmox with better error handling
"""

from proxmoxer import ProxmoxAPI
import subprocess
import time
import sys

# API Token credentials
HOST = "192.168.11.199:8006"
USER = "root@pam"
TOKEN_NAME = "mini_m4_1_bot"
TOKEN_VALUE = "07099881-6fcc-4498-ab50-3df80f180c6e"

print("="*60)
print("🚀 PROXMOX ARR STACK DEPLOYMENT v2")
print("="*60)

# Connect to Proxmox
print("\n🔐 Connecting to Proxmox...")
try:
    proxmox = ProxmoxAPI(
        HOST,
        user=USER,
        token_name=TOKEN_NAME,
        token_value=TOKEN_VALUE,
        verify_ssl=False
    )
    version = proxmox.version.get()
    print(f"✅ Connected! Proxmox VE {version['version']}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# Find free container ID starting from 220
print("\n🔍 Finding free container ID...")
containers = proxmox.nodes('pve').lxc.get()
used_ids = [ct['vmid'] for ct in containers]
container_id = 220
while container_id in used_ids:
    container_id += 1
print(f"✅ Container ID: {container_id}")

# Check if container exists and delete if needed
print(f"\n🔍 Checking if container {container_id} exists...")
try:
    existing = proxmox.nodes('pve').lxc(container_id).status.current.get()
    print(f"⚠️ Container {container_id} exists (status: {existing['status']})")
    print(f"   Deleting...")

    if existing['status'] == 'running':
        print(f"   → Stopping...")
        proxmox.nodes('pve').lxc(container_id).status.stop.post()
        for i in range(30):
            try:
                proxmox.nodes('pve').lxc(container_id).status.current.get()
                time.sleep(1)
            except:
                break
        print(f"   ✅ Stopped")

    print(f"   → Deleting...")
    proxmox.nodes('pve').lxc(container_id).delete()
    print(f"   ✅ Deleted")
    time.sleep(3)

except Exception as e:
    error_str = str(e).lower()
    if "does not exist" in error_str or "404" in error_str or "doesn't exist" in error_str:
        print(f"✅ Container {container_id} does not exist, ready to create")
    else:
        print(f"⚠️ Unexpected error: {e}")
        print(f"   Continuing anyway...")

# Create LXC container
print(f"\n📦 Creating LXC container: arr-stack")
try:
    proxmox.nodes('pve').lxc.create(
        vmid=container_id,
        ostemplate='local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst',
        hostname='arr-stack',
        cores=4,
        memory=8192,
        swap=2048,
        storage='local-lvm',
        rootfs='local-lvm:32',
        net0='name=eth0,bridge=vmbr0,ip=dhcp',
        onboot=1,
        start=1
    )
    print(f"✅ Container created successfully!")
except Exception as e:
    print(f"❌ Failed to create container: {e}")
    print(f"\n💡 Troubleshooting:")
    print(f"   1. Check if Ubuntu 22.04 template is downloaded")
    print(f"   2. Check storage space: pvesh get /nodes/pve/storage")
    print(f"   3. Check token permissions")
    sys.exit(1)

# Wait for container to start
print(f"\n⏳ Waiting for container to fully start...")
time.sleep(20)

# Verify container is running
try:
    status = proxmox.nodes('pve').lxc(container_id).status.current.get()
    print(f"✅ Container status: {status['status']}")
    if status['status'] != 'running':
        print(f"❌ Container not running! Status: {status['status']}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Cannot get container status: {e}")
    sys.exit(1)

print(f"\n🎉 CONTAINER READY!")
print(f"   CT ID: {container_id}")
print(f"   Hostname: arr-stack")
print(f"   Status: Running")
print(f"\n📝 Next steps:")
print(f"   pct exec {container_id} -- bash -c '$(curl -fsSL https://raw.githubusercontent.com/arr-stack/install/main/install.sh)'")
print(f"\n⏳ Or run manual install:")
print(f"   pct enter {container_id}")
print(f"   Then follow: /Users/mini-m4-1/clawd/skills/proxmox/ARR_DEPLOYMENT_GUIDE.md")
