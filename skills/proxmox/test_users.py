#!/usr/bin/env python3
"""
Test different username formats
"""

from proxmoxer import ProxmoxAPI

password = "sooyosoyo"
host = "192.168.11.199:8006"

users = [
    "root@pam",
    "root@pve",
    "root",
    "root@realm",
]

for user in users:
    print(f"\n🔑 Trying user: {user}")
    try:
        proxmox = ProxmoxAPI(
            host,
            user=user,
            password=password,
            verify_ssl=False,
            timeout=10
        )
        version = proxmox.version.get()
        print(f"✅ SUCCESS! User: {user}")
        print(f"   Proxmox VE {version['version']}")
        print(f"   Hostname: {version.get('hostname', 'N/A')}")
        print(f"\n   ✓ CORRECT CREDENTIALS:")
        print(f"     Host: {host}")
        print(f"     User: {user}")
        print(f"     Password: {password}")
        break
    except Exception as e:
        error = str(e)
        if "authenticate" in error.lower():
            print(f"❌ Authentication failed - wrong user or password")
        else:
            print(f"❌ {error[:80]}")
