#!/usr/bin/env bash
set -euo pipefail

docker rm -f jellyseerr >/dev/null 2>&1 || true

docker run -d \
  --name jellyseerr \
  --network host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Warsaw \
  -e LOG_LEVEL=info \
  -v /root/arr-stack/config/jellyseerr:/app/config \
  --restart unless-stopped \
  fallenbagel/jellyseerr:latest >/dev/null

sleep 8

docker logs jellyseerr --tail 30 2>&1 | grep -E 'Starting Jellyseerr version|Server ready' || true
