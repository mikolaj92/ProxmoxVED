#!/bin/bash
# Update single Sonarr server in Jellyseerr

curl -s -c /tmp/jelly-single.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "📺 Aktualizuję Sonarr (pojedynczy obiekt)..."
curl -s -b /tmp/jelly-single.txt \
  -X POST http://localhost:5055/api/v1/settings/sonarr \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | python3 -m json.tool
echo ""

echo "🎬 Aktualizuję Radarr (pojedynczy obiekt)..."
curl -s -b /tmp/jelly-single.txt \
  -X POST http://localhost:5055/api/v1/settings/radarr \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | python3 -m json.tool
