#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'nl -ba /app/dist/api/servarr/sonarr.js | sed -n "1,120p"'
