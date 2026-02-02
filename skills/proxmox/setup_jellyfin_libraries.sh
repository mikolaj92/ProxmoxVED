#!/usr/bin/env python3
import json, urllib.request, sys, time

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base_url = "http://192.168.11.66:8096"

print("== Jellyfin: add TV library =="/)

# Add TV library
tv_config = {
    "Name": "TV Shows",
    "CollectionType": "tvshows",
    "Locations": ["/root/arr-stack/media/tv"],
    "RefreshLibrary": True
}

try:
    tv_req = urllib.request.Request(
        f"{base_url}/Library/VirtualFolders?api_key={api_key}",
        data=json.dumps(tv_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(tv_req) as r:
        print("TV library added successfully")
except Exception as e:
    print(f"ERROR adding TV library: {e}")

print()
print("== Jellyfin: add Movies library =="/)

# Add Movies library
movies_config = {
    "Name": "Movies",
    "CollectionType": "movies",
    "Locations": ["/root/arr-stack/media/movies"],
    "RefreshLibrary": True
}

try:
    movies_req = urllib.request.Request(
        f"{base_url}/Library/VirtualFolders?api_key={api_key}",
        data=json.dumps(movies_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(movies_req) as r:
        print("Movies library added successfully")
except Exception as e:
    print(f"ERROR adding Movies library: {e}")

print()
print("Waiting 10 seconds for scan...")
time.sleep(10)

print()
print("== Verify libraries ==")

try:
    libraries = json.load(urllib.request.urlopen(f"{base_url}/Library/VirtualFolders?api_key={api_key}"))
    print(f"Total libraries: {len(libraries)}")
    for lib in libraries:
        print(f"  - {lib.get('Name')}: {lib.get('CollectionType')}")
        print(f"    Path: {lib.get('Locations', [])}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("== Check items ==")

try:
    items = json.load(urllib.request.urlopen(f"{base_url}/Items?api_key={api_key}&Recursive=true&limit=20"))
    print(f"Total items: {items.get('TotalRecordCount')}")
    for item in items.get('Items', [])[:10]:
        print(f"  - {item.get('name')} ({item.get('type')})")
except Exception as e:
    print(f"ERROR: {e}")
