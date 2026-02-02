#!/usr/bin/env python3
import json, urllib.request, sys, os, glob, time

print("== Check media files in /root/arr-stack/media/ ==")

# Check if there are any files
for root, dirs, files in os.walk('/root/arr-stack/media'):
    level = root.replace('/root/arr-stack/media', '').count(os.sep)
    if level < 3:
        print(f"{root}: {len(files)} files")
        for f in files[:3]:
            print(f"  - {f}")

print()
print("== Jellyfin: check libraries ==")

# Get Jellyfin config
try:
    libraries = json.load(urllib.request.urlopen("http://192.168.11.66:8096/Library/VirtualFolders?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"))
    print(f"Libraries: {len(libraries)}")
    for lib in libraries:
        print(f"  - {lib.get('name')}: {lib.get('collectionType')}")
        print(f"    locations: {lib.get('locations')}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("== Jellyfin: scan all libraries ==")

# Trigger library refresh
try:
    refresh_url = "http://192.168.11.66:8096/Library/Refresh?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
    urllib.request.urlopen(refresh_url, data=b'', timeout=30)
    print("Refresh triggered")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("Waiting 5 seconds for scan...")
time.sleep(5)

print()
print("== Jellyfin: check items ==")

# Get items from libraries
try:
    items = json.load(urllib.request.urlopen("http://192.168.11.66:8096/Items?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888&Recursive=true&limit=20"))
    print(f"Total items: {items.get('TotalRecordCount')}")
    for item in items.get('Items', [])[:10]:
        print(f"  - {item.get('name')} ({item.get('type')})")
except Exception as e:
    print(f"ERROR: {e}")
