#!/usr/bin/env bash
set -euo pipefail

docker restart jellyseerr >/dev/null
sleep 6

docker logs jellyseerr --tail 20 2>&1 | grep -E 'Starting Jellyseerr version|Server ready' || true
