#!/bin/bash
# Try login with admin account

echo "🔑 Próbuję zalogować z email..."
curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' | python3 -m json.tool
echo ""

echo "🔑 Próbuję zalogować z username..."
curl -s -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"arradmin123"}' | python3 -m json.tool
echo ""

echo "📋 Sprawdzam użytkownika w bazie..."
sqlite3 ~/arr-stack/config/overseerr/db/db.sqlite3 "SELECT id, email, username FROM user;"
