#!/bin/bash
echo "🔄 Restartuję Jellyseerr..."
docker restart jellyseerr
sleep 10
echo " ✅"
echo ""

echo "🔍 Sprawdzam status..."
curl -s http://localhost:5055/api/v1/status | python3 -m json.tool | grep version
echo ""

echo "📋 Sprawdzam połączenie Jellyfin..."
curl -s http://localhost:5055/api/v1/settings/public | python3 -c "import json,sys; data=json.load(sys.stdin); j=data.get('jellyfin',{}); print(f'URL: {j.get(\"ip\")}:{j.get(\"port\")}'); print(f'API Key: {j.get(\"apiKey\",\"Not set\")[:50]}...')"
