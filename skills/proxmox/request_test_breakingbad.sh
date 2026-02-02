#!/usr/bin/env bash
set -euo pipefail
JELLY_URL="http://localhost:5055"

curl -s -c /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' >/dev/null

TMDB_ID=1396

echo "== Request Breaking Bad S1 (tmdb:$TMDB_ID) =="
curl -s -b /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/request" \
  -H 'Content-Type: application/json' \
  --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' \
| python3 -c 'import sys,json
try:
  print(json.load(sys.stdin))
except Exception:
  print(sys.stdin.read())'
