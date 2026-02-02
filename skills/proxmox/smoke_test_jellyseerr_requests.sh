#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055

curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== request list (len) =="
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=3&skip=0" > /tmp/jelly_req.json
wc -c /tmp/jelly_req.json
head -c 240 /tmp/jelly_req.json; echo

echo "== create Breaking Bad S1 =="
code=$(curl -s -o /tmp/jelly_create.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}')
echo "HTTP $code"
head -c 300 /tmp/jelly_create.out; echo

echo "== jellyseerr tail =="
docker logs jellyseerr --tail 80 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Sonarr API|Sent request to Radarr|\[Radarr\]|Failed' | tail -80 || true
