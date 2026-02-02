#!/usr/bin/env python3
"""Download Ubuntu 22.04 template via API"""
from proxmoxer import ProxmoxAPI
import time

proxmox = ProxmoxAPI(
    "192.168.11.199:8006",
    user='root@pam',
    token_name='mini_m4_1_bot',
    token_value='07099881-6fcc-4498-ab50-3df80f180c6e',
    verify_ssl=False
)

print("⬇️  Downloading Ubuntu 22.04 template...")
print("   (this may take 5-10 minutes)\n")

try:
    # Start download
    task = proxmox.nodes('pve').aplinfo.post(
        storage='local',
        template='ubuntu-22.04-standard_22.04-1_amd64.tar.zst'
    )
    print(f"✅ Download started!")
    print(f"   Task UPID: {task}")

    # Wait for download to complete
    print(f"\n⏳ Waiting for download...")
    for i in range(600):  # 10 minutes max
        try:
            task_status = proxmox.nodes('pve').tasks(task).status.get()
            status = task_status.get('status')
            if status == 'stopped':
                exitstatus = task_status.get('exitstatus')
                if exitstatus == 'OK':
                    print(f"✅ Download completed!")
                    break
                else:
                    print(f"❌ Download failed: {exitstatus}")
                    exit(1)
        except:
            pass

        if i % 10 == 0:
            print(f"   Progress: {i//10}/60 min...")
        time.sleep(1)

    # Verify template is available
    print(f"\n🔍 Verifying template...")
    templates = proxmox.nodes('pve').storage('local').content.get()
    ubuntu_templates = [t for t in templates if 'ubuntu-22.04' in t.get('volid', '')]
    if ubuntu_templates:
        print(f"✅ Template ready:")
        for t in ubuntu_templates:
            print(f"   • {t.get('volid')}")
    else:
        print(f"❌ Template not found in storage")

except Exception as e:
    print(f"❌ Error: {e}")
