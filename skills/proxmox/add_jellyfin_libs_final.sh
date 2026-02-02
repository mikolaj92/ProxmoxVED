#!/bin/bash
# Dodaj biblioteki Jellyfin - uruchom na hoście CT 220
# Użycie: bash add_jellyfin_libs.sh

echo "=== Dodawanie bibliotek Jellyfin ==="

# TV Shows
echo "1. Dodaję TV Shows..."
curl -s -X POST "http://localhost:8096/Library/VirtualFolders?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888&name=TV%20Shows&collectionType=tvshows" \
  -H "Content-Type: application/json" \
  -d '{"Paths":["/root/arr-stack/media/tv"]}' \
  2>&1 | head -c 300

echo
echo "2. Dodaję Movies..."
curl -s -X POST "http://localhost:8096/Library/VirtualFolders?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888&name=Movies&collectionType=movies" \
  -H "Content-Type: application/json" \
  -d '{"Paths":["/root/arr-stack/media/movies"]}' \
  2>&1 | head -c 300

echo
echo "3. Restartuję Jellyfin..."
docker restart jellyfin >/dev/null
sleep 8

echo "4. Sprawdzam biblioteki..."
curl -s "http://localhost:8096/Library/VirtualFolders?api_key=61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888" | head -c 600

echo
echo "Gotowe!"
