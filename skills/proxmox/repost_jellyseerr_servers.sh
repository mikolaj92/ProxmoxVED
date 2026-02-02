#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055

curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== Re-post Sonarr server =="
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/settings/sonarr" \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "id": 3,
    "name": "Sonarr",
    "hostname": "192.168.11.66",
    "port": 8989,
    "apiKey": "0375672f0f64474c8843b922d0ab595e",
    "useSsl": false,
    "baseUrl": "/",
    "active": true,
    "is4k": false,
    "isDefault": true,
    "activeProfileId": 1,
    "activeProfileName": "Any",
    "activeDirectory": "/tv",
    "enableSeasonFolders": false
  }' > /tmp/repost_sonarr.out
head -c 300 /tmp/repost_sonarr.out; echo

echo "== Re-post Radarr server =="
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/settings/radarr" \
  -H 'Content-Type: application/json' \
  --data-binary '{
    "id": 3,
    "name": "Radarr",
    "hostname": "192.168.11.66",
    "port": 7878,
    "apiKey": "e2166ae2a7284752a3d6b95423485f42",
    "useSsl": false,
    "baseUrl": "/",
    "active": true,
    "is4k": false,
    "isDefault": true,
    "activeProfileId": 1,
    "activeProfileName": "Any",
    "activeDirectory": "/movies",
    "minimumAvailability": "released"
  }' > /tmp/repost_radarr.out
head -c 300 /tmp/repost_radarr.out; echo

echo "== Restart Jellyseerr =="
docker restart jellyseerr >/dev/null
sleep 4

echo "== Request list now =="
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=5&skip=0" | head -c 200; echo
