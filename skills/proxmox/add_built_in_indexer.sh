#!/usr/bin/env python3
import json, urllib.request, sys, time

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Get Cardigann definition for a public indexer (e.g., TorrentGalaxy) ==")

# Try to get a preset definition that's known to work
try:
    # List all available Cardigann indexers
    schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))

    # Look for public, working indexers
    public_indexers = []
    for s in schemas:
        name = s.get('name', '')
        impl = s.get('implementation', '')
        if impl == 'Cardigann' and 'public' in name.lower() or '1337x' in name.lower() or 'piratebay' in name.lower() or 'yggtorrent' in name.lower():
            public_indexers.append(s)

    print(f"Found {len(public_indexers)} public indexer schemas:")
    for idx in public_indexers[:10]:
        print(f"  - {idx.get('name')}: {idx.get('implementation')}")

    # Try adding 1337x if available
    for schema in public_indexers:
        if '1337x' in schema.get('name', '').lower():
            print(f"\n== Adding {schema.get('name')} ==")

            add_config = {
                "name": schema.get('name'),
                "implementation": schema.get('implementation'),
                "config_contract": schema.get('config_contract'),
                "enable": True
            }

            try:
                req = urllib.request.Request(
                    f"{base_url}/indexer?apikey={api_key}",
                    data=json.dumps(add_config).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req) as r:
                    result = json.load(r)
                    print(f"Success: {result}")
            except Exception as e:
                print(f"ERROR: {e}")
            break

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n== Alternative: Add Newznab indexer (Binsearch is public) ==")

# Newznab format for public NZB indexer
newznab_config = {
    "name": "Binsearch",
    "implementation": "Newznab",
    "config_contract": "NewznabSettings",
    "enable": True,
    "base_url": "https://binsearch.info",
    "api_key": "",
    "categories": [5000, 5010, 5020, 5030, 5040, 5060, 5070, 5080]
}

try:
    req = urllib.request.Request(
        f"{base_url}/indexer?apikey={api_key}",
        data=json.dumps(newznab_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.load(r)
        print(f"Binsearch added: {result}")
except Exception as e:
    print(f"ERROR adding Binsearch: {e}")

print("\n== Current indexer list ==")
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: {idx.get('implementation')}, enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")
