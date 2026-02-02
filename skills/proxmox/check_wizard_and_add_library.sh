#!/usr/bin/env python3
import json, urllib.request

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Sprawdzam wizard status ===")

try:
    wizard = json.load(urllib.request.urlopen(f"{base}/Startup/Configuration?api_key={api_key}"))
    print(f"Wizard completed: {wizard.get('IsWizardCompleted')}")
except Exception as e:
    print(f"Wizard check: {e}")

print("\n=== Libraries ===")
try:
    libs = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    print(f"Libraries: {len(libs)}")
    for lib in libs:
        print(f"  - {lib.get('Name')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== Try to add library directly ===")
try:
    # Try POST to add library
    add_data = {
        "Name": "TV Shows",
        "CollectionType": "tvshows",
        "Paths": ["/root/arr-stack/media/tv"]
    }

    req = urllib.request.Request(
        f"{base}/Library/VirtualFolders?api_key={api_key}",
        data=json.dumps(add_data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(req) as r:
        result = json.load(r)
        print(f"Dodano: {result.get('Name') if isinstance(result, dict) else result}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== Final libraries check ===")
try:
    libs2 = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    print(f"Libraries: {len(libs2)}")
    for lib in libs2:
        print(f"  - {lib.get('Name')}: {lib.get('Locations', [])}")
except Exception as e:
    print(f"ERROR: {e}")
