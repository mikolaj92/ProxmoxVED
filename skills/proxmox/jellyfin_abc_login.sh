#!/bin/bash
# Login to Jellyfin as abc user and add admin user

JELLYFIN_URL="http://localhost:8096"

echo "🔑 Loguję jako użytkownik abc..."
LOGIN=$(curl -s -X POST "$JELLYFIN_URL/Users/authenticatebyname" \
  -H "Content-Type: application/json" \
  -H "X-Emby-Authorization: MediaBrowser Client=\"Jellyfin Web\", Device=\"Setup\", DeviceId=\"setup\", Version=\"10.0.0\"" \
  -d '{"Username":"abc","Pw":""}')

echo "$LOGIN" | python3 -m json.tool | head -20
echo ""

# Extract API key
API_KEY=$(echo "$LOGIN" | python3 -c "import json,sys; print(json.load(sys.stdin).get('AccessToken', ''))" 2>/dev/null)

if [ ! -z "$API_KEY" ]; then
    echo "✅ API Key: ${API_KEY:0:30}..."
    echo ""

    echo "👤 Dodaję użytkownika admin..."
    curl -s -X POST "$JELLYFIN_URL/Users/New" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $API_KEY" \
      -d '{
        "Name": "admin",
        "Password": "admin123"
      }' | python3 -m json.tool
    echo ""

    echo "📺 Dodaję bibliotekę TV Shows..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $API_KEY" \
      -d '{
        "Name": "TV Shows",
        "CollectionType": "tvshows",
        "Paths": ["/tv"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    echo "🎬 Dodaję bibliotekę Movies..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $API_KEY" \
      -d '{
        "Name": "Movies",
        "CollectionType": "movies",
        "Paths": ["/movies"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    echo "🎵 Dodaję bibliotekę Music..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $API_KEY" \
      -d '{
        "Name": "Music",
        "CollectionType": "music",
        "Paths": ["/music"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    echo "🔄 Odświeżam biblioteki..."
    curl -s -X POST "$JELLYFIN_URL/Library/Refresh" \
      -H "X-MediaBrowser-Token: $API_KEY" \
      -d '""'
    echo ""
fi

echo "================================"
echo "✅ JELLYFIN SKONFIGUROWANE!"
echo ""
echo "📱 Jellyfin: http://192.168.11.66:8096"
echo "👤 Login: admin / admin123"
