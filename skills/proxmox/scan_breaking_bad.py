#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Szukam Breaking Bad ===")

try:
    items = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&searchTerm=Breaking%20Bad&includeItemTypes=Episode"))
    print(f"Znaleziono: {items.get('TotalRecordCount')}")

    for item in items.get('Items',[])[:10]:
        sn = item.get('ParentIndexNumber')
        en = item.get('IndexNumber')
        name = item.get('Name')
        print(f"  S{sn}E{en}: {name}")

    if items.get('TotalRecordCount') == 0:
        print("\nBreaking Bad nie znaleziony.")
        print("Spróbuję ręcznie dodać ścieżkę do biblioteki...")

except Exception as e:
    print(f"ERROR: {e}")

# Try triggering a full library scan
print("\n=== Uruchamiam skan biblioteki ===")
try:
    scan_req = urllib.request.Request(
        f"{base}/ScheduledTasks/Running/Refresh%20Library?api_key={api_key}",
        data=b'{}',
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(scan_req) as r:
        print("Skan uruchomione")
except Exception as e:
    print(f"ERROR: {e}")
