#!/usr/bin/env bash
set -euo pipefail
APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)

curl -s "http://localhost:9696/api/v1/applications/schema?apikey=$APIKEY" > /tmp/prowlarr_appschema.json
python3 - <<'PY'
import json
arr=json.load(open('/tmp/prowlarr_appschema.json'))
for impl in ['Sonarr','Radarr']:
  x=next(i for i in arr if i.get('implementation')==impl)
  keys=['name','implementation','configContract','syncLevel','enable']
  print(impl, {k:x.get(k) for k in keys})
PY
