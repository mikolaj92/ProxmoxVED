#!/bin/bash
# Dodaj ścieżkę do biblioteki TV Shows w Jellyfin przez XML edit

echo "=== Edytuję options.xml dla TV Shows ==="

# Backup
docker exec jellyfin cp "/config/data/root/default/TV Shows/options.xml" "/config/data/root/default/TV Shows/options.xml.bak"

# Nowa zawartość PathInfos
PATH_INFO='<PathInfos>
    <PathInfo>
      <Path>/root/arr-stack/media/tv</Path>
    </PathInfo>
  </PathInfos>'

# Zamień pusty PathInfos na nowy
docker exec jellyfin sed -i 's|<PathInfos />|'"$PATH_INFO"'|g' "/config/data/root/default/TV Shows/options.xml"

echo "Zaktualizowane. Weryfikacja:"
docker exec jellyfin cat "/config/data/root/default/TV Shows/options.xml" | grep -A5 "PathInfos"

echo
echo "Restartuję Jellyfin..."
docker restart jellyfin >/dev/null
sleep 8

echo "Gotowe!"
