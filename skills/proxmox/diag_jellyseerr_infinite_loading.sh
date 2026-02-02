#!/usr/bin/env bash
set -euo pipefail
JELLY=http://localhost:5055

# auth
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== /api/v1/status =="
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/status" | head -c 500; echo

echo "== /api/v1/request?take=5&skip=0 =="
resp=$(curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=5&skip=0")
echo "$resp" | head -c 500; echo

echo "== quick JSON parse (keys) =="
python3 - <<'PY'
import json,sys
raw=sys.stdin.read()
try:
  j=json.loads(raw)
  print('keys', list(j.keys()))
except Exception as e:
  print('not json:', e)
PY
<<<"$resp"

echo "== Jellyseerr logs (tail, errors) =="
docker logs jellyseerr --tail 220 2>&1 | egrep -i 'error|exception|TypeError|request\]' | tail -160 || true

echo "== settings.json server cache sanity =="
python3 - <<'PY'
import json
p='/root/arr-stack/config/jellyseerr/settings.json'
d=json.load(open(p))
for name in ['sonarr','radarr']:
  arr=d.get(name) or []
  print(name, 'len', len(arr))
  for s in arr:
    print(' id', s.get('id'), 'default', s.get('isDefault'), 'profiles', type(s.get('profiles')).__name__, 'rootFolders', type(s.get('rootFolders')).__name__)
PY
