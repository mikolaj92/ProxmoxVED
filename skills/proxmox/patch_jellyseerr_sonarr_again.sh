#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr node -e '
const fs=require("fs");
const f="/app/dist/api/servarr/sonarr.js";
let s=fs.readFileSync(f,"utf8");
if(!s.includes("HOTFIX: guard missing seasons from lookup")){
  const target="seasons: this.buildSeasonList(options.seasons, series.seasons.map((season) => ({";
  const repl="seasons: this.buildSeasonList(options.seasons, (series.seasons || []).map((season) => ({\n                    // HOTFIX: guard missing seasons from lookup\n";
  if(!s.includes(target)) throw new Error("target missing");
  s=s.replace(target,repl);
  fs.writeFileSync(f,s);
  console.log("patched sonarr.js");
} else {
  console.log("already patched");
}
'

docker restart jellyseerr >/dev/null
sleep 6

docker logs jellyseerr --tail 10 2>&1 | grep -E 'Starting Jellyseerr version|Server ready' || true
