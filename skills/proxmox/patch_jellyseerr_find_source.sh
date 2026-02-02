#!/usr/bin/env bash
set -euo pipefail

docker exec jellyseerr sh -lc 'grep -R "sonarrServers\.find" -n dist 2>/dev/null | sed -n "1,10p"'
