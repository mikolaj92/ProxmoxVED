#!/usr/bin/env python3
import json, urllib.request, sys, time

print("== Prowlarr: Test release search (different endpoint) ==")

# Try release endpoint with query params
release_url = "http://192.168.11.66:9696/api/v1/release?apikey=8c6dca6adf3644ba9a7981b736ef636f&query=Breaking%20Bad&categories=5000&limit=10&type=search"

try:
    with urllib.request.urlopen(release_url, timeout=60) as r:
        results = json.load(r)
        print(f"Found {len(results)} results")
        for res in results[:5]:
            print(f"  - {res.get('title')}")
            print(f"    indexer: {res.get('indexer', 'N/A')}")
            print(f"    size: {res.get('size', 0)/(1024*1024):.1f} MB")
            print(f"    seeders: {res.get('seeders', 0)}")
            print()
except Exception as e:
    print(f"ERROR: {e}")
