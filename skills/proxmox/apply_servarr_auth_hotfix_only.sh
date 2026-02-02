#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr node -e '
const fs=require("fs");
const f="/app/dist/api/servarr/base.js";
let s=fs.readFileSync(f,"utf8");
if(s.includes("HOTFIX: use X-Api-Key header")){
  console.log("already patched");
  process.exit(0);
}
const pattern=/super\(url,\s*\{\s*apikey:\s*apiKey,\s*\},\s*\{\s*nodeCache:\s*cache_1\.default\.getCache\(cacheName\)\.data,\s*\}\s*\);/m;
if(!pattern.test(s)){
  console.error("pattern not found");
  process.exit(1);
}
s = s.replace(pattern,
  "super(url, {}, {\n            // HOTFIX: use X-Api-Key header (query apikey breaks POST with 405 on Sonarr/Radarr)\n            headers: { \\\"X-Api-Key\\\": apiKey },\n            nodeCache: cache_1.default.getCache(cacheName).data,\n        });"
);
if(!s.includes("\"X-Api-Key\"")){
  console.error("replacement sanity check failed");
  process.exit(1);
}
fs.writeFileSync(f,s);
console.log("patched", f);
'

docker restart jellyseerr >/dev/null
sleep 6

echo "== jellyseerr ready =="
docker logs jellyseerr --tail 20 2>&1 | grep -E 'Starting Jellyseerr version|Server ready' || true
