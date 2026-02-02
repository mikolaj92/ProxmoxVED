#!/usr/bin/env bash
set -euo pipefail
APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)

echo "== prowlarr indexers count =="
curl -s "http://localhost:9696/api/v1/indexer?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a))'

echo "== prowlarr app schema list =="
# Prowlarr supports /api/v1/applications/schema
curl -s "http://localhost:9696/api/v1/applications/schema?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a)); print([x.get("implementation") for x in a][:20])'
