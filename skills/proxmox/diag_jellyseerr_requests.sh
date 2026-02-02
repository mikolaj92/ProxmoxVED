#!/usr/bin/env bash
set -euo pipefail

SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
JELLY_URL="http://localhost:5055"
SONARR_URL="http://localhost:8989"
RADARR_URL="http://localhost:7878"

need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing $1" >&2; exit 1; }; }
need curl
need python3

echo "== Jellyseerr auth (cookie) =="
curl -s -c /tmp/jelly.cookie \
  -X POST "$JELLY_URL/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' \
| python3 -c 'import sys,json
try:
  d=json.load(sys.stdin)
  print({"ok": d.get("user") is not None, "user": (d.get("user") or {}).get("email")})
except Exception as e:
  print({"ok": False, "error": str(e)})'

echo
echo "== Jellyseerr settings (sonarr/radarr) =="
echo "-- sonarr"
curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/settings/sonarr" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  for s in arr:
    out={k:s.get(k) for k in ["id","name","hostname","port","baseUrl","active","isDefault","activeDirectory","activeProfileId","activeProfileName"]}
    print(out)
except Exception as e:
  print({"error": str(e)})'

echo "-- radarr"
curl -s -b /tmp/jelly.cookie "$JELLY_URL/api/v1/settings/radarr" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  for s in arr:
    out={k:s.get(k) for k in ["id","name","hostname","port","baseUrl","active","isDefault","activeDirectory","activeProfileId","activeProfileName"]}
    print(out)
except Exception as e:
  print({"error": str(e)})'

echo
echo "== Direct Sonarr API test =="
curl -s "$SONARR_URL/api/v3/system/status?apiKey=$SONARR_KEY" \
| python3 -c 'import sys,json
try:
  d=json.load(sys.stdin)
  print({k:d.get(k) for k in ["appName","version","instanceName","osName"]})
except Exception as e:
  print({"error": str(e)})'
curl -s "$SONARR_URL/api/v3/rootfolder?apiKey=$SONARR_KEY" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  for r in arr:
    print({k:r.get(k) for k in ["id","path","accessible"]})
except Exception as e:
  print({"error": str(e)})'
curl -s "$SONARR_URL/api/v3/qualityprofile?apiKey=$SONARR_KEY" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  if arr:
    d=arr[0]
    print({k:d.get(k) for k in ["id","name","cutoff"]})
  else:
    print([])
except Exception as e:
  print({"error": str(e)})'

echo
echo "== Direct Radarr API test =="
curl -s "$RADARR_URL/api/v3/system/status?apiKey=$RADARR_KEY" \
| python3 -c 'import sys,json
try:
  d=json.load(sys.stdin)
  print({k:d.get(k) for k in ["appName","version","instanceName","osName"]})
except Exception as e:
  print({"error": str(e)})'
curl -s "$RADARR_URL/api/v3/rootfolder?apiKey=$RADARR_KEY" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  for r in arr:
    print({k:r.get(k) for k in ["id","path","accessible"]})
except Exception as e:
  print({"error": str(e)})'
curl -s "$RADARR_URL/api/v3/qualityprofile?apiKey=$RADARR_KEY" \
| python3 -c 'import sys,json
try:
  arr=json.load(sys.stdin)
  if arr:
    d=arr[0]
    print({k:d.get(k) for k in ["id","name","cutoff"]})
  else:
    print([])
except Exception as e:
  print({"error": str(e)})'

echo
echo "== Jellyseerr container logs (errors/warnings last 200) =="
docker logs jellyseerr --tail 200 2>&1 \
| egrep -i "error|warn|exception|sonarr|radarr" \
| tail -120 || true
