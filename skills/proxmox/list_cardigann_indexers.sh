#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Get all Cardigann indexer schemas ==")

schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))

cardigann_schemas = [s for s in schemas if s.get('implementation') == 'Cardigann']

print(f"Total Cardigann schemas: {len(cardigann_schemas)}\n")

# Show first 20
print("First 20 Cardigann indexers:")
for s in cardigann_schemas[:20]:
    name = s.get('definitionName', 'unknown')
    label = s.get('name', name)
    print(f"  - {label} (definition: {name})")

# Check if our target indexers exist
print("\n=== Looking for specific indexers ===")
targets = ["yts", "1337x", "thepiratebay", "torrentgalaxy", "limetorrents", "rarbg"]

for target in targets:
    found = False
    for s in cardigann_schemas:
        if target.lower() in s.get('definitionName', '').lower():
            print(f"✓ Found: {s.get('name')} (definition: {s.get('definitionName')})")
            found = True
            break
    if not found:
        print(f"✗ NOT FOUND: {target}")
