#!/bin/bash
# Explore Overseerr API endpoints

echo "🔍 Sprawdzam dostępne endpointy Overseerr..."
echo ""

# Try register endpoint
echo "1. Próbuję /api/v1/auth/register..."
curl -s -X POST http://localhost:5055/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' | python3 -m json.tool
echo ""

# Try first-setup endpoint
echo "2. Próbuję /api/v1/setup/initialize..."
curl -s -X POST http://localhost:5055/api/v1/setup/initialize \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","username":"admin","password":"arradmin123"}' | python3 -m json.tool
echo ""

# Try initialize endpoint
echo "3. Próbuję /api/v1/initialize..."
curl -s -X POST http://localhost:5055/api/v1/initialize \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","username":"admin","password":"arradmin123"}' | python3 -m json.tool
echo ""

# Check if we can access settings without auth
echo "4. Sprawdzam /api/v1/settings/public..."
curl -s http://localhost:5055/api/v1/settings/public | python3 -m json.tool | head -30
echo ""

# Check database status
echo "5. Sprawdzam /api/v1/status..."
curl -s http://localhost:5055/api/v1/status | python3 -m json.tool
