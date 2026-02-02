#!/usr/bin/env bash
set -euo pipefail
docker logs jellyseerr --tail 120 2>&1 | grep -E "Media Request|Sonarr|Radarr" | tail -80 || true
