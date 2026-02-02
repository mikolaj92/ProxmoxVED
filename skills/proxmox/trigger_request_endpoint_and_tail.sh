#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

# hit endpoint
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=5&skip=0" >/dev/null || true

echo "== log tail =="
docker logs jellyseerr --tail 80 2>&1 | tail -80
