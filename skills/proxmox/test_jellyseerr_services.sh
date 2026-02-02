#!/bin/bash
# Test Jellyseerr login and check services

echo "🔑 Loguję do Jellyseerr..."
curl -s -c /tmp/jellyseerr-test.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

echo "📺 Sprawdzam Sonarr..."
curl -s -b /tmp/jellyseerr-test.txt http://localhost:5055/api/v1/settings/sonarr | python3 -m json.tool | head -30
echo ""

echo "🎬 Sprawdzam Radarr..."
curl -s -b /tmp/jellyseerr-test.txt http://localhost:5055/api/v1/settings/radarr | python3 -m json.tool | head -30
echo ""

echo "📺 Sprawdzam Jellyfin connection..."
curl -s -b /tmp/jellyseerr-test.txt http://localhost:5055/api/v1/settings/jellyfin | python3 -m json.tool
