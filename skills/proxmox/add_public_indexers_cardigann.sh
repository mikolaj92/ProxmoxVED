#!/usr/bin/env python3
import json, urllib.request, sys, time

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

# Public indexers to add (Cardigann definitions)
indexers_to_add = [
    {
        "definitionName": "yts",
        "name": "YTS",
        "implementation": "Cardigann",
        "configContract": "CardigannSettings"
    },
    {
        "definitionName": "1337x",
        "name": "1337x",
        "implementation": "Cardigann",
        "configContract": "CardigannSettings"
    },
    {
        "definitionName": "thepiratebay",
        "name": "The Pirate Bay",
        "implementation": "Cardigann",
        "configContract": "CardigannSettings"
    }
]

print("== Adding public indexers using Cardigann definitions ==\n")

for idx_def in indexers_to_add:
    print(f"Adding {idx_def['name']}...")
    
    # Get the schema for this indexer from Prowlarr
    try:
        schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))
        
        # Find matching schema by definitionName
        target_schema = None
        for s in schemas:
            if s.get('definitionName') == idx_def['definitionName']:
                target_schema = s
                break
        
        if not target_schema:
            print(f"  WARNING: Schema not found for {idx_def['name']}")
            continue
        
        # Prepare the indexer config based on schema
        add_config = {
            "name": idx_def['name'],
            "implementation": idx_def['implementation'],
            "configContract": idx_def['configContract'],
            "enable": True
        }
        
        # Add required fields from schema
        if 'fields' in target_schema:
            add_config['fields'] = []
            for field in target_schema.get('fields', []):
                field_copy = field.copy()
                # Keep default values from schema
                if 'value' in field:
                    field_copy['value'] = field['value']
                add_config['fields'].append(field_copy)
        
        # Add the indexer
        req = urllib.request.Request(
            f"{base_url}/indexer?apikey={api_key}",
            data=json.dumps(add_config).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req) as r:
            result = json.load(r)
            if isinstance(result, dict) and 'name' in result:
                print(f"  ✓ Added: {result['name']} (ID: {result.get('id', 'N/A')})")
            else:
                print(f"  ✓ Added: {result}")
    
    except urllib.error.HTTPError as e:
        print(f"  ✗ HTTP Error {e.code}: {e.reason}")
    except Exception as e:
        print(f"  ✗ ERROR: {e}")

print("\n== Verify all indexers =="
try:
    indexers = json.load(urllib.request.urlopen(f"{base_url}/indexer?apikey={api_key}"))
    print(f"Total indexers: {len(indexers)}\n")
    for idx in indexers:
        print(f"  • {idx.get('name')}: {idx.get('implementation')}, enabled={idx.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n== Trigger application sync to Sonarr/Radarr =="
try:
    sync_req = urllib.request.Request(
        f"{base_url}/command?apikey={api_key}",
        data=json.dumps({"name": "ApplicationIndexerSync"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(sync_req) as r:
        result = json.load(r)
        print(f"✓ Sync command sent: {result.get('name')}, ID: {result.get('id')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\nWaiting 15 seconds for sync...")
time.sleep(15)

print("\n== Check indexer count in Sonarr =="
try:
    apps = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/application?apikey=0375672f0f64474c8843b922d0ab595e"))
    for app in apps:
        if app.get('name') == 'Prowlarr':
            print(f"Sonarr ← Prowlarr: indexerCount={app.get('indexerCount')}")
except Exception as e:
    print(f"ERROR: {e}")
