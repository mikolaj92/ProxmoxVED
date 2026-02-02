#!/usr/bin/env bash
set -euo pipefail
JELLY_URL="http://localhost:5055"

curl -s -c /tmp/jelly.cookie -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' >/dev/null

resp=$(curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/request?take=5&skip=0")

echo "== raw =="
echo "$resp" | head -c 600; echo

echo "== parsed =="
echo "$resp" | python3 -c 'import sys,json
j=json.load(sys.stdin)
print(j.keys())
print("pageInfo", j.get("pageInfo"))
print("results_len", len(j.get("results", [])))
for r in j.get("results", []):
  print({"id":r.get("id"),"type":r.get("type"),"status":r.get("status"),"title":(r.get("media") or {}).get("title")})'
