#!/usr/bin/env bash
set -euo pipefail

echo "== Sonarr: recent commands =="
python3 -c "
import json, urllib.request
cmds = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/command?apikey=0375672f0f64474c8843b922d0ab595e'))
for c in cmds[:10]:
    print(f'{c.get(\"name\")}: status={c.get(\"status\")}, started={c.get(\"started\")}, ended={c.get(\"ended\")}')

print()
print('== Last SeasonSearch command details ==')
for c in cmds:
    if c.get('name') == 'SeasonSearch':
        print(f'name: {c.get(\"name\")}')
        print(f'status: {c.get(\"status\")}')
        print(f'started: {c.get(\"started\")}')
        print(f'ended: {c.get(\"ended\")}')
        print(f'body: {c.get(\"body\")}')
        break
" 2>/dev/null
