#!/bin/bash
# Configure Jellyfin startup

JELLYFIN_URL="http://localhost:8096"

echo "🔍 Sprawdzam czy Jellyfin wymaga setup..."
curl -s "$JELLYFIN_URL/Startup/Configuration" | python3 -m json.tool | head -30
