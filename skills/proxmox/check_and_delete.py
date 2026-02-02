#!/usr/bin/env python3
"""
Quick script to check and delete existing container
"""

from proxmoxer import ProxmoxAPI
import sys

proxmox = ProxmoxAPI(
    '192.168.11.199:8006',
    user='root@pam',
    password='sooyosoyo',
    verify_ssl=False
)

# List containers
containers = proxmox.nodes('pve').lxc.get()
print(f"Existing containers:")
for ct in containers:
    print(f"  ID: {ct['vmid']}, Name: {ct.get('name', 'N/A')}, Status: {ct['status']}")

# Check if 106 exists
ct_106 = None
for ct in containers:
    if ct['vmid'] == 106:
        ct_106 = ct
        break

if ct_106:
    print(f"\n⚠️ Container 106 exists!")
    action = input("Delete it? (y/n): ")
    if action.lower() == 'y':
        # Stop first
        if ct_106['status'] == 'running':
            print(f"  → Stopping container...")
            proxmox.nodes('pve').lxc(106).status.stop.post()
            import time
            time.sleep(5)

        # Delete
        print(f"  → Deleting container...")
        proxmox.nodes('pve').lxc(106).delete()
        print(f"  ✅ Container 106 deleted!")
    else:
        print(f"  ❌ Aborted")
        sys.exit(1)
else:
    print(f"\n✅ Container 106 does not exist, ready to create!")
