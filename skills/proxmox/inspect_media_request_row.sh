#!/usr/bin/env bash
set -euo pipefail
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3

echo "== media_request schema (first 25 cols) =="
sqlite3 "$DB" "pragma table_info(media_request);" | head -25 || true

echo

echo "== latest requests fields =="
sqlite3 "$DB" "select id,type,status,mediaId,serverId,profileId,rootFolder,createdAt from media_request order by id desc limit 10;" || true
