#!/usr/bin/env bash
set -euo pipefail
python3 - <<'PY'
import json
p='/root/arr-stack/config/jellyseerr/settings.old.json'
d=json.load(open(p))
son=d.get('sonarr')
rad=d.get('radarr')
print('old sonarr type', type(son).__name__, 'len', len(son) if isinstance(son,list) else None)
if isinstance(son,list) and son:
  print('old sonarr profiles type', type(son[0].get('profiles')).__name__)
print('old radarr type', type(rad).__name__, 'len', len(rad) if isinstance(rad,list) else None)
if isinstance(rad,list) and rad:
  print('old radarr profiles type', type(rad[0].get('profiles')).__name__)
PY
