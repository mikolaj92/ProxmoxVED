#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'ls -la /app/dist/lib | sed -n "1,80p"'
