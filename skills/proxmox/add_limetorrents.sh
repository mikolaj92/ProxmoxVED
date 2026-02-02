#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Add LimeTorrents ==")

urls = ["https://limetorrents.lol", "https://www.limetorrents.pro", "https://limetor.com"]

for url in urls:
    print(f"  Trying {url}...", end=' ')

    config = {
        "definitionName": "limetorrents",
        "name": "LimeTorrents",
        "implementation": "Cardigann",
        "configContract": "CardigannSettings",
        "enable": True,
        "redirect": False,
        "appProfileId": 1,
        "priority": 25,
        "baseUrl": url,
        "fields": [
            {"order": 0, "name": "definitionFile", "value": "limetorrents"},
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
            break
    except Exception as e:
        print(f"FAIL ({str(e)[:100]})")
        break

print("\n== All indexers ==")
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: enabled={idx.get('enable')}, impl={idx.get('implementation')}")
except Exception as e:
    print(f"ERROR: {e}")
