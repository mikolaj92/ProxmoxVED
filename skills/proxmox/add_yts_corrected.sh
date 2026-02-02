#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Add YTS with correct appProfileId and priority ==")

# Get available app profiles first
try:
    profiles = json.load(urllib.request.urlopen(f"{base_url}/app/profile?apikey={api_key}"))
    print(f"Available app profiles: {len(profiles)}")
    for p in profiles:
        print(f"  - ID {p.get('id')}: {p.get('name')}")

    # Use first profile (usually ID 1)
    app_profile_id = profiles[0].get('id') if profiles else 1
    print(f"\nUsing app profile ID: {app_profile_id}")

except Exception as e:
    print(f"ERROR getting profiles: {e}")
    app_profile_id = 1

# YTS config with all required fields
yts_config = {
    "definitionName": "yts",
    "name": "YTS",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": True,
    "redirect": False,
    "appProfileId": app_profile_id,
    "priority": 25,
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
        }
    ]
}

print(f"\nSending config:")
print(json.dumps(yts_config, indent=2))

try:
    req = urllib.request.Request(
        f"{base_url}/indexer?apikey={api_key}",
        data=json.dumps(yts_config).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as r:
        result = json.load(r)
        print(f"\n✓ SUCCESS!")
        print(f"  Name: {result.get('name')}")
        print(f"  ID: {result.get('id')}")
        print(f"  Implementation: {result.get('implementation')}")

except urllib.error.HTTPError as e:
    print(f"\n✗ HTTP Error {e.code}: {e.reason}")
    error_response = e.read().decode('utf-8')
    print(f"Response: {error_response}")
except Exception as e:
    print(f"\n✗ ERROR: {e}")
