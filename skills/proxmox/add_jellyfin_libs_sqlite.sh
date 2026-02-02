#!/usr/bin/env bash
set -euo pipefail

DB="/root/arr-stack/config/jellyfin/data/library.db"

echo "== Backup Jellyfin DB =="
cp "$DB" "$DB.bak-$(date +%s)" || true

echo
echo "== Add TV Shows library to Jellyfin (SQLite) =="
# Jellyfin uses a specific schema for libraries
sqlite3 "$DB" << "EOSQL"
INSERT INTO LibraryOptions (Id, LibraryOptionsId)
VALUES (1, 1);

INSERT INTO TopLevelFolders (Id, Name, Path, CollectionType, LibraryOptionsId)
VALUES (1, 'TV Shows', '/root/arr-stack/media/tv', 'tvshows', 1);
EOSQL

echo "TV library added (ID: 1)"

echo
echo "== Add Movies library to Jellyfin =="
sqlite3 "$DB" << "EOSQL"
INSERT INTO LibraryOptions (Id, LibraryOptionsId)
VALUES (2, 2);

INSERT INTO TopLevelFolders (Id, Name, Path, CollectionType, LibraryOptionsId)
VALUES (2, 'Movies', '/root/arr-stack/media/movies', 'movies', 2);
EOSQL

echo "Movies library added (ID: 2)"

echo
echo "== Verify =="
sqlite3 "$DB" "SELECT Id, Name, Path, CollectionType FROM TopLevelFolders;"

echo
echo "== Restart Jellyfin to pick up changes =="
docker restart jellyfin >/dev/null
sleep 8

echo "Jellyfin restarted"
docker logs jellyfin --tail 20 2>&1 | grep -E 'Startup complete|Server ready' || true
