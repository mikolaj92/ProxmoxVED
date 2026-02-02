#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055

curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== create request Breaking Bad S1 =="
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" \
  -H 'Content-Type: application/json' \
  --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' \
| head -c 500; echo

sleep 2

echo "== list requests =="
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=5&skip=0" | head -c 500; echo

echo "== jellyseerr logs about Sonarr =="
docker logs jellyseerr --tail 80 2>&1 | grep -E "Media Request|Sonarr" | tail -40 || true
