#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Test different indexer URLs ==")

indexers_to_try = [
    {
        "definitionName": "yts",
        "name": "YTS",
        "urls": ["https://yts.lt", "https://yts.am", "https://yts.unblockit.download"]
    },
    {
        "definitionName": "1337x",
        "name": "1337x",
        "urls": ["https://1337x.to", "https://1337x.st", "https://x1337x.ws"]
    },
    {
        "definitionName": "thepiratebay",
        "name": "The Pirate Bay",
        "urls": ["https://thepiratebay.org", "https://tpb.party", "https://thepiratebay.party"]
    }
]

for idx_def in indexers_to_try:
    print(f"\n=== Testing {idx_def['name']} ===")

    for url in idx_def['urls']:
        print(f"  Trying {url}...")

        config = {
            "definitionName": idx_def['definitionName'],
            "name": idx_def['name'],
            "implementation": "Cardigann",
            "configContract": "CardigannSettings",
            "enable": True,
            "redirect": False,
            "appProfileId": 1,
            "priority": 25,
            "baseUrl": url,
            "fields": [
                {"order": 0, "name": "definitionFile", "value": idx_def['definitionName']},
                {"order": 1, "name": "baseUrl", "value": url}
            ]
        }

        try:
            req = urllib.request.Request(
                f"{base_url}/indexer?apikey={api_key}",
                data=json.dumps(config).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                result = json.load(r)
                print(f"    ✓ SUCCESS! ID: {result.get('id')}")
                print(f"      Name: {result.get('name')}")
                break  # Success, try next indexer
        except urllib.error.HTTPError as e:
            error_resp = e.read().decode('utf-8')
            if "Name does not resolve" in error_resp or "connect" in error_resp.lower():
                print(f"    ✗ Connection failed")
                continue
            else:
                print(f"    ✗ HTTP {e.code}: {error_resp[:200]}")
                break
        except Exception as e:
            print(f"    ✗ ERROR: {str(e)[:200]}")
            break

print("\n== Verify all indexers =="
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total: {len(indexers)}")
    for idx in indexers:
        print(f"  • {idx.get('name')}: {idx.get('implementation')}, enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")
