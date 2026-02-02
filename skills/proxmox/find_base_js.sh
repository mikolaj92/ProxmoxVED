#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'find /app -name base.js | grep servarr | sed -n "1,10p"'
