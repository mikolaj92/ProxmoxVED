#!/bin/bash
# Test with max permissions

API_BASE="http://localhost:5055/api/v1"

# Login
echo "🔑 Loguję..."
curl -s -c /tmp/jelly-test.txt \
  -X POST $API_BASE/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"

echo "👂 Sprawdzam permissions..."
LOGIN=$(curl -s -X POST $API_BASE/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}')
echo "$LOGIN" | python3 -c "import json,sys; print('Permissions:', json.load(sys.stdin).get('permissions'))"
echo ""

echo "📺 Próbuję dodać Sonarr..."
curl -s -b /tmp/jelly-test.txt \
  -X POST $API_BASE/settings/sonarr \
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
  }' | python3 -m json.tool | head -10
