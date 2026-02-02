#!/bin/bash
# Explore Jellyseerr settings endpoints

curl -s -c /tmp/jelly-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "🔍 Sprawdzam /api/v1/settings/main..."
curl -s -b /tmp/jelly-cookies.txt http://localhost:5055/api/v1/settings/main | python3 -m json.tool | head -50
