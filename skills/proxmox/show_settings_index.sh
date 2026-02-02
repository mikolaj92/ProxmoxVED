#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'ls -la /app/dist/lib/settings | sed -n "1,80p"'
docker exec jellyseerr sh -lc 'nl -ba /app/dist/lib/settings/index.js | sed -n "1,220p"'
