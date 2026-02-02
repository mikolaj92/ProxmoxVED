#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Add YTS using full config (like Nyaa.si) ==")

# YTS config based on schema
yts_config = {
    "definitionName": "yts",
    "name": "YTS",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": True,
    "redirect": False,
    "baseUrl": "https://yts.mx",
    "fields": [
        {
            "order": 0,
            "name": "definitionFile",
            "value": "yts"
        },
        {
            "order": 1,
            "name": "baseUrl",
            "value": "https://yts.mx"
        },
        {
            "order": 9,
            "name": "torrentBaseSettings.preferMagnetUrl",
            "value": False
        }
    ]
}

try:
    req = urllib.request.Request(
        f"{base_url}/indexer?apikey={api_key}",
        data=json.dumps(yts_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.load(r)
        print(f"SUCCESS: {result}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"ERROR: {e}")
