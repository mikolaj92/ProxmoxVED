#!/bin/bash
# Complete Jellyfin setup

JELLYFIN_URL="http://localhost:8096"

echo "🎬 KONFIGURUJĘ JELLYFIN..."
echo "================================"
echo ""

# Step 1: Complete startup configuration
echo "1️⃣ Kończę setup startup..."
curl -s -X POST "$JELLYFIN_URL/Startup/Complete" \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool
echo ""

# Step 2: Create admin user
echo "2️⃣ Tworzę użytkownika admina..."
curl -s -X POST "$JELLYFIN_URL/Users/New" \
  -H "Content-Type: application/json" \
  -d '{
    "Name": "admin",
    "Password": "admin123"
  }' | python3 -m json.tool
echo ""

# Wait for user creation
sleep 3

# Step 3: Get admin API key
echo "3️⃣ Generuję API key dla admina..."
ADMIN_KEY=$(curl -s -X POST "$JELLYFIN_URL/Users/authenticatebyname" \
  -H "Content-Type: application/json" \
  -H "X-Emby-Authorization: \"MediaBrowser Client=\"Jellyfin Web\", Device=\"Jellyseerr\", DeviceId=\"jellyseerr-setup\", Version=\"1.0.0\"" \
  -d '{
    "Username": "admin",
    "Pw": "admin123"
  }' | python3 -c "import json,sys; print(json.load(sys.stdin).get('AccessToken', ''))")

echo "API Key: ${ADMIN_KEY:0:30}..."
echo ""

# Step 4: Add TV library
echo "4️⃣ Dodaję bibliotekę TV Shows..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $ADMIN_KEY" \
  -d '{
    "Name": "TV Shows",
    "CollectionType": "tvshows",
    "Paths": ["/tv"],
    "LibraryOptions": {
      "EnableArchiveMediaFiles": false,
      "EnablePhotos": false,
      "EnableRealtimeMonitor": false
    }
  }' | python3 -m json.tool
echo ""

# Step 5: Add Movies library
echo "5️⃣ Dodaję bibliotekę Movies..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $ADMIN_KEY" \
  -d '{
    "Name": "Movies",
    "CollectionType": "movies",
    "Paths": ["/movies"],
    "LibraryOptions": {
      "EnableArchiveMediaFiles": false,
      "EnablePhotos": false,
      "EnableRealtimeMonitor": false
    }
  }' | python3 -m json.tool
echo ""

# Step 6: Add Music library
echo "6️⃣ Dodaję bibliotekę Music..."
curl -s -X POST "$JELLYFIN_URL/Library/VirtualFolders" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $ADMIN_KEY" \
  -d '{
    "Name": "Music",
    "CollectionType": "music",
    "Paths": ["/music"],
    "LibraryOptions": {
      "EnableArchiveMediaFiles": false,
      "EnablePhotos": false,
      "EnableRealtimeMonitor": false
    }
  }' | python3 -m json.tool
echo ""

# Step 7: Trigger library scan
echo "7️⃣ Skanuję biblioteki..."
curl -s -X POST "$JELLYFIN_URL/Library/Refresh" \
  -H "Content-Type: application/json" \
  -H "X-MediaBrowser-Token: $ADMIN_KEY" \
  -d '""'
echo ""

echo "================================"
echo "✅ JELLYFIN SKONFIGUROWANE!"
echo ""
echo "📱 Jellyfin URL: http://192.168.11.66:8096"
echo "👤 Login: admin / admin123"
