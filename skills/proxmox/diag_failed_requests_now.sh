#!/usr/bin/env bash
set -euo pipefail

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)

echo "== jellyseerr logs (recent media request failures) =="
docker logs jellyseerr --tail 250 2>&1 | grep -E "Media Request|Sonarr API|Radarr\]|Failed" | tail -160 || true

echo

echo "== sonarr queue (first 400 chars) =="
curl -s "http://localhost:8989/api/v3/queue?includeEpisode=true&apiKey=$SONARR_KEY" | head -c 400; echo

echo "== radarr queue (first 400 chars) =="
curl -s "http://localhost:7878/api/v3/queue?apiKey=$RADARR_KEY" | head -c 400; echo

echo

echo "== prowlarr indexers (name, enable, protocol) =="
curl -s "http://localhost:9696/api/v1/indexer?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print([(x.get("name"),x.get("enable"),x.get("protocol"),x.get("privacy")) for x in a])'
