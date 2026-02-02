#!/usr/bin/env bash
set -euo pipefail
SONARR="http://localhost:8989"
KEY="0375672f0f64474c8843b922d0ab595e"

curl -s "$SONARR/api/v3/series?apiKey=$KEY" > /tmp/sonarr_series.json

ID=$(python3 - <<'PY'
import json
arr=json.load(open('/tmp/sonarr_series.json'))
ids=[s.get('id') for s in arr if s.get('tvdbId')==81797 or s.get('title')=='One Piece']
print(ids[0] if ids else '')
PY
)

echo "series_id=$ID"
if [ -z "$ID" ]; then
  echo "One Piece not present in Sonarr"
  exit 0
fi

code=$(curl -s -o /tmp/sonarr_del.out -w "%{http_code}" \
  -X DELETE "$SONARR/api/v3/series/$ID?deleteFiles=true&addExclusion=false&apiKey=$KEY")

echo "DELETE HTTP $code"
head -200 /tmp/sonarr_del.out || true
