#!/usr/bin/env bash
set -euo pipefail

FILE=/app/dist/routes/request.js

# Patch with node (no perl in container)
docker exec -e FILE="$FILE" jellyseerr node -e '
const fs=require("fs");
const file=process.env.FILE;
let s=fs.readFileSync(file,"utf8");
if(s.includes("HOTFIX: ensure profiles is always an array")){
  console.log("patch already present");
  process.exit(0);
}
const needle = "const radarrServers = await Promise.all(settings.radarr.map(async (radarrSetting) => {";
const idx = s.indexOf(needle);
if(idx<0){ console.error("needle not found"); process.exit(1); }
const end = s.indexOf("}));", idx);
if(end<0){ console.error("end marker not found"); process.exit(1); }
const insertPos = end + "}));".length;
const insert = "\n        // HOTFIX: ensure profiles is always an array (prevents request list crash)\n        sonarrServers.forEach((srv)=>{ if (srv && !Array.isArray(srv.profiles)) srv.profiles = []; });\n        radarrServers.forEach((srv)=>{ if (srv && !Array.isArray(srv.profiles)) srv.profiles = []; });\n";
s = s.slice(0, insertPos) + insert + s.slice(insertPos);
fs.writeFileSync(file, s);
console.log("patched", file);
'

docker restart jellyseerr >/dev/null
sleep 6

# Test endpoint
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=10&skip=0" | head -c 500; echo
