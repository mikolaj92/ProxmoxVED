#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
base = "http://localhost:8096"

print("=== Dodaję ścieżkę do istniejącej biblioteki TV Shows ===")

# Get library details
try:
    libs = json.load(urllib.request.urlopen(f"{base}/Library/VirtualFolders?api_key={api_key}"))
    tv_lib = [l for l in libs if l.get('Name') == 'TV Shows'][0]
    item_id = tv_lib.get('ItemId')

    print(f"TV Shows ItemId: {item_id}")
    print(f"Current Locations: {tv_lib.get('Locations', [])}")

    # Try to update library - but this may not work via API
    # Instead, trigger a scan and see if it finds the folder
    print(f"\nUruchamiam skan biblioteki...")

    scan_req = urllib.request.Request(
        f"{base}/Items/{item_id}/Refresh?api_key={api_key}",
        data=json.dumps({}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    with urllib.request.urlopen(scan_req) as r:
        result = json.load(r)
        print(f"Skanowanie uruchomione: {result.get('State', 'N/A')}")

    print(f"\nPoczekaj 10 sekund...")
    import time
    time.sleep(10)

    # Check if items were found
    items = json.load(urllib.request.urlopen(f"{base}/Items?api_key={api_key}&Recursive=true&ParentId={item_id}&limit=20"))
    print(f"\nZnaleziono items: {items.get('TotalRecordCount')}")
    for item in items.get('Items',[])[:10]:
        print(f"  - {item.get('Name')} ({item.get('Type')})")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
