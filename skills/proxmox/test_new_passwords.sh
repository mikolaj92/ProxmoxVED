#!/usr/bin/env bash
set -euo pipefail

echo "== Jellyseerr login test =="
curl -s -i -X POST http://localhost:5055/api/v1/auth/local \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' \
| head -15

echo

echo "== Transmission basic auth check (should return 200/401) =="
code=$(curl -s -o /dev/null -w "%{http_code}" -u transmission:Test123 http://localhost:9091/transmission/web/)
echo "HTTP $code"
