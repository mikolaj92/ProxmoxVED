#!/bin/bash
# Check Jellyseerr user permissions

echo "🔑 Loguję do Jellyseerr..."
LOGIN=$(curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}')

echo "$LOGIN" | python3 -m json.tool | head -30
echo ""

# Get cookie
curl -s -c /tmp/jelly-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "👂 Sprawdzam user details..."
curl -s -b /tmp/jelly-cookies.txt http://localhost:5055/api/v1/user | python3 -m json.tool
