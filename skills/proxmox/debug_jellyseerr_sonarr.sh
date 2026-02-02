#!/bin/bash
# Debug Jellyseerr connection

curl -s -c /tmp/jelly-debug.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "🔍 Sprawdzam połączenie z Sonarr..."
curl -s -b /tmp/jelly-debug.txt http://localhost:5055/api/v1/settings/sonarr | python3 -m json.tool 2>/dev/null | head -80
echo ""

echo "🔍 Sprawdzam Quality Profiles z Sonarr..."
curl -s "http://localhost:8989/api/v1/qualityprofile?apiKey=0375672f0f64474c8843b922d0ab595e" | python3 -m json.tool 2>/dev/null || echo "SONARR API NIE ODPOWIADA"
echo ""

echo "🔍 Sprawdzam Root Folders z Sonarr..."
curl -s "http://localhost:8989/api/v1/rootfolder?apiKey=0375672f0f64474c8843b922d0ab595e" | python3 -m json.tool 2>/dev/null || echo "BŁĄD ROOT FOLDERS"
