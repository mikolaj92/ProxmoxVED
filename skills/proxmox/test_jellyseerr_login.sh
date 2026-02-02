#!/bin/bash
# Test Jellyseerr login and check servers

echo "🔑 Próbuję zalogować admina..."
curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' | python3 -m json.tool | head -30
echo ""

echo "📊 Sprawdzam połączone serwery..."
curl -s -c /tmp/jellyseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

curl -s -b /tmp/jellyseerr-cookies.txt http://localhost:5055/api/v1/settings/servers | python3 -m json.tool | head -50
