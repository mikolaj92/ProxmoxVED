#!/usr/bin/env bash
set -euo pipefail
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3
JELLY=http://localhost:5055

echo "== media_request rows =="
sqlite3 "$DB" "select id,type,status,mediaId,createdAt from media_request order by id desc limit 10;" || true

echo "== media_request count =="
sqlite3 "$DB" "select count(*) from media_request;" || true

echo

echo "== /api/v1/request?take=20 =="
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=20&skip=0" | head -c 800; echo

echo

echo "== jellyseerr log tail (Media Request) =="
docker logs jellyseerr --tail 200 2>&1 | grep -E "Media Request|requestId" | tail -120 || true
