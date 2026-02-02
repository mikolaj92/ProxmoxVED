#!/usr/bin/env python3
import json, urllib.request, sys, time

print("== Adding public indexers to Prowlarr ==")

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

# Public indexers to add (using torznab/newznab format)
indexers_to_add = [
    {
        "name": "The Pirate Bay",
        "implementation": "Torznab",
        "config_contract": "TorznabSettings",
        "enable": True,
        "base_url": "https://apibay.org/q.php",
        "api_key": "",
        "categories": [5000, 5010, 5020, 5030, 5040, 5060, 5070, 5080]
    },
    {
        "name": "1337x",
        "implementation": "Torznab",
        "config_contract": "TorznabSettings",
        "enable": True,
        "base_url": "https://1337x.to",
        "api_key": "",
        "categories": [5000, 5010, 5020, 5030, 5040, 5060, 5070, 5080]
    },
    {
        "name": "NZBGeek",
        "implementation": "Newznab",
        "config_contract": "NewznabSettings",
        "enable": True,
        "base_url": "https://api.nzbgeek.info",
        "api_key": "",
        "categories": [5000, 5010, 5020, 5030, 5040, 5060, 5070, 5080]
    }
]

# Get Prowlarr indexer schema first to understand the format
print("\n== Get indexer schema ==")
try:
    schema = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))
    print(f"Found {len(schema)} schema types")
    for s in schema[:3]:
        print(f"  - {s.get('implementation')}: {s.get('config_contract')}")
except Exception as e:
    print(f"ERROR getting schema: {e}")

# Add a simple cardigann indexer (YTS for movies)
print("\n== Add YTS indexer (movies) ==")

yts_config = {
    "name": "YTS",
    "implementation": "Cardigann",
    "config_contract": "CardigannSettings",
    "enable": True,
    "baseUrl": "https://yts.mx",
    "categories": [5020]  # Movies
}

try:
    req = urllib.request.Request(
        f"{base_url}/indexer?apikey={api_key}",
        data=json.dumps(yts_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.load(r)
        print(f"YTS added: {result.get('name') if isinstance(result, dict) else 'success'}")
except Exception as e:
    print(f"ERROR adding YTS: {e}")

print("\n== List all indexers after adding ==")
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total indexers: {len(indexers)}")
    for idx in indexers:
        print(f"  - {idx.get('name')}: enabled={idx.get('enable')}, type={idx.get('implementation')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n== Trigger application sync to Sonarr/Radarr ==")
try:
    sync_req = urllib.request.Request(
        f"{base_url}/command?apikey={api_key}",
        data=json.dumps({"name": "ApplicationIndexerSync"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(sync_req) as r:
        result = json.load(r)
        print(f"Sync command sent: {result.get('name')}, ID: {result.get('id')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nWaiting 10 seconds for sync...")
time.sleep(10)

print("\n== Verify indexer count on Sonarr ==")
try:
    apps = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/indexer/schema?apikey=0375672f0f64474c8843b922d0ab595e"))
    print(f"Sonarr indexer schemas available: {len(apps)}")
except Exception as e:
    print(f"ERROR: {e}")
