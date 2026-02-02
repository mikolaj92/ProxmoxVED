#!/bin/bash
# Usuń biblioteki i restart Jellyfin

echo "=== Usuwam biblioteki z bazy ==="
sqlite3 /root/arr-stack/config/jellyfin/data/data/jellyfin.db "DELETE FROM BaseItems WHERE Type = 'MediaBrowser.Controller.Entities.CollectionFolder';"
echo "Usunięte"

echo "=== Restartuję Jellyfin ==="
docker restart jellyfin >/dev/null
sleep 15

echo "Jellyfin gotowe"
