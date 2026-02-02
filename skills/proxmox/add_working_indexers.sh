#!/bin/bash
echo "📡 Adding public indexers to Prowlarr..."
echo ""

# Add Nyaa.si (anime - no CloudFlare)
echo "→ Adding Nyaa.si..."
curl -s -X POST "http://192.168.11.66:9696/api/v1/indexer" \
  -H "X-Api-Key: 8c6dca6adf3644ba9a7981b736ef636f" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nyaa.si",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": true,
    "appProfileId": 1,
    "priority": 25,
    "downloadClientId": 0,
    "fields": [
      {"order": 0, "name": "definitionFile", "value": "nyaasi"},
      {"order": 1, "name": "baseUrl", "value": "https://nyaa.si"}
    ]
  }'
echo ""
echo "✅ Nyaa.si added!"
echo ""

# Add RuTor
echo "→ Adding RuTor..."
curl -s -X POST "http://192.168.11.66:9696/api/v1/indexer" \
  -H "X-Api-Key: 8c6dca6adf3644ba9a7981b736ef636f" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RuTor",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": true,
    "appProfileId": 1,
    "priority": 25,
    "downloadClientId": 0,
    "fields": [
      {"order": 0, "name": "definitionFile", "value": "rutor"},
      {"order": 1, "name": "baseUrl", "value": "https://rutor.info"}
    ]
  }'
echo ""
echo "✅ RuTor added!"
echo ""

# Check status
echo "🔍 Verifying added indexers..."
curl -s "http://192.168.11.66:9696/api/v1/indexer?apiKey=8c6dca6adf3644ba9a7981b736ef636f" | python3 -m json.tool
echo ""

# Trigger sync
echo "🔄 Syncing to apps..."
curl -s -X POST "http://192.168.11.66:9696/api/v1/command" \
  -H "X-Api-Key: 8c6dca6adf3644ba9a7981b736ef636f" \
  -H "Content-Type: application/json" \
  -d '{"name":"ApplicationIndexerSync","commandName":"ApplicationIndexerSync"}'
echo ""
echo "✅ Done!"
