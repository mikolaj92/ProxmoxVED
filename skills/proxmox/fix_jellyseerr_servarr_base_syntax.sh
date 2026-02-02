#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr node -e 'const fs=require("fs"); const f="/app/dist/api/servarr/base.js"; let s=fs.readFileSync(f,"utf8"); s=s.replace(/headers:\s*\{\s*X-Api-Key:\s*apiKey\s*\}/g, "headers: { \"X-Api-Key\": apiKey }"); fs.writeFileSync(f,s); console.log("fixed header key quoting");'

docker restart jellyseerr >/dev/null
sleep 6

echo "== jellyseerr ready? =="
docker logs jellyseerr --tail 20 2>&1 | egrep -i 'Server ready|Starting Jellyseerr version' || true
