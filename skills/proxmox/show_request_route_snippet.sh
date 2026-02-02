#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr sh -lc 'nl -ba dist/routes/request.js | sed -n "130,210p"'

docker exec jellyseerr sh -lc 'nl -ba dist/api/servarr/base.js | sed -n "1,120p"'
