#!/bin/bash
# Add Root Folder to Sonarr

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
SONARR_URL="http://192.168.11.66:8989/api/v3"

echo "📁 Dodaję Root Folder do Sonarr..."
curl -s -X POST "$SONARR_URL/rootfolder" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/media/tv",
    "name": "TV Shows"
  }' | python3 -m json.tool
echo ""

echo "✅ Sprawdzam Root Folders..."
curl -s "$SONARR_URL/rootfolder?apiKey=$SONARR_KEY" | python3 -m json.tool
