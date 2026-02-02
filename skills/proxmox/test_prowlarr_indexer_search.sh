#!/usr/bin/env python3
import json, urllib.request, sys, time

print("== Prowlarr: Test indexer search for 'Breaking Bad' ==")

# Prowlarr search API endpoint
search_url = "http://192.168.11.66:9696/api/v1/search?apikey=8c6dca6adf3644ba9a7981b736ef636f"

# Test search for Breaking Bad S01E01
search_data = {
    "query": "Breaking Bad",
    "indexerIds": [],
    "categories": [5000],  # TV
    "type": "search",
    "limit": 20
}

req = urllib.request.Request(
    search_url,
    data=json.dumps(search_data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
}

try:
    with urllib.request.urlopen(req, timeout=60) as r:
        results = json.load(r)
        print(f"Found {len(results)} results")
        for res in results[:5]:
            print(f"  - {res.get('title')}")
            print(f"    indexer: {res.get('indexer', {}).get('name', 'N/A')}")
            print(f"    size: {res.get('size', 0)/(1024*1024):.1f} MB")
            print(f"    seeders: {res.get('seeders', 0)}")
            print()
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n== Prowlarr: List all indexers ==")
try:
    indexers = json.load(urllib.request.urlopen("http://192.168.11.66:9696/api/v1/indexer?apikey=8c6dca6adf3644ba9a7981b736ef636f"))
    print(f"Total indexers: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")
