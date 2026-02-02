#!/usr/bin/env python3
import json, urllib.request

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Po TopParentId update ===")

# Check library paths
try:
    libs = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    print(f"Libraries: {len(libs)}")
    for lib in libs:
        name = lib.get('Name')
        path = lib.get('Path')
        print(f"  - {name}: {path}")
except Exception as e:
    print(f"Libraries check error: {e}")

# Search for Breaking Bad
try:
    items = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking%20Bad&includeItemTypes=Series"))
    print(f"\nBreaking Bad series: {items.get('TotalRecordCount')}")
    for item in items.get('Items',[]):
        print(f"  - {item.get('Name')} (ID: {item.get('Id')})")
except Exception as e:
    print(f"Search error: {e}")

# Also check episodes
try:
    eps = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking&includeItemTypes=Episode&limit=10"))
    print(f"\nBreaking Bad episodes: {eps.get('TotalRecordCount')}")
    for item in eps.get('Items',[])[:5]:
        sn = item.get('ParentIndexNumber')
        en = item.get('IndexNumber')
        print(f"  - S{sn}E{en}: {item.get('Name')}")
except Exception as e:
    print(f"Episodes search error: {e}")
