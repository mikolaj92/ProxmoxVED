#!/bin/bash
# Add default indexer to Prowlarr
PROWLARR_KEY="8c6dca6adf3644ba9a7981b736ef636f"
BASE_URL="http://192.168.11.66"

echo "📡 Adding Cardigann (built-in) indexer..."

# Try to add Cardigann indexer
curl -s -X POST "${BASE_URL}:9696/api/v1/indexer" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cardigann",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": true,
    "baseSettings": {
      "url": "https://cardigann.example.com"
    }
  }' && echo " ✅ Indexer added" || echo " ⚠️ Indexer setup requires manual configuration"

echo ""
echo "📋 INDEXER SETUP REQUIRED"
echo "=============================="
echo "Prowlarr needs indexers to find content."
echo ""
echo "FREE OPTIONS:"
echo "  1. Cardigann (built-in, needs manual URL config)"
echo "  2. Jackett (run separate container)"
echo ""
echo "PAID OPTIONS (recommended):"
echo "  3. NZBGeek - https://nzbgeek.info"
echo "  4. DogNZB - https://dognzb.cr"
echo "  5. NZB.su - https://nzb.su"
echo ""
echo "To add indexers:"
echo "  1. Open: http://192.168.11.66:9696"
echo "  2. Go to: Indexers → Add → Torznab/Newznab"
echo "  3. Enter your indexer credentials"
echo "=============================="
