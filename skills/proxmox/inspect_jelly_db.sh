#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/arr-stack/config/jellyseerr/db/db.sqlite3"
echo "== tables =="
sqlite3 "$DB" ".tables"
echo

echo "== user_settings schema =="
sqlite3 "$DB" "PRAGMA table_info(user_settings);"
echo

echo "== user_settings sample =="
sqlite3 "$DB" "SELECT id, userId, json_extract(settings, '$.sonarr') FROM user_settings LIMIT 3;" || true
