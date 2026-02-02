#!/bin/bash
# Initialize Overseerr with admin account

echo "🔑 Inicjalizuję Overseerr z kontem admina..."
echo ""

# Try initialize endpoint
echo "Próbuję /api/v1/settings/initialize..."
RESPONSE=$(curl -s -X POST http://localhost:5055/api/v1/settings/initialize \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "arradmin123",
    "email": "admin@arr.local"
  }')

echo "$RESPONSE" | python3 -m json.tool
echo ""

# Check if initialized
echo "Sprawdzam status..."
curl -s http://localhost:5055/api/v1/settings/public | python3 -m json.tool | grep -E "initialized|localLogin"
echo ""

# Try login
echo "Próbuję zalogować..."
LOGIN=$(curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "arradmin123"
  }')

echo "$LOGIN" | python3 -m json.tool | head -20
