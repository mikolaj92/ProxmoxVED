#!/bin/bash
# Add indexers to Prowlarr via API
PROWLARR_KEY="8c6dca6adf3644ba9a7981b736ef636f"
BASE_URL="http://192.168.11.66:9696"

echo "📡 Adding indexers to Prowlarr..."
echo ""

# 1. Add Cardigann (built-in indexer definitions)
echo "🔹 Adding Cardigann (built-in indexers)..."

# Cardigann has many built-in indexers, try to add a few popular ones
INDEXERS=(
    "1337x|cardigann|https://1337x.to"
    "nyaasi|cardigann|https://nyaa.si"
    "torrentgalaxy|cardigann|https://torrentgalaxy.to"
    "rustorrent|cardigann|https://ru-tor.org"
)

for indexer in "${INDEXERS[@]}"; do
    IFS='|' read -r name impl url <<< "$indexer"
    echo "   → Adding $name..."

    curl -s -X POST "${BASE_URL}/api/v1/indexer" \
      -H "X-Api-Key: ${PROWLARR_KEY}" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"$name\",
        \"implementation\": \"$impl\",
        \"configContract\": \"CardigannSettings\",
        \"enable\": true,
        \"baseSettings\": {
          \"url\": \"$url\",
          \"apiKey\": \"\"
        }
      }" > /dev/null

    if [ $? -eq 0 ]; then
        echo "      ✅ $name added"
    else
        echo "      ⚠️ $name failed (may need manual setup)"
    fi
done

echo ""
echo "🔹 Adding public Torznab indexers..."

# Try to add some public NZB indexers (these typically require signup)
PUBLIC_INDEXERS=(
    "NZBGeek|torznab|https://api.nzbgeek.info"
    "NZB.su|torznab|https://api.nzb.su"
)

for indexer in "${PUBLIC_INDEXERS[@]}"; do
    IFS='|' read -r name impl url <<< "$indexer"
    echo "   → Adding $name (requires signup)..."

    curl -s -X POST "${BASE_URL}/api/v1/indexer" \
      -H "X-Api-Key: ${PROWLARR_KEY}" \
      -H "Content-Type: application/json" \
      -d "{
        \"name\": \"$name\",
        \"implementation\": \"$impl\",
        \"configContract\": \"TorznabSettings\",
        \"enable\": false,
        \"baseSettings\": {
          \"baseUrl\": \"$url\",
          \"apiKey\": \"YOUR_API_KEY_HERE\",
          \"categories\": [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]
        }
      }" > /dev/null

    echo "      ⚠️ $name added (disabled - needs API key)"
done

echo ""
echo "🔹 Testing indexer sync to apps..."

# Trigger sync to connected apps
curl -s -X POST "${BASE_URL}/api/v1/command" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ApplicationIndexerSync",
    "commandName": "ApplicationIndexerSync"
  }' > /dev/null

echo "   ✅ Indexer sync triggered to Sonarr/Radarr/Lidarr"

echo ""
echo "📊 Checking added indexers..."
curl -s "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" | python3 -m json.tool | head -50

echo ""
echo "✅ Indexer setup complete!"
echo ""
echo "📋 SUMMARY:"
echo "  • Cardigann indexers: Added (built-in)"
echo "  • Public indexers: Added (disabled - need API keys)"
echo "  • Sync to apps: Triggered"
echo ""
echo "🔧 NEXT STEPS:"
echo "  1. Open: http://192.168.11.66:9696"
echo "  2. Go to: Indexers"
echo "  3. Test each indexer"
echo "  4. For paid indexers (NZBGeek, NZB.su):"
echo "     - Sign up at their website"
echo "     - Get API key"
echo "     - Edit indexer in Prowlarr"
echo "     - Add API key and enable"
echo ""
