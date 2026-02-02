#!/bin/bash
# Add all servers to Jellyseerr

API_BASE="http://localhost:5055/api/v1"

# Login
echo "🔑 Loguję..."
curl -s -c /tmp/jelly-final.txt \
  -X POST $API_BASE/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

# Sonarr already added, verify
echo "📺 Sprawdzam Sonarr..."
curl -s -b /tmp/jelly-final.txt $API_BASE/settings/sonarr | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Liczba: {len(d)}'); print(f'Nazwa: {d[0].get(\"name\") if d else \"Brak\"}')"
echo ""

# Add Radarr
echo "🎬 Dodaję Radarr..."
curl -s -b /tmp/jelly-final.txt \
  -X POST $API_BASE/settings/radarr \
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
echo ""

# Update Jellyfin
echo "📺 Aktualizuję Jellyfin..."
curl -s -b /tmp/jelly-final.txt \
  -X PATCH $API_BASE/settings/jellyfin \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "192.168.11.66",
    "port": 8096,
    "useSsl": false,
    "apiKey": "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
  }' | python3 -m json.tool
echo ""

echo "✅ Weryfikacja..."
curl -s -b /tmp/jelly-final.txt $API_BASE/settings/main | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Sonarr: {len(d.get(\"sonarr\",[]))}'); print(f'Radarr: {len(d.get(\"radarr\",[]))}'); print(f'Jellyfin: {d.get(\"jellyfin\",{}).get(\"ip\")}:{d.get(\"jellyfin\",{}).get(\"port\")}')"
