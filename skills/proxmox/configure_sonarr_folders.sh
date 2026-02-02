#!/bin/bash
# Configure Root Folders and Quality Profiles in Sonarr

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
SONARR_URL="http://192.168.11.66:8989"

echo "📺 Konfiguruję Sonarr..."
echo ""

# Add Root Folder
echo "📁 Dodaję Root Folder..."
curl -s -X POST "$SONARR_URL/api/v1/rootfolder" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/media/tv",
    "name": "TV Shows"
  }' | python3 -m json.tool
echo ""

# Check existing quality profiles
echo "📊 Sprawdzam Quality Profiles..."
curl -s "$SONARR_URL/api/v1/qualityprofile?apiKey=$SONARR_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print('Liczba profili:', len(d)); [print(f'  - {p[\"name\"]} (ID: {p[\"id\"]})') for p in d[:5]]"
echo ""

# Add Quality Profile if needed
echo "✅ Sonarr skonfigurowane!"
echo ""
echo "Root Folder: /media/tv"
