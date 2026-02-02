#!/usr/bin/env python3
import json, urllib.request, sys, time

print("== Prowlarr: test search 'Breaking Bad S01' ==")
# Use Prowlarr search API
search_url = "http://192.168.11.66:9696/api/v1/search?apikey=8c6dca6adf3644ba9a7981b736ef636f"
search_data = json.dumps({
    "query": "Breaking Bad",
    "categories": [5000],  # TV
    "type": "search",
    "limit": 10
}).encode('utf-8')

req = urllib.request.Request(search_url, data=search_data, headers={
    'Content-Type': 'application/json'
})

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        results = json.load(r)
        print(f"Found {len(results)} results")
        for res in results[:5]:
            print(f"  - {res.get('title')}")
            print(f"    indexer: {res.get('indexer')}")
            print(f"    size: {res.get('size')}")
            print(f"    seeders: {res.get('seeders')}")
            print()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
