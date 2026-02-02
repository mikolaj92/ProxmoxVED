#!/usr/bin/env bash
set -euo pipefail
docker exec jellyseerr sh -lc 'ls -la dist | sed -n "1,30p"'
