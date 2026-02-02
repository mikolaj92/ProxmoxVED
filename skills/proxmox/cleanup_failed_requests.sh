#!/usr/bin/env bash
set -euo pipefail
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3

echo "== requests before (id,type,status,mediaId,createdAt) =="
sqlite3 "$DB" "select id,type,status,mediaId,createdAt from media_request order by id desc limit 30;" || true

echo

echo "== deleting FAILED requests (status=4) =="
# status=4 in this DB corresponds to FAILED (as seen previously)
sqlite3 "$DB" "delete from season_request where requestId in (select id from media_request where status=4);" || true
sqlite3 "$DB" "delete from media_request where status=4;" || true

echo "== requests after =="
sqlite3 "$DB" "select id,type,status,mediaId,createdAt from media_request order by id desc limit 30;" || true

echo

docker restart jellyseerr >/dev/null
sleep 6

echo "restarted jellyseerr"
