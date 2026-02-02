#!/usr/bin/env python3
import json, urllib.request

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Jellyfin Status ===")

# Check if wizard is needed
try:
    wizard = json.load(urllib.request.urlopen(f"{base}/Startup/Configuration?api_key={api_key}"))
    print(f"Wizard completed: {wizard.get('IsWizardCompleted')}")
except:
    print("Wizard check failed")

# Check libraries
try:
    libs = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    print(f"\nLibraries: {len(libs)}")
    for lib in libs:
        name = lib.get('Name')
        coll_type = lib.get('CollectionType')
        locs = lib.get('Locations', [])
        print(f"  - {name} ({coll_type})")
        print(f"    Locations: {locs}")
except Exception as e:
    print(f"Libraries check failed: {e}")

# Get items
try:
    items = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&limit=10"))
    print(f"\nTotal items: {items.get('TotalRecordCount')}")
    for item in items.get('Items',[])[:5]:
        print(f"  - {item.get('Name')} ({item.get('Type')})")
except Exception as e:
    print(f"Items check failed: {e}")

print("\n=== Direct Links ===")
print(f"Dashboard: {base}/dashboard.html")
print(f"Libraries: {base}/web/index.html#/dashboard/libraries.html")
print(f"Add Library: {base}/web/index.html#/wizard/library.html")
print(f"TV Shows: {base}/web/index.html#/details.html?type=CollectionFolder&id=767bffe4f11c93ef34b805451a696a4e")
