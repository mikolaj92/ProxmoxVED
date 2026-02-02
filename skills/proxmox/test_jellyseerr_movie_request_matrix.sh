#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== request The Matrix (tmdb 603) =="
code=$(curl -s -o /tmp/jelly_movie.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"movie","mediaId":603,"is4k":false}')
echo "HTTP $code"
head -c 250 /tmp/jelly_movie.out; echo

echo "== jellyseerr tail =="
docker logs jellyseerr --tail 80 2>&1 | grep -E 'Sent request to Radarr|Radarr accepted|\[Radarr\]|Failed|status code' | tail -80 || true
