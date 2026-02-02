#!/bin/bash
# Update Jellyseerr Sonarr/Radarr connection with correct paths

curl -s -c /tmp/jelly-update.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "🔍 Pobieram aktualną konfigurację..."
curl -s -b /tmp/jelly-update.txt http://localhost:5055/api/v1/settings/sonarr > /tmp/sonarr-config.json
curl -s -b /tmp/jelly-update.txt http://localhost:5055/api/v1/settings/radarr > /tmp/radarr-config.json

python3 << 'EOF'
import json

# Update Sonarr
with open('/tmp/sonarr-config.json', 'r') as f:
    sonarr = json.load(f)

for s in sonarr:
    s['activeDirectory'] = '/tv'
    if s.get('name') == 'Sonarr':
        s['isDefault'] = True

with open('/tmp/sonarr-updated.json', 'w') as f:
    json.dump(sonarr, f, indent=2)

# Update Radarr
with open('/tmp/radarr-config.json', 'r') as f:
    radarr = json.load(f)

for r in radarr:
    r['activeDirectory'] = '/movies'
    if r.get('name') == 'Radarr':
        r['isDefault'] = True

with open('/tmp/radarr-updated.json', 'w') as f:
    json.dump(radarr, f, indent=2)

print("✅ Konfiguracja zaktualizowana")
EOF
echo ""

echo "📺 Aktualizuję Sonarr w Jellyseerr..."
curl -s -b /tmp/jelly-update.txt \
  -X POST http://localhost:5055/api/v1/settings/sonarr \
  -H "Content-Type: application/json" \
  -d @/tmp/sonarr-updated.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin), indent=2)[:500])"
echo ""

echo "🎬 Aktualizuję Radarr w Jellyseerr..."
curl -s -b /tmp/jelly-update.txt \
  -X POST http://localhost:5055/api/v1/settings/radarr \
  -H "Content-Type: application/json" \
  -d @/tmp/radarr-updated.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin), indent=2)[:500])"
