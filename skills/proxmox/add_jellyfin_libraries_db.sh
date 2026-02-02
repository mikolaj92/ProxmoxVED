#!/bin/bash
# Add libraries directly to Jellyfin database

DB="$HOME/arr-stack/config/jellyfin/data/data/jellyfin.db"

echo "📺 Dodaję bibliotekę TV Shows..."
sqlite3 "$DB" "INSERT INTO Libraries (Guid, Name, TypePath, CollectionType, PrimaryImageAspectRatio, IsVisible) VALUES ('tvshows', 'TV Shows', '/tv', 'tvshows', 16, 1);"
echo " ✅"
echo ""

echo "🎬 Dodaję bibliotekę Movies..."
sqlite3 "$DB" "INSERT INTO Libraries (Guid, Name, TypePath, CollectionType, PrimaryImageAspectRatio, IsVisible) VALUES ('movies', 'Movies', '/movies', 'movies', 16, 1);"
echo " ✅"
echo ""

echo "🎵 Dodaję bibliotekę Music..."
sqlite3 "$DB" "INSERT INTO Libraries (Guid, Name, TypePath, CollectionType, PrimaryImageAspectRatio, IsVisible) VALUES ('music', 'Music', '/music', 'music', 16, 1);"
echo " ✅"
echo ""

echo "🔍 Sprawdzam biblioteki..."
sqlite3 "$DB" "SELECT Name, TypePath, CollectionType FROM Libraries;"
echo ""

echo "🔄 Restartuję Jellyfin aby załadować biblioteki..."
docker restart jellyfin
sleep 10
echo " ✅"
