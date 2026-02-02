#!/bin/bash
# Initialize Overseerr using API Key

API_KEY="MTc2OTkzNzU3OTk1NTNhMjk5NTEzLWU5YTQtNDE3Yy1iNTA4LWFmZjlmMmU1ZGE3Mg=="

echo "🔑 Używam API Key do inicjalizacji..."
echo ""

# Try to initialize with API key
echo "1. Próbuję /api/v1/settings/initialize z API Key..."
curl -s -X POST "http://localhost:5055/api/v1/settings/initialize?api_key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "arradmin123",
    "email": "admin@arr.local"
  }' | python3 -m json.tool
echo ""

# Try without api_key param but in header
echo "2. Próbuję z API key w header..."
curl -s -X POST "http://localhost:5055/api/v1/settings/initialize" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "username": "admin",
    "password": "arradmin123",
    "email": "admin@arr.local"
  }' | python3 -m json.tool
echo ""

# Check status
echo "3. Sprawdzam status..."
curl -s "http://localhost:5055/api/v1/settings/public?api_key=$API_KEY" | python3 -m json.tool | grep -E "initialized|localLogin"
