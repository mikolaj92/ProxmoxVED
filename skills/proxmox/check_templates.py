#!/usr/bin/env python3
"""Check available Proxmox templates"""
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(
    "192.168.11.199:8006",
    user='root@pam',
    token_name='mini_m4_1_bot',
    token_value='07099881-6fcc-4498-ab50-3df80f180c6e',
    verify_ssl=False
)

print("📋 Available LXC Templates:")
templates = proxmox.nodes('pve').aplinfo.get()
ubuntu_templates = [t for t in templates if 'ubuntu' in t.get('template', '').lower() and '22.04' in t.get('template', '')]

if ubuntu_templates:
    print(f"\n✅ Found Ubuntu 22.04 templates:")
    for t in ubuntu_templates[:3]:
        print(f"   • {t.get('template', 'N/A')}")
        print(f"     Size: {t.get('size', 'N/A')}")
else:
    print(f"\n❌ No Ubuntu 22.04 templates found!")
    print(f"\n💡 Download in Proxmox UI:")
    print(f"   (local) → Templates → Templates → Add")
    print(f"   Search: ubuntu 22.04 standard")
    print(f"   Download any Ubuntu 22.04 template")

# Check storage
print(f"\n💾 Storage Status:")
storage = proxmox.nodes('pve').storage.get()
for s in storage:
    if s.get('type') == 'dir' or s.get('type') == 'lvm':
        used = s.get('used', 0)
        total = s.get('total', 1)
        pct = (used / total) * 100 if total > 0 else 0
        print(f"   • {s.get('storage', 'N/A')}: {pct:.1f}% used ({s.get('type', 'N/A')})")
