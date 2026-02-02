#!/usr/bin/env bash
set -euo pipefail
JELLY_URL="http://localhost:5055"

curl -s -c /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' >/dev/null

curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/settings/sonarr" | python3 -c 'import sys,json; import pprint; pprint.pp(json.load(sys.stdin))'
