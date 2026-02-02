#!/bin/bash
# Check Sonarr v3 API endpoints

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
SONARR_URL="http://192.168.11.66:8989/api/v3"

echo "📊 Quality Profiles (v3):"
curl -s "$SONARR_URL/qualityprofile?apiKey=$SONARR_KEY" | python3 -m json.tool | head -50
echo ""

echo "📁 Root Folders (v3):"
curl -s "$SONARR_URL/rootfolder?apiKey=$SONARR_KEY" | python3 -m json.tool | head -50
