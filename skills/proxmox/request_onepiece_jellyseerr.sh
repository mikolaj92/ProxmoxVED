#!/usr/bin/env bash
set -euo pipefail
JELLY_URL="http://localhost:5055"

# auth
curl -s -c /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' >/dev/null

TMDB_ID=37854

echo "== Fetch TV details (tmdb:$TMDB_ID) =="
curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/tv/$TMDB_ID" | python3 -c 'import sys,json
j=json.load(sys.stdin)
print({"name":j.get("name"),"id":j.get("id"),"numberOfSeasons":j.get("numberOfSeasons")})
seasons=j.get("seasons") or []
print("seasons", [s.get("seasonNumber") for s in seasons][:15], "...")'

echo

echo "== Create request (ALL seasons) =="
# Many installs accept "seasons": [ {"seasonNumber": X} ... ] or just [X]
# We'll try a conservative payload: seasons as list of numbers excluding 0.
seasons=$(curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/tv/$TMDB_ID" | python3 -c 'import sys,json
j=json.load(sys.stdin)
nums=[s.get("seasonNumber") for s in (j.get("seasons") or []) if s.get("seasonNumber") not in (None,0)]
print(json.dumps(nums))')

echo "payload seasons: $seasons" | head -c 200; echo

curl -s -b /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/request" \
  -H 'Content-Type: application/json' \
  --data-binary "{\"mediaType\":\"tv\",\"tmdbId\":$TMDB_ID,\"seasons\":$seasons}" \
| python3 -c 'import sys,json
try:
  j=json.load(sys.stdin)
  print(j)
except Exception as e:
  print(sys.stdin.read())'
