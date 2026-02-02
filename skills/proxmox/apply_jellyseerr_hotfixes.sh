#!/usr/bin/env bash
set -euo pipefail

# 1) Fix request list crash (profiles.find not a function)
docker exec jellyseerr node -e '
const fs=require("fs");
const f="/app/dist/routes/request.js";
let s=fs.readFileSync(f,"utf8");
if(!s.includes("HOTFIX: ensure profiles is always an array")){
  const idx=s.indexOf("const radarrServers = await Promise.all(settings.radarr.map(async (radarrSetting) => {");
  if(idx<0) throw new Error("needle not found");
  const end=s.indexOf("}));", idx);
  if(end<0) throw new Error("end marker not found");
  const insertPos=end+4;
  const insert="\n        // HOTFIX: ensure profiles is always an array (prevents request list crash)\n        sonarrServers.forEach((srv)=>{ if (srv && !Array.isArray(srv.profiles)) srv.profiles = []; });\n        radarrServers.forEach((srv)=>{ if (srv && !Array.isArray(srv.profiles)) srv.profiles = []; });\n";
  s=s.slice(0,insertPos)+insert+s.slice(insertPos);
  fs.writeFileSync(f,s);
  console.log("patched",f);
} else {
  console.log("request hotfix already present");
}
'

# 2) Fix Sonarr addSeries crash when lookup seasons missing
docker exec jellyseerr node -e '
const fs=require("fs");
const f="/app/dist/api/servarr/sonarr.js";
let s=fs.readFileSync(f,"utf8");
if(!s.includes("HOTFIX: guard missing seasons from lookup")){
  const target="seasons: this.buildSeasonList(options.seasons, series.seasons.map((season) => ({";
  if(!s.includes(target)) throw new Error("target not found");
  const repl="seasons: this.buildSeasonList(options.seasons, (series.seasons || []).map((season) => ({\n                    // HOTFIX: guard missing seasons from lookup\n";
  s=s.replace(target,repl);
  fs.writeFileSync(f,s);
  console.log("patched",f);
} else {
  console.log("sonarr seasons hotfix already present");
}
'

# 3) Fix Servarr auth: use X-Api-Key header instead of query param apikey (POST returns 405 otherwise)
docker exec jellyseerr node -e '
const fs=require("fs");
const f="/app/dist/api/servarr/base.js";
let s=fs.readFileSync(f,"utf8");
if(!s.includes("HOTFIX: use X-Api-Key header")){
  // Replace only the params object { apikey: apiKey } with {} and inject headers option
  s = s.replace(/super\(url,\s*\{\s*apikey:\s*apiKey,\s*\},\s*\{\s*nodeCache:\s*cache_1\.default\.getCache\(cacheName\)\.data,\s*\}\s*\);/m,
    "super(url, {}, {\n            // HOTFIX: use X-Api-Key header (query apikey breaks POST with 405 on Sonarr/Radarr)\n            headers: { \"X-Api-Key\": apiKey },\n            nodeCache: cache_1.default.getCache(cacheName).data,\n        });"
  );
  if(!s.includes('headers: { "X-Api-Key": apiKey }')) throw new Error("auth patch failed");
  fs.writeFileSync(f,s);
  console.log("patched",f);
} else {
  console.log("servarr auth hotfix already present");
}
'

# restart
docker restart jellyseerr >/dev/null
sleep 6

# quick smoke tests
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

echo "== /api/v1/request (head) =="
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=3&skip=0" | head -c 200; echo

echo "== try request Breaking Bad S1 =="
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' | head -c 200; echo

echo "== jellyseerr tail =="
docker logs jellyseerr --tail 60 2>&1 | grep -E "Sent request to Sonarr|Sonarr accepted|Sonarr API|Failed" | tail -60 || true
