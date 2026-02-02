#!/bin/bash
# Final verification

curl -s -c /tmp/jelly-verify.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "✅ KONFIGURACJA JELLYSEERR"
echo "================================"
echo ""

echo "📺 Sonarr:"
curl -s -b /tmp/jelly-verify.txt http://localhost:5055/api/v1/settings/sonarr | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'  - {s[\"name\"]}: {s[\"ip\"]}:{s[\"port\"]}') for s in d]"

echo ""
echo "🎬 Radarr:"
curl -s -b /tmp/jelly-verify.txt http://localhost:5055/api/v1/settings/radarr | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'  - {s[\"name\"]}: {s[\"ip\"]}:{s[\"port\"]}') for s in d]"

echo ""
echo "📺 Jellyfin:"
curl -s -b /tmp/jelly-verify.txt http://localhost:5055/api/v1/settings/jellyfin | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  - {d[\"name\"]}: {d[\"ip\"]}:{d[\"port\"]}')"

echo ""
echo "================================"
echo "✅ WSZYSTKO SKONFIGUROWANE!"
