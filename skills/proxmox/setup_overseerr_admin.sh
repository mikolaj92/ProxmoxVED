#!/bin/bash
# Create Overseerr admin account via API

echo "🔑 Tworzę konto admina w Overseerr..."
echo ""

# Create admin account
echo "1. Rejestruję admina..."
RESPONSE=$(curl -s -X POST http://localhost:5055/api/v1/auth/local-first \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","username":"admin","password":"arradmin123"}')

echo "$RESPONSE" | python3 -m json.tool
echo ""

# Try to login
echo "2. Loguję się..."
LOGIN=$(curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"arradmin123"}')

echo "$LOGIN" | python3 -m json.tool
echo ""

# Check if we got a token
TOKEN=$(echo "$LOGIN" | python3 -c "import sys, json; print(json.load(sys.stdin).get('accessToken', ''))" 2>/dev/null)

if [ ! -z "$TOKEN" ]; then
    echo "✅ SUKCES! Konto admina utworzone!"
    echo "Token: ${TOKEN:0:20}..."
else
    echo "⚠️ Możliwe że konto już istnieje lub API endpoint wymaga UI setup"
fi
