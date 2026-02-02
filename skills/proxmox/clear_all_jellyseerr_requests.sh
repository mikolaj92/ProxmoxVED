#!/usr/bin/env bash
set -euo pipefail
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3

echo "counts before:"
sqlite3 "$DB" "select 'media_request', count(*) from media_request;"
sqlite3 "$DB" "select 'season_request', count(*) from season_request;"

sqlite3 "$DB" "delete from season_request;"
sqlite3 "$DB" "delete from media_request;"
# keep media table so UI cache remains, but can be cleared too

echo "counts after:"
sqlite3 "$DB" "select 'media_request', count(*) from media_request;"
sqlite3 "$DB" "select 'season_request', count(*) from season_request;"

docker restart jellyseerr >/dev/null
sleep 4

echo "test /api/v1/request:"
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=5&skip=0" | head -c 200; echo
