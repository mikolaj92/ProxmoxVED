#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Finalna próba dodania bibliotek przez API ===\n")

# Try 1: Minimal JSON with Name in body
print("1. Próba z Name w body...")
try:
    data1 = {"Name": "TV Shows", "CollectionType": "tvshows", "Paths": ["/root/arr-stack/media/tv"]}
    req1 = urllib.request.Request(
        f"{base}/Library/VirtualFolders?api_key={api_key}&refreshLibrary=false",
        data=json.dumps(data1).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req1) as r:
        print(f"  Status: {r.status}")
        print(f"  Response: {r.read(500)}")
except Exception as e:
    print(f"  ERROR: {e}")

# Try 2: With pathInfos
print("\n2. Próba z PathInfos...")
try:
    data2 = {
        "Name": "TV Shows",
        "CollectionType": "tvshows",
        "PathInfos": [{"Path": "/root/arr-stack/media/tv"}]
    }
    req2 = urllib.request.Request(
        f"{base}/Library/VirtualFolders?api_key={api_key}",
        data=json.dumps(data2).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req2) as r:
        print(f"  Status: {r.status}")
        print(f"  Response: {r.read(500)}")
except Exception as e:
    print(f"  ERROR: {e}")

# Try 3: Lowercase names
print("\n3. Próba z lowercase names...")
try:
    data3 = {"name": "TV Shows", "collectionType": "tvshows", "paths": ["/root/arr-stack/media/tv"]}
    req3 = urllib.request.Request(
        f"{base}/Library/VirtualFolders?api_key={api_key}",
        data=json.dumps(data3).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req3) as r:
        print(f"  Status: {r.status}")
        print(f"  Response: {r.read(500)}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n4. Sprawdzam biblioteki...")
try:
    libs = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    print(f"  Libraries: {len(libs)}")
    for lib in libs:
        print(f"    - {lib.get('Name')}: {lib.get('Locations', [])}")
except Exception as e:
    print(f"  ERROR: {e}")
