#!/usr/bin/env bash
set -euo pipefail
JELLY_URL="http://localhost:5055"

curl -s -c /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' >/dev/null

TMDB_ID=37854

# seasons as objects
payload='{"mediaType":"tv","mediaId":37854,"seasons":[{"seasonNumber":22}],"is4k":false}'

echo "payload=$payload"

curl -s -b /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/request" \
  -H 'Content-Type: application/json' \
  --data-binary "$payload" \
| python3 -c 'import sys,json
try:
  print(json.load(sys.stdin))
except Exception:
  print(sys.stdin.read())'
