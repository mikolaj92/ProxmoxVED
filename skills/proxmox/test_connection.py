#!/usr/bin/env python3
"""
Test Proxmox connection with different host formats
"""

from proxmoxer import ProxmoxAPI

password = "sooyosoyo"

hosts = [
    "192.168.11.199:8006",
    "https://192.168.11.199:8006",
    "http://192.168.11.199:8006",
]

for host in hosts:
    print(f"\nTrying: {host}")
    try:
        proxmox = ProxmoxAPI(
            host,
            user='root@pam',
            password=password,
            verify_ssl=False,
            timeout=10
        )
        version = proxmox.version.get()
        print(f"✅ SUCCESS! Proxmox VE {version['version']}")
        print(f"   Hostname: {version.get('hostname', 'N/A')}")
        print(f"   This is the correct format!")
        break
    except Exception as e:
        print(f"❌ Failed: {str(e)[:100]}")
