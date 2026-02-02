#!/usr/bin/env bash
set -euo pipefail
# run inside jellyseerr container
cat > /tmp/check.js <<'NODE'
const fs = require('fs');
const path = '/app/config/settings.json';
const d = JSON.parse(fs.readFileSync(path,'utf8'));
const sonarr = d.sonarr;
console.log('sonarr type', Array.isArray(sonarr), 'len', sonarr?.length);
if (Array.isArray(sonarr)) {
  for (const s of sonarr) {
    console.log('server id', s.id, 'profiles isArray', Array.isArray(s.profiles), 'profiles typeof', typeof s.profiles);
  }
}
NODE

docker exec jellyseerr node /tmp/check.js
