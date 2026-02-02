#!/bin/bash
# Check response headers and get session

echo "🔑 Loguję z pełnymi nagłówkami..."
curl -s -i -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' | grep -i "set-cookie\|token\|access"
echo ""

echo "📋 Sprawdzam sesję..."
curl -s -c /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "Cookies:"
cat /tmp/overseerr-cookies.txt
echo ""

echo "🔍 Sprawdzam /api/v1/user z sesją..."
curl -s -b /tmp/overseerr-cookies.txt http://localhost:5055/api/v1/user | python3 -m json.tool
