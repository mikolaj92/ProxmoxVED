#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'grep -R "getRolling" -n dist/api/externalapi.js dist/api/externalapi/*.js dist/api 2>/dev/null | sed -n "1,20p"'
docker exec jellyseerr sh -lc 'nl -ba dist/api/externalapi.js | sed -n "1,220p"'
