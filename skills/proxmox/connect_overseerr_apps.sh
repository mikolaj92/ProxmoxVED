#!/bin/bash
# Connect Overseerr to other apps using session

echo "🔑 Pobieram sesję cookie..."
curl -s -c /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

echo "📺 Dodaję Sonarr..."
curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sonarr",
    "type": "sonarr",
    "hostname": "192.168.11.66",
    "port": 8989,
    "apiKey": "0375672f0f64474c8843b922d0ab595e",
    "active": true
  }' | python3 -m json.tool
echo ""

echo "🎬 Dodaję Radarr..."
curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Radarr",
    "type": "radarr",
    "hostname": "192.168.11.66",
    "port": 7878,
    "apiKey": "e2166ae2a7284752a3d6b95423485f42",
    "active": true
  }' | python3 -m json.tool
echo ""

echo "🎵 Dodaję Lidarr..."
curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lidarr",
    "type": "lidarr",
    "hostname": "192.168.11.66",
    "port": 8686,
    "apiKey": "d86ba94cd43e4501bebe77dcbad7b7cd",
    "active": true
  }' | python3 -m json.tool
echo ""

echo "📺 Dodaję Jellyfin..."
curl -s -b /tmp/overseerr-cookies.txt \
  -X POST http://localhost:5055/api/v1/settings/servers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jellyfin",
    "type": "jellyfin",
    "hostname": "192.168.11.66",
    "port": 8096,
    "apiKey": "",
    "active": true
  }' | python3 -m json.tool
echo ""

echo "✅ Sprawdzam połączone servery..."
curl -s -b /tmp/overseerr-cookies.txt http://localhost:5055/api/v1/settings/servers | python3 -m json.tool | grep -E "id|name|type|active"
