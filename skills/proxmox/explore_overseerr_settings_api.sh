#!/bin/bash
# Explore Overseerr API endpoints

echo "🔑 Pobieram sesję cookie..."
curl -s -c /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

echo "🔍 Sprawdzam /api/v1/settings..."
curl -s -b /tmp/overseerr-cookies.txt http://localhost:5055/api/v1/settings | python3 -m json.tool | head -80
