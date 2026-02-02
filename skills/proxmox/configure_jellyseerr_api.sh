#!/bin/bash
# Configure Jellyseerr services via API

API_BASE="http://localhost:5055/api/v1"

# Login and get cookie
echo "🔑 Loguję do Jellyseerr..."
curl -s -c /tmp/jellyseerr-config.txt \
  -X POST $API_BASE/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

# Add Sonarr
echo "📺 Dodaję Sonarr..."
curl -s -b /tmp/jellyseerr-config.txt \
  -X POST $API_BASE/settings/sonarr \
  -H "Content-Type: application/json" \
  -d '{
    "id": 0,
    "name": "Sonarr",
    "hostname": "192.168.11.66",
    "port": 8989,
    "apiKey": "0375672f0f64474c8843b922d0ab595e",
    "useSsl": false,
    "baseUrl": "/",
    "active": true,
    "is4k": false,
    "isDefault": true
  }' | python3 -m json.tool
echo ""

# Add Radarr
echo "🎬 Dodaję Radarr..."
curl -s -b /tmp/jellyseerr-config.txt \
  -X POST $API_BASE/settings/radarr \
  -H "Content-Type: application/json" \
  -d '{
    "id": 0,
    "name": "Radarr",
    "hostname": "192.168.11.66",
    "port": 7878,
    "apiKey": "e2166ae2a7284752a3d6b95423485f42",
    "useSsl": false,
    "baseUrl": "/",
    "active": true,
    "is4k": false,
    "isDefault": true
  }' | python3 -m json.tool
echo ""

# Add Jellyfin
echo "📺 Dodaję Jellyfin..."
curl -s -b /tmp/jellyseerr-config.txt \
  -X POST $API_BASE/settings/jellyfin \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jellyfin",
    "ip": "192.168.11.66",
    "port": 8096,
    "useSsl": false,
    "urlBase": "",
    "apiKey": "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
  }' | python3 -m json.tool
echo ""

echo "✅ Sprawdzam połączone serwery..."
curl -s -b /tmp/jellyseerr-config.txt $API_BASE/settings/main | python3 -c "import json,sys; d=json.load(sys.stdin); print('Sonarr:', len(d.get('sonarr',[]))); print('Radarr:', len(d.get('radarr',[]))); print('Jellyfin IP:', d.get('jellyfin',{}).get('ip','Not set')); print('Jellyfin API Key:', d.get('jellyfin',{}).get('apiKey','Not set')[:30]+'...')"
