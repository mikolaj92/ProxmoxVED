#!/usr/bin/env bash
set -euo pipefail
APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"

base=http://localhost:9696/api/v1

echo "== wait 10s for sync =="
sleep 10

echo "== prowlarr command history (last 5) =="
curl -s "$base/command?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); a=sorted(a, key=lambda x:x.get("id",0), reverse=True)[:5]; print([(x.get("id"),x.get("name"),x.get("status")) for x in a])'

echo "== sonarr indexers count =="
curl -s "http://localhost:8989/api/v3/indexer?apiKey=$SONARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a))'

echo "== radarr indexers count =="
curl -s "http://localhost:7878/api/v3/indexer?apiKey=$RADARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a))'
