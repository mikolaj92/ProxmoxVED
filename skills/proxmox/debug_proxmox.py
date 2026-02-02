#!/usr/bin/env python3
"""Debug Proxmox storage and templates"""
from proxmoxer import ProxmoxAPI

proxmox = ProxmoxAPI(
    "192.168.11.199:8006",
    user='root@pam',
    token_name='mini_m4_1_bot',
    token_value='07099881-6fcc-4498-ab50-3df80f180c6e',
    verify_ssl=False
)

print("💾 STORAGE STATUS:\n")
storage = proxmox.nodes('pve').storage.get()
for s in storage:
    if s.get('content') and 'rootdir' in s.get('content', ''):
        used = s.get('used', 0)
        total = s.get('total', 1)
        avail = total - used
        pct = (used / total * 100) if total > 0 else 0
        print(f"📦 {s.get('storage')}:")
        print(f"   Type: {s.get('type')}")
        print(f"   Used: {pct:.1f}%")
        print(f"   Available: {avail / 1024**3:.1f} GB")
        print(f"   Content: {s.get('content')}")
        print()

print("\n📋 TEMPLATES:\n")
templates = proxmox.nodes('pve').aplinfo.get()
ubuntu_22 = [t for t in templates if 'ubuntu' in t.get('template', '').lower() and '22.04' in t.get('template', '')]
if ubuntu_22:
    print("✅ Ubuntu 22.04 templates available:")
    for t in ubuntu_22[:5]:
        print(f"   • {t.get('template')}")
else:
    print("❌ No Ubuntu 22.04 templates found!")

print("\n🔍 RECENT TASKS:\n")
try:
    tasks = proxmox.nodes('pve').tasks.get(limit=10)
    for task in tasks:
        if task.get('type') in ['lxc', 'vzcreate']:
            print(f"   • {task.get('type')} - {task.get('status')} - {task.get('upid')}")
except:
    print("   Could not fetch tasks")
