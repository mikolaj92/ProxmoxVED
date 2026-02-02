#!/usr/bin/env bash
set -euo pipefail

echo "== verify patches =="
docker exec jellyseerr sh -lc 'grep -n "HOTFIX" -n /app/dist/routes/request.js | sed -n "1,5p"'
docker exec jellyseerr sh -lc 'grep -n "HOTFIX" -n /app/dist/api/servarr/sonarr.js | sed -n "1,5p"'
docker exec jellyseerr sh -lc 'grep -n "HOTFIX" -n /app/dist/api/servarr/base.js | sed -n "1,8p"'

echo

echo "== show servarr/base.js constructor snippet =="
docker exec jellyseerr sh -lc 'nl -ba /app/dist/api/servarr/base.js | sed -n "8,22p"'

echo

echo "== create request Breaking Bad S1 =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' | head -c 300; echo

sleep 2

echo "== jellyseerr tail =="
docker logs jellyseerr --tail 80 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Sonarr API|Failed|status code' | tail -80 || true
