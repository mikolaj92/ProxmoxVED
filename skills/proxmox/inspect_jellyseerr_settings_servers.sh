#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json
p='/root/arr-stack/config/jellyseerr/settings.json'
d=json.load(open(p))
for name in ['sonarr','radarr']:
  arr=d.get(name)
  print('\n==',name,'servers==')
  for s in arr:
    print('id', s.get('id'), 'isDefault', s.get('isDefault'), 'activeDirectory', s.get('activeDirectory'))
    for field in ['profiles','rootFolders','tags']:
      v=s.get(field)
      print(' ',field, 'type', type(v).__name__)
      # show short preview
      if isinstance(v, list):
        print('   len', len(v), 'first_keys', list(v[0].keys())[:6] if v else None)
      elif isinstance(v, dict):
        print('   keys', list(v.keys())[:10])
      else:
        print('   value', v)
PY
