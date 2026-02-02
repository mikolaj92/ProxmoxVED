#!/usr/bin/env bash
set -euo pipefail
# search in dist for the failing expression

docker exec jellyseerr sh -lc 'grep -R "profiles" -n dist/routes dist/api 2>/dev/null | grep -E "sonarrServers|profiles" | sed -n "1,20p"'
