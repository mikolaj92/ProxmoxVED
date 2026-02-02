#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr sh -lc 'command -v curl >/dev/null 2>&1 || (apk add --no-cache curl >/dev/null)'

echo "== From inside jellyseerr container -> Radarr system/status =="
docker exec jellyseerr sh -lc 'curl -s -o /tmp/out -w "%{http_code}" -X GET "http://192.168.11.66:7878/api/v3/system/status" -H "X-Api-Key: e2166ae2a7284752a3d6b95423485f42"; echo; head -20 /tmp/out'

echo
echo "== From inside jellyseerr container -> Sonarr system/status =="
docker exec jellyseerr sh -lc 'curl -s -o /tmp/out -w "%{http_code}" -X GET "http://192.168.11.66:8989/api/v3/system/status" -H "X-Api-Key: 0375672f0f64474c8843b922d0ab595e"; echo; head -20 /tmp/out'
