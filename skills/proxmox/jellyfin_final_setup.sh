#!/bin/bash
# Add libraries and make admin an administrator

API_KEY="fbc6cd84e2ea4ba8bd2c839384a86f..."
JELLYFIN_URL="http://localhost:8096"
USER_ID="1d142ba0c87a4a8b85f955573a2fd5a0"

echo "🔑 Używam API key abc..."
# Login as abc to get fresh API key
LOGIN=$(curl -s -X POST "$JELLYFIN_URL/Users/authenticatebyname" \
  -H "Content-Type: application/json" \
  -H "X-Emby-Authorization: MediaBrowser Client=\"Jellyfin Web\", Device=\"Setup\", DeviceId=\"setup\", Version=\"10.0.0\"" \
  -d '{"Username":"abc","Pw":""}')

API_KEY=$(echo "$LOGIN" | python3 -c "import json,sys; print(json.load(sys.stdin).get('AccessToken', ''))" 2>/dev/null)

echo "✅ API Key: ${API_KEY:0:30}..."
echo ""

echo "👤 Nadaję uprawnienia admina..."
curl -s -X POST "$JELLYFIN_URL/Users/$USER_ID/Policy" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $API_KEY" \
  -d '{
    "IsAdministrator": true,
    "IsHidden": false,
    "EnableCollectionManagement": true,
    "EnableSubtitleManagement": true,
    "EnableContentDeletion": true
  }' | python3 -m json.tool
echo ""

echo "📺 Dodaję bibliotekę TV Shows (CollectionType: tvshows)..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $API_KEY" \
  -d '{
    "CollectionType": "tvshows",
    "Name": "TV Shows",
    "Paths": ["/tv"],
    "LibraryOptions": {"EnableRealtimeMonitor": false}
  }' | python3 -m json.tool
echo ""

echo "🎬 Dodaję bibliotekę Movies (CollectionType: movies)..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $API_KEY" \
  -d '{
    "CollectionType": "movies",
    "Name": "Movies",
    "Paths": ["/movies"],
    "LibraryOptions": {"EnableRealtimeMonitor": false}
  }' | python3 -m json.tool
echo ""

echo "🎵 Dodaję bibliotekę Music (CollectionType: music)..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $API_KEY" \
  -d '{
    "CollectionType": "music",
    "Name": "Music",
    "Paths": ["/music"],
    "LibraryOptions": {"EnableRealtimeMonitor": false}
  }' | python3 -m json.tool
echo ""

echo "🔄 Skanuję biblioteki..."
curl -s -X POST "$JELLYFIN_URL/Library/Refresh" \
  -H "X-MediaBrowser-Token: $API_KEY" \
  -d '""'
echo ""

echo "✅ GOTOWE!"
