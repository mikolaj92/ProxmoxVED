#!/usr/bin/env bash
set -euo pipefail
DB="$HOME/arr-stack/config/jellyseerr/db/db.sqlite3"

# list media entries matching One Piece
sqlite3 "$DB" "select id, mediaType, tmdbId, tvdbId, status from media where tvdbId=81797 or tmdbId=37854;"

# delete related requests (if any)
sqlite3 "$DB" "delete from media_request where mediaId in (select id from media where tvdbId=81797 or tmdbId=37854);"
sqlite3 "$DB" "delete from season_request where requestId not in (select id from media_request);" || true

# optional: delete media rows too (so Jellyseerr refetches clean)
sqlite3 "$DB" "delete from media where tvdbId=81797 or tmdbId=37854;"

echo "done"
