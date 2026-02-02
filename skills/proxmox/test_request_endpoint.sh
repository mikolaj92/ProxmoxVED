#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055
docker restart jellyseerr >/dev/null
sleep 4
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=10&skip=0" | head -c 400; echo
