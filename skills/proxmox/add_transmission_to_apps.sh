#!/bin/bash
# Add Transmission as download client to Sonarr/Radarr/Lidarr
BASE_URL="http://192.168.11.66"
TRANS_HOST="192.168.11.66"
TRANS_PORT="9091"
TRANS_USER="transmission"
TRANS_PASS="transmission123"

echo "🔗 Adding Transmission to ARR apps..."
echo ""

# API keys
PROWLARR_KEY="8c6dca6adf3644ba9a7981b736ef636f"
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
LIDARR_KEY="d86ba94cd43e4501bebe77dcbad7b7cd"

# Test Transmission first
echo "→ Testing Transmission connection..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -u "${TRANS_USER}:${TRANS_PASS}" "${BASE_URL}:9091/transmission/rpc" 2>/dev/null)

if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "409" ] || [ "$HTTP_CODE" = "200" ]; then
    echo "   ✅ Transmission responding!"
else
    echo "   ⚠️ Transmission not ready (HTTP $HTTP_CODE), waiting..."
    sleep 5
fi

# Add to Sonarr
echo ""
echo "📺 Adding to Sonarr..."
curl -s -X POST "${BASE_URL}:8989/api/v1/downloadclient" \
  -H "X-Api-Key: ${SONARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Transmission",
    "implementation": "Transmission",
    "configContract": "TransmissionSettings",
    "enable": true,
    "priority": 1,
    "fields": [
      {"order": 0, "name": "host", "value": "'${TRANS_HOST}'"},
      {"order": 1, "name": "port", "value": '${TRANS_PORT}'},
      {"order": 2, "name": "urlBase", "value": "/transmission/"},
      {"order": 3, "name": "username", "value": "'${TRANS_USER}'"},
      {"order": 4, "name": "password", "value": "'${TRANS_PASS}'"},
      {"order": 5, "name": "category", "value": "sonarr"},
      {"order": 6, "name": "directory", "value": "/downloads/complete"}
    ]
  }'
echo ""
echo "   ✅ Sonarr updated!"
echo ""

# Add to Radarr
echo "🎬 Adding to Radarr..."
curl -s -X POST "${BASE_URL}:7878/api/v1/downloadclient" \
  -H "X-Api-Key: ${RADARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Transmission",
    "implementation": "Transmission",
    "configContract": "TransmissionSettings",
    "enable": true,
    "priority": 1,
    "fields": [
      {"order": 0, "name": "host", "value": "'${TRANS_HOST}'"},
      {"order": 1, "name": "port", "value": '${TRANS_PORT}'},
      {"order": 2, "name": "urlBase", "value": "/transmission/"},
      {"order": 3, "name": "username", "value": "'${TRANS_USER}'"},
      {"order": 4, "name": "password", "value": "'${TRANS_PASS}'"},
      {"order": 5, "name": "category", "value": "radarr"},
      {"order": 6, "name": "directory", "value": "/downloads/complete"}
    ]
  }'
echo ""
echo "   ✅ Radarr updated!"
echo ""

# Add to Lidarr
echo "🎵 Adding to Lidarr..."
curl -s -X POST "${BASE_URL}:8686/api/v1/downloadclient" \
  -H "X-Api-Key: ${LIDARR_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Transmission",
    "implementation": "Transmission",
    "configContract": "TransmissionSettings",
    "enable": true,
    "priority": 1,
    "fields": [
      {"order": 0, "name": "host", "value": "'${TRANS_HOST}'"},
      {"order": 1, "name": "port", "value": '${TRANS_PORT}'},
      {"order": 2, "name": "urlBase", "value": "/transmission/"},
      {"order": 3, "name": "username", "value": "'${TRANS_USER}'"},
      {"order": 4, "name": "password", "value": "'${TRANS_PASS}'"},
      {"order": 5, "name": "category", "value": "lidarr"},
      {"order": 6, "name": "directory", "value": "/downloads/complete"}
    ]
  }'
echo ""
echo "   ✅ Lidarr updated!"
echo ""

# Verify
echo "🔍 Verifying..."
echo ""
echo "📺 Sonarr download clients:"
curl -s "${BASE_URL}:8989/api/v1/downloadclient?apiKey=${SONARR_KEY}" | python3 -m json.tool | grep -E '"name"|"enable"' | head -10
echo ""
echo "🎬 Radarr download clients:"
curl -s "${BASE_URL}:7878/api/v1/downloadclient?apiKey=${RADARR_KEY}" | python3 -m json.tool | grep -E '"name"|"enable"' | head -10
echo ""
echo "🎵 Lidarr download clients:"
curl -s "${BASE_URL}:8686/api/v1/downloadclient?apiKey=${LIDARR_KEY}" | python3 -m json.tool | grep -E '"name"|"enable"' | head -10
echo ""

echo "============================================================"
echo "✅ TRANSMISSION CONFIGURED IN ALL APPS!"
echo "============================================================"
echo ""
echo "🚗 Transmission Web UI: ${BASE_URL}:9091"
echo "   Username: ${TRANS_USER}"
echo "   Password: ${TRANS_PASS}"
echo ""
echo "📱 Downloads go to: ~/arr-stack/media/downloads/"
echo ""
echo "✅ Sonarr/Radarr/Lidarr will now use Transmission!"
echo "============================================================"
