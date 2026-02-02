#!/bin/bash
# Dodaj ścieżki do bibliotek Jellyfin
API_KEY="61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
BASE="http://localhost:8096"

echo "=== Dodaję ścieżki do bibliotek ==="

# Pobierz ItemId dla TV Shows
TV_ID=$(curl -s "$BASE/Library/VirtualFolders?api_key=$API_KEY" | python3 -c "import json,sys; libs=json.load(sys.stdin); print([l.get('ItemId') for l in libs if l.get('Name')=='TV Shows'][0])")

echo "TV Shows ID: $TV_ID"

# Dodaj ścieżkę
curl -s -X POST "$BASE/Library/VirtualFolders/Paths?api_key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"ItemId\":\"$TV_ID\",\"Path\":\"/root/arr-stack/media/tv\"}" \
  | head -c 300

echo
echo "Done. Restartuję Jellyfin..."
docker restart jellyfin >/dev/null
sleep 8

echo "Weryfikacja:"
curl -s "$BASE/Library/VirtualFolders?api_key=$API_KEY" | python3 -c "import json,sys; libs=json.load(sys.stdin); tv=[l for l in libs if l.get('Name')=='TV Shows'][0]; print(json.dumps(tv.get('Locations'), indent=2))"
