#!/bin/bash
# Configure Jellyfin completely through API

JELLYFIN_URL="http://localhost:8096"

echo "🎬 KONFIGURUJĘ JELLYFIN PRZEZ API..."
echo "================================"
echo ""

# Check if setup is needed
echo "🔍 Sprawdzam status..."
STATUS=$(curl -s "$JELLYFIN_URL/Startup/Configuration")
if [ "$STATUS" != "null" ] && [ ! -z "$STATUS" ]; then
    echo "Setup jest wymagany"
    echo ""

    # Complete startup
    echo "1️⃣ Kończę startup..."
    curl -s -X POST "$JELLYFIN_URL/Startup/Complete" \
      -H "Content-Type: application/json" \
      -d '{"ServerName":"arr-stack","UICulture":"pl"}' | python3 -m json.tool
    echo ""
    sleep 3
else
    echo "Setup już zakończony"
    echo ""
fi

# Create admin user using first-run wizard endpoint
echo "2️⃣ Tworzę użytkownika admina..."
curl -s -X POST "$JELLYFIN_URL/Users/New" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "admin",
    "Password": "admin123"
  }' | python3 -m json.tool
echo ""

# Wait and get API key
sleep 3

echo "3️⃣ Loguję jako admin..."
LOGIN_RESPONSE=$(curl -s -X POST "$JELLYFIN_URL/Users/authenticatebyname" \
  -H "Content-Type: application/json" \
  -H "X-Emby-Authorization: MediaBrowser Client=\"Jellyfin Web\", Device=\"Setup\", DeviceId=\"setup\", Version=\"10.0.0\"" \
  -d '{"Username":"admin","Pw":"admin123"}')

echo "$LOGIN_RESPONSE" | python3 -m json.tool | head -20
echo ""

# Extract API key
ADMIN_KEY=$(echo "$LOGIN_RESPONSE" | python3 -c "import json,sys; print(json.load(sys.stdin).get('AccessToken', ''))" 2>/dev/null)

if [ ! -z "$ADMIN_KEY" ]; then
    echo "API Key: ${ADMIN_KEY:0:30}..."
    echo ""

    # Add TV library
    echo "4️⃣ Dodaję bibliotekę TV Shows..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $ADMIN_KEY" \
      -d '{
        "Name": "TV Shows",
        "CollectionType": "tvshows",
        "Paths": ["/tv"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    # Add Movies library
    echo "5️⃣ Dodaję bibliotekę Movies..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $ADMIN_KEY" \
      -d '{
        "Name": "Movies",
        "CollectionType": "movies",
        "Paths": ["/movies"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    # Add Music library
    echo "6️⃣ Dodaję bibliotekę Music..."
    curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
      -H "Content-Type: application/json" \
      -H "X-MediaBrowser-Token: $ADMIN_KEY" \
      -d '{
        "Name": "Music",
        "CollectionType": "music",
        "Paths": ["/music"],
        "LibraryOptions": {"EnableRealtimeMonitor": false}
      }' | python3 -m json.tool
    echo ""

    # Refresh libraries
    echo "7️⃣ Odświeżam biblioteki..."
    curl -s -X POST "$JELLYFIN_URL/Library/Refresh" \
      -H "X-MediaBrowser-Token: $ADMIN_KEY" \
      -d '""'
    echo ""
fi

echo "================================"
echo "✅ JELLYFIN SKONFIGUROWANE!"
echo ""
echo "📱 Jellyfin URL: http://192.168.11.66:8096"
echo "👤 Login: admin / admin123"
