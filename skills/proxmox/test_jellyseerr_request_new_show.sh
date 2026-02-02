#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055

curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== request Better Call Saul S1 (tmdb 60059) =="
code=$(curl -s -o /tmp/jelly_newreq.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":60059,"seasons":[1],"is4k":false}')
echo "HTTP $code"
head -c 300 /tmp/jelly_newreq.out; echo

echo "== jellyseerr tail =="
docker logs jellyseerr --tail 80 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Sonarr API|Failed|status code' | tail -80 || true
