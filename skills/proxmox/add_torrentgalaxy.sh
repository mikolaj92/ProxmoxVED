#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Add TorrentGalaxy ==")

urls = ["https://torrentgalaxy.to", "https://torrentgalaxy.mx", "https://tgx.rs"]

for url in urls:
    print(f"  Trying {url}...", end=' ')

    config = {
        "definitionName": "torrentgalaxyclone",
        "name": "TorrentGalaxy",
        "implementation": "Cardigann",
        "configContract": "CardigannSettings",
        "enable": True,
        "redirect": False,
        "appProfileId": 1,
        "priority": 25,
        "baseUrl": url,
        "fields": [
            {"order": 0, "name": "definitionFile", "value": "torrentgalaxyclone"},
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
            print(f"OK (ID: {result.get('id')})")
            break
    except urllib.error.HTTPError as e:
        error_resp = e.read().decode('utf-8')
        if "Name does not resolve" in error_resp or "connect" in error_resp.lower():
            print("FAIL (connection)")
            continue
        else:
            print(f"FAIL (HTTP {e.code})")
            print(f"  Details: {error_resp[:300]}")
            break
    except Exception as e:
        print(f"FAIL ({str(e)[:100]})")
        break

print("\n== Verify all indexers ==")
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n== Sync with Sonarr/Radarr ==")
try:
    sync_req = urllib.request.Request(
        f"{base_url}/command?apikey={api_key}",
        data=json.dumps({"name": "ApplicationIndexerSync"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(sync_req) as r:
        result = json.load(r)
        print(f"Sync command sent: {result.get('name')}")
except Exception as e:
    print(f"ERROR: {e}")
