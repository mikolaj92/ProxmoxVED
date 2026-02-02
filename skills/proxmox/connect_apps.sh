#!/bin/bash
# Connect ARR apps via API
PROWLARR_KEY="8c6dca6adf3644ba9a7981b736ef636f"
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
LIDARR_KEY="d86ba94cd43e4501bebe77dcbad7b7cd"
BASE_URL="http://192.168.11.66"

echo "🔗 Connecting ARR apps..."
echo ""

# Add Sonarr to Prowlarr
echo "📡 Adding Sonarr to Prowlarr..."
curl -s -X POST "${BASE_URL}:9696/api/v1/application" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Sonarr\",
    \"implementation\": \"Sonarr\",
    \"configContract\": \"SonarrSettings\",
    \"syncLevel\": 0,
    \"enabled\": true,
    \"apiKey\": \"${SONARR_KEY}\",
    \"baseUrl\": \"${BASE_URL}:8989\"
  }" && echo " ✅ Sonarr added" || echo " ❌ Failed"
echo ""

# Add Radarr to Prowlarr
echo "📡 Adding Radarr to Prowlarr..."
curl -s -X POST "${BASE_URL}:9696/api/v1/application" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Radarr\",
    \"implementation\": \"Radarr\",
    \"configContract\": \"RadarrSettings\",
    \"syncLevel\": 0,
    \"enabled\": true,
    \"apiKey\": \"${RADARR_KEY}\",
    \"baseUrl\": \"${BASE_URL}:7878\"
  }" && echo " ✅ Radarr added" || echo " ❌ Failed"
echo ""

# Add Lidarr to Prowlarr
echo "📡 Adding Lidarr to Prowlarr..."
curl -s -X POST "${BASE_URL}:9696/api/v1/application" \
  -H "X-Api-Key: ${PROWLARR_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Lidarr\",
    \"implementation\": \"Lidarr\",
    \"configContract\": \"LidarrSettings\",
    \"syncLevel\": 0,
    \"enabled\": true,
    \"apiKey\": \"${LIDARR_KEY}\",
    \"baseUrl\": \"${BASE_URL}:8686\"
  }" && echo " ✅ Lidarr added" || echo " ❌ Failed"
echo ""

# Verify connections
echo "🔍 Verifying connections..."
curl -s "${BASE_URL}:9696/api/v1/application" \
  -H "X-Api-Key: ${PROWLARR_KEY}" | python3 -m json.tool
echo ""

echo "✅ Setup complete!"
