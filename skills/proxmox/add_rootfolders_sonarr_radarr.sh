#!/bin/bash
# Add Root Folders to Sonarr and Radarr

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
SONARR_URL="http://192.168.11.66:8989/api/v3"
RADARR_URL="http://192.168.11.66:7878/api/v3"

echo "📺 Dodaję Root Folder do Sonarr..."
curl -s -X POST "$SONARR_URL/rootfolder" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/tv", "name": "TV Shows"}' | python3 -m json.tool
echo ""

echo "✅ Sonarr Root Folders:"
curl -s "$SONARR_URL/rootfolder?apiKey=$SONARR_KEY" | python3 -m json.tool
echo ""

echo "🎬 Dodaję Root Folder do Radarr..."
curl -s -X POST "$RADARR_URL/rootfolder" \
  -H "X-Api-Key: $RADARR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"path": "/movies", "name": "Movies"}' | python3 -m json.tool
echo ""

echo "✅ Radarr Root Folders:"
curl -s "$RADARR_URL/rootfolder?apiKey=$RADARR_KEY" | python3 -m json.tool
