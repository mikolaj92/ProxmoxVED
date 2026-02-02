#!/usr/bin/env bash
set -euo pipefail

echo "== jellyseerr last 120 lines containing Sonarr/Radarr request =="
docker logs jellyseerr --tail 200 2>&1 | grep -E 'Sent request to Sonarr|Sent request to Radarr|Sonarr accepted|Radarr|Sonarr API|Failed to add' | tail -200 || true
