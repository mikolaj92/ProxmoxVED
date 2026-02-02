#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/arr-stack/config/jellyseerr/db/db.sqlite3"
sqlite3 "$DB" "select id, type, status, mediaId, createdAt from media_request order by id desc limit 10;"
