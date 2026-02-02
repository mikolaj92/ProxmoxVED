#!/usr/bin/env bash
set -euo pipefail
FILE=/app/dist/api/servarr/sonarr.js

docker exec -e FILE="$FILE" jellyseerr node -e '
const fs=require("fs");
const file=process.env.FILE;
let s=fs.readFileSync(file,"utf8");
if(s.includes("HOTFIX: guard missing seasons from lookup")){
  console.log("patch already present");
  process.exit(0);
}
// Replace: series.seasons.map((season) => ({
// with guarded version
const target = "seasons: this.buildSeasonList(options.seasons, series.seasons.map((season) => ({";
if(!s.includes(target)){
  console.error("target not found");
  process.exit(1);
}
const repl = "seasons: this.buildSeasonList(options.seasons, (series.seasons || []).map((season) => ({\n                    // HOTFIX: guard missing seasons from lookup\n";
s = s.replace(target, repl);
fs.writeFileSync(file, s);
console.log("patched", file);
' ;

docker restart jellyseerr >/dev/null
sleep 6

echo "== test request create (Breaking Bad S1) =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}' | head -c 220; echo

echo "== jellyseerr log tail (sonarr) =="
docker logs jellyseerr --tail 60 2>&1 | grep -E "Sent request to Sonarr|Sonarr API|Sonarr accepted|Failed" | tail -30 || true
