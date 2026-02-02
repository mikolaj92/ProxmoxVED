#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json
p='/root/arr-stack/config/jellyseerr/settings.json'
d=json.load(open(p))
for k in ['sonarr','radarr']:
  print('\n==',k,'==')
  v=d.get(k)
  print('type', type(v).__name__)
  if isinstance(v, dict):
    print('keys', list(v.keys()))
    for sub in ['servers','server']:
      if sub in v:
        print(sub,'type', type(v[sub]).__name__)
        if isinstance(v[sub], list):
          print('len', len(v[sub]))
          for s in v[sub]:
            print('  id', s.get('id'), 'isDefault', s.get('isDefault'), 'profiles_type', type(s.get('profiles')).__name__)
        else:
          print(v[sub])
PY
