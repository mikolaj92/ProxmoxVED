#!/bin/bash
# Mark Overseerr as initialized using session cookie

echo "🔑 Pobieram sesję cookie..."
curl -s -c /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

echo "✏️ Oznaczam Overseerr jako zainicjowany..."
curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/initialize \
  -H "Content-Type: application/json" \
  -d '{"initialized":true}' | python3 -m json.tool
echo ""

echo "🔍 Sprawdzam status..."
curl -s http://localhost:5055/api/v1/settings/public | python3 -m json.tool | grep -E "initialized|localLogin"
echo ""

echo "👥 Sprawdzam użytkownika..."
curl -s -b /tmp/overseerr-cookies.txt http://localhost:5055/api/v1/user | python3 -m json.tool | grep -E "id|username|permissions"
