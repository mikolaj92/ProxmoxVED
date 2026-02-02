#!/usr/bin/env python3
import json, urllib.request, sys

api_key = "8c6dca6adf3644ba9a7981b736ef636f"
base_url = "http://192.168.11.66:9696/api/v1"

print("== Get YTS schema ==")

schemas = json.load(urllib.request.urlopen(f"{base_url}/indexer/schema?apikey={api_key}"))

yts_schema = None
for s in schemas:
    if s.get('definitionName') == 'yts':
        yts_schema = s
        break

if yts_schema:
    print("YTS Schema:")
    print(json.dumps(yts_schema, indent=2))
else:
    print("YTS schema not found")
