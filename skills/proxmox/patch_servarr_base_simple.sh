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
const old = "super(url, {\n            apikey: apiKey,\n        }, {\n            nodeCache: cache_1.default.getCache(cacheName).data,\n        });";
if(!s.includes(old)){
  console.error("old snippet not found");
  process.exit(1);
}
const neu = "super(url, {}, {\n            // HOTFIX: use X-Api-Key header (query apikey breaks POST with 405 on Sonarr/Radarr)\n            headers: { \"X-Api-Key\": apiKey },\n            nodeCache: cache_1.default.getCache(cacheName).data,\n        });";
s = s.replace(old, neu);
fs.writeFileSync(f,s);
console.log("patched", f);
'

docker restart jellyseerr >/dev/null
sleep 6

echo "== jellyseerr ready =="
docker logs jellyseerr --tail 20 2>&1 | grep -E 'Starting Jellyseerr version|Server ready' || true
