#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Get existing indexer config (Nyaa.si) ==")
indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))

for idx in indexers:
    if idx.get('name') == 'Nyaa.si':
        print(f"Name: {idx.get('name')}")
        print(f"Implementation: {idx.get('implementation')}")
        print(f"Config contract: {idx.get('config_contract')}")
        print(f"Full config:")
        print(json.dumps(idx, indent=2))
        break

print("\n== Get indexer schema for Nyaa.si to understand required fields ==")
schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))

for s in schemas:
    if s.get('name') == 'Nyaa.si':
        print(f"Schema for Nyaa.si:")
        print(json.dumps(s, indent=2))
        break
