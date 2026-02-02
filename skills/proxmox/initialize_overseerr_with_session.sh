#!/bin/bash
# Initialize Overseerr with proper session handling

echo "🔑 Inicjalizuję Overseerr z kontem admina (z sesją)..."
echo ""

# Create session cookie
echo "1. Pobieram sesję cookie..."
curl -s -c /tmp/overseerr-cookies.txt http://localhost:5055/ > /dev/null

# Try initialize with cookie
echo "2. Inicjalizuję z cookie..."
RESPONSE=$(curl -s -b /tmp/overseerr-cookies.txt -c /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/initialize \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "arradmin123",
    "email": "admin@arr.local"
  }')

echo "$RESPONSE" | python3 -m json.tool
echo ""

# Check if initialized
echo "3. Sprawdzam status..."
curl -s http://localhost:5055/api/v1/settings/public | python3 -m json.tool | grep -E "initialized|localLogin|applicationTitle"
echo ""

# Login attempt
echo "4. Próbuję zalogować..."
LOGIN=$(curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "arradmin123",
    "email": "admin@arr.local"
  }')

echo "$LOGIN" | python3 -m json.tool | head -30
