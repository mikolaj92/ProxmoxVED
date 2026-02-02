#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'nl -ba /app/dist/lib/settings.js | sed -n "1,220p"'
