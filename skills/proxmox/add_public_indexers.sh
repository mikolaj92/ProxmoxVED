#!/bin/bash
PROWLARR_KEY="8c6dca6adf3644ba9a7981b736ef636f"
BASE_URL="http://192.168.11.66:9696"

echo "📡 Adding public (no-signup) indexers..."
echo ""

# Add 1337x
echo "→ Adding 1337x..."
curl -s -X POST "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"1337x","implementation":"Cardigann","configContract":"CardigannSettings","enable":true,"baseSettings":{"baseUrl":"https://1337x.to"}}'
echo " ✅"

# Add Nyaa.si
echo "→ Adding Nyaa.si..."
curl -s -X POST "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Nyaa.si","implementation":"Cardigann","configContract":"CardigannSettings","enable":true,"baseSettings":{"baseUrl":"https://nyaa.si"}}'
echo " ✅"

# Add TorrentGalaxy
echo "→ Adding TorrentGalaxy..."
curl -s -X POST "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"TorrentGalaxy","implementation":"Cardigann","configContract":"CardigannSettings","enable":true,"baseSettings":{"baseUrl":"https://torrentgalaxy.to"}}'
echo " ✅"

# Add Zooqle
echo "→ Adding Zooqle..."
curl -s -X POST "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Zooqle","implementation":"Cardigann","configContract":"CardigannSettings","enable":true,"baseSettings":{"baseUrl":"https://zooqle.com"}}'
echo " ✅"

# Add RuTor
echo "→ Adding RuTor..."
curl -s -X POST "${BASE_URL}/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"RuTor","implementation":"Cardigann","configContract":"CardigannSettings","enable":true,"baseSettings":{"baseUrl":"https://rutor.info"}}'
echo " ✅"

echo ""
echo "🔍 Checking status..."
curl -s "${BASE_URL}/api/v1/indexer?apiKey=${PROWLARR_KEY}" | python3 -m json.tool | head -50

echo ""
echo "🔄 Triggering sync to apps..."
curl -s -X POST "${BASE_URL}/api/v1/command" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"name":"ApplicationIndexerSync","commandName":"ApplicationIndexerSync"}'

echo ""
echo "✅ Done!"
