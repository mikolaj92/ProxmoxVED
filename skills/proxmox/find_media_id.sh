#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/arr-stack/config/jellyseerr/db/db.sqlite3"
sqlite3 "$DB" "SELECT id, mediaType, tmdbId, tvdbId, status FROM media WHERE tmdbId=37854;"
