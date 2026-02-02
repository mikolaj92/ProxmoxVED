#!/usr/bin/env bash
set -euo pipefail
FILE=/app/dist/api/servarr/base.js

# Patch ServarrBase to use X-Api-Key header instead of query param `apikey`
docker exec -e FILE="$FILE" jellyseerr node -e '
const fs=require("fs");
const file=process.env.FILE;
let s=fs.readFileSync(file,"utf8");
if(s.includes("HOTFIX: use X-Api-Key header")){
  console.log("patch already present");
  process.exit(0);
}
// Find the super(url, { apikey: apiKey }, { nodeCache: ... }) call and replace it.
const re = /super\(url,\s*\{\s*apikey:\s*apiKey,\s*\},\s*\{\s*nodeCache:([^}]+)\}\s*\);/m;
const m = s.match(re);
if(!m){
  console.error("pattern not found");
  process.exit(1);
}
const nodeCachePart = m[1].trim();
const replacement = `super(url, {}, {\n            // HOTFIX: use X-Api-Key header (query apikey breaks POST with 405 on Sonarr/Radarr)\n            headers: { 'X-Api-Key': apiKey },\n            nodeCache:${nodeCachePart}\n        });`;
s = s.replace(re, replacement);
fs.writeFileSync(file, s);
console.log("patched", file);
'

docker restart jellyseerr >/dev/null
sleep 6

echo "== quick test: create Sonarr add series via Jellyseerr request (Breaking Bad S1) =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' | head -c 220; echo

sleep 2

echo "== jellyseerr log tail (Sonarr/Radarr) =="
docker logs jellyseerr --tail 80 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Sonarr API|Sent request to Radarr|\[Radarr\]|Failed' | tail -80 || true
