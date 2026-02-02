#!/usr/bin/env bash
set -euo pipefail

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"

echo "== Prowlarr API key from config.xml =="
APIKEY=""
if [ -f /root/arr-stack/config/prowlarr/config.xml ]; then
  APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)
  echo "$APIKEY"
else
  echo "missing /root/arr-stack/config/prowlarr/config.xml"
fi

echo
if [ -n "$APIKEY" ]; then
  echo "== Prowlarr applications =="
  curl -s "http://localhost:9696/api/v1/applications?apikey=$APIKEY" | head -c 600; echo
fi

echo

echo "== Sonarr indexers count =="
curl -s "http://localhost:8989/api/v3/indexer?apiKey=$SONARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a))'

echo "== Radarr indexers count =="
curl -s "http://localhost:7878/api/v3/indexer?apiKey=$RADARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a))'

echo

echo "== Sonarr download clients =="
curl -s "http://localhost:8989/api/v3/downloadclient?apiKey=$SONARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a)); print([x.get("name") for x in a])'

echo "== Radarr download clients =="
curl -s "http://localhost:7878/api/v3/downloadclient?apiKey=$RADARR_KEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(len(a)); print([x.get("name") for x in a])'
