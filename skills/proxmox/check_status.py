#!/usr/bin/env python3
"""Check Proxmox container status"""
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(
    "192.168.11.199:8006",
    user='root@pam',
    token_name='mini_m4_1_bot',
    token_value='07099881-6fcc-4498-ab50-3df80f180c6e',
    verify_ssl=False
)

print("📊 Proxmox Container Status:\n")

try:
    # Check container 200
    try:
        status = proxmox.nodes('pve').lxc(200).status.current.get()
        print(f"✅ Container 200: {status['status']}")
        print(f"   CPU: {status.get('cpu', 'N/A')}")
        print(f"   Memory: {status.get('mem', 0) / 1024 / 1024:.0f} MB")
        print(f"   MaxMem: {status.get('maxmem', 0) / 1024 / 1024:.0f} MB")
    except Exception as e:
        print(f"❌ Container 200 error: {e}")

    # List all containers
    print(f"\n📋 All containers:")
    containers = proxmox.nodes('pve').lxc.get()
    for ct in containers:
        print(f"   • CT {ct['vmid']}: {ct.get('name', 'N/A')} - {ct['status']}")

except Exception as e:
    print(f"❌ Error: {e}")
