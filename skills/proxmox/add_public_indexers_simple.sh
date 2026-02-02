#!/usr/bin/env python3
import json, urllib.request, sys, time

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Adding public indexers (Cardigann) ==")

indexers = [
    {"definitionName": "yts", "name": "YTS"},
    {"definitionName": "1337x", "name": "1337x"},
    {"definitionName": "thepiratebay", "name": "The Pirate Bay"}
]

for idx_def in indexers:
    print(f"Adding {idx_def['name']}...")
    try:
        schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))
        target_schema = None
        for s in schemas:
            if s.get('definitionName') == idx_def['definitionName']:
                target_schema = s
                break
        
        if not target_schema:
            print(f"  WARNING: Schema not found")
            continue
        
        add_config = {
            "name": idx_def['name'],
            "implementation": "Cardigann",
            "configContract": "CardigannSettings",
            "enable": True
        }
        
        req = urllib.request.Request(
            f"{base_url}/indexer?apikey={api_key}",
            data=json.dumps(add_config).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as r:
            result = json.load(r)
            print(f"  SUCCESS: {result}")
    
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n== Verify ==")
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")
