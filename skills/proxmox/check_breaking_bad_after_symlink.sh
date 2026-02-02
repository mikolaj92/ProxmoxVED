#!/usr/bin/env python3
import json, urllib.request, time

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Sprawdzam Breaking Bad po symlink ===")

# Search for series
try:
    items = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking%20Bad&includeItemTypes=Series"))
    print(f"Series znaleziono: {items.get('TotalRecordCount')}")
    for item in items.get('Items',[]):
        print(f"  - {item.get('Name')}")
        print(f"    Path: {item.get('Path')}")
        print(f"    ID: {item.get('Id')}")
except Exception as e:
    print(f"ERROR: {e}")

# Search for episodes
try:
    eps = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking&includeItemTypes=Episode&limit=20"))
    print(f"\nOdcinki znaleziono: {eps.get('TotalRecordCount')}")
    for item in eps.get('Items',[])[0:10]:
        sn = item.get('ParentIndexNumber', '?')
        en = item.get('IndexNumber', '?')
        print(f"  - S{sn}E{en}: {item.get('Name')[:60]}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nOczekam 5 sekund na skan...")
time.sleep(5)

# Try scan library
try:
    scan = urllib.request.urlopen(f"{base}/Items/767bffe4f11c93ef34b805451a696a4e/Refresh?api_key={api_key}", data=b'{}', headers={'Content-Type': 'application/json'}, method='POST')
    print(f"Skan wysłany: {scan.status}")
except Exception as e:
    print(f"Skan error: {e}")

time.sleep(10)

# Check again
print("\nPo skanie:")
try:
    items2 = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking%20Bad&includeItemTypes=Series"))
    print(f"Series: {items2.get('TotalRecordCount')}")
    eps2 = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking&includeItemTypes=Episode&limit=20"))
    print(f"Odcinki: {eps2.get('TotalRecordCount')}")
except Exception as e:
    print(f"ERROR: {e}")
