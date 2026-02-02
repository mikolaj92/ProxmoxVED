#!/usr/bin/env bash
set -euo pipefail
# Tail recent jellyseerr logs and show Sonarr/Radarr request lines

docker logs jellyseerr --tail 120 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Sonarr API|Sent request to Radarr|\[Radarr\]|Failed' | tail -120 || true
