#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'grep -n "buildSeasonList" /app/dist/api/servarr/sonarr.js | sed -n "1,20p"'
docker exec jellyseerr sh -lc 'nl -ba /app/dist/api/servarr/sonarr.js | sed -n "120,220p"'
