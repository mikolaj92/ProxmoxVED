#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/settings/sonarr" > /tmp/jelly_sonarr.json
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/settings/radarr" > /tmp/jelly_radarr.json

echo "== sonarr file size =="
wc -c /tmp/jelly_sonarr.json
python3 - <<'PY'
import json
arr=json.load(open('/tmp/jelly_sonarr.json'))
print('servers', len(arr))
for s in arr:
  print('id', s.get('id'), 'profiles', type(s.get('profiles')).__name__, 'profiles_len', len(s.get('profiles') or []))
PY

echo "== radarr file size =="
wc -c /tmp/jelly_radarr.json
python3 - <<'PY'
import json
arr=json.load(open('/tmp/jelly_radarr.json'))
print('servers', len(arr))
for s in arr:
  print('id', s.get('id'), 'profiles', type(s.get('profiles')).__name__, 'profiles_len', len(s.get('profiles') or []))
PY
