#!/bin/bash
# Configure Jellyseerr via GET + UPDATE

API_BASE="http://localhost:5055/api/v1"

# Login
echo "🔑 Loguję..."
curl -s -c /tmp/jelly-cookies.txt \
  -X POST $API_BASE/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null
echo " ✅"
echo ""

# Get current settings
echo "📋 Pobieram aktualne ustawienia..."
curl -s -b /tmp/jelly-cookies.txt $API_BASE/settings/main > /tmp/jelly-settings.json
cat /tmp/jelly-settings.json | python3 -m json.tool > /dev/null
echo " ✅"
echo ""

# Update with Python
python3 << 'EOF'
import json

# Load current settings
with open('/tmp/jelly-settings.json', 'r') as f:
    data = json.load(f)

# Update Sonarr
data['sonarr'] = [{
    "id": 1,
    "name": "Sonarr",
    "hostname": "192.168.11.66",
    "port": 8989,
    "apiKey": "0375672f0f64474c8843b922d0ab595e",
    "useSsl": False,
    "baseUrl": "/",
    "active": True,
    "is4k": False,
    "isDefault": True,
    "activeProfileId": 1,
    "activeProfileName": "Any",
    "activeDirectory": "/tv",
    "enableSeasonFolders": False
}]

# Update Radarr
data['radarr'] = [{
    "id": 1,
    "name": "Radarr",
    "hostname": "192.168.11.66",
    "port": 7878,
    "apiKey": "e2166ae2a7284752a3d6b95423485f42",
    "useSsl": False,
    "baseUrl": "/",
    "active": True,
    "is4k": False,
    "isDefault": True,
    "activeProfileId": 1,
    "activeProfileName": "Any",
    "activeDirectory": "/movies",
    "minimumAvailability": "released"
}]

# Update Jellyfin
data['jellyfin'] = {
    "name": "Jellyfin",
    "ip": "192.168.11.66",
    "port": 8096,
    "useSsl": False,
    "urlBase": "",
    "apiKey": "61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
}

# Save updated settings
with open('/tmp/jelly-settings-updated.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Ustawienia zaktualizowane")
print(f"\nSonarr: {len(data['sonarr'])} serwerów")
print(f"Radarr: {len(data['radarr'])} serwerów")
print(f"Jellyfin: {data['jellyfin']['ip']}:{data['jellyfin']['port']}")
EOF
echo ""

# Send updated settings back
echo "💾 Zapisuję ustawienia przez API..."
curl -s -b /tmp/jelly-cookies.txt \
  -X PUT $API_BASE/settings/main \
  -H "Content-Type: application/json" \
  -d @/tmp/jelly-settings-updated.json | python3 -m json.tool
echo ""

echo "🔍 Weryfikuję..."
curl -s -b /tmp/jelly-cookies.txt $API_BASE/settings/main | python3 -c "import json,sys; d=json.load(sys.stdin); print('Sonarr:', len(d.get('sonarr',[]))); print('Radarr:', len(d.get('radarr',[]))); print('Jellyfin:', d.get('jellyfin',{}).get('ip','Not set'))"
