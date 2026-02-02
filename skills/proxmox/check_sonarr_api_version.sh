#!/bin/bash
# Fix Sonarr connection with correct API version

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
SONARR_URL="http://192.168.11.66:8989"

echo "🔍 Sprawdzam poprawną wersję API..."
echo ""

echo "v3:"
curl -s "$SONARR_URL/api/v3/system/status?apiKey=$SONARR_KEY" | python3 -m json.tool | head -20
echo ""

echo "v1:"
curl -s "$SONARR_URL/api/v1/system/status?apiKey=$SONARR_KEY" | python3 -m json.tool | head -20
echo ""

echo "bez wersji:"
curl -s "$SONARR_URL/api/system/status?apiKey=$SONARR_KEY" | python3 -m json.tool | head -20
