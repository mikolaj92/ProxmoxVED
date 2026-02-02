#!/usr/bin/env bash
set -euo pipefail
NEWPASS="Test123"

# stop/remove existing
if docker ps -a --format '{{.Names}}' | grep -q '^transmission$'; then
  docker stop transmission >/dev/null || true
  docker rm transmission >/dev/null || true
fi

# run with same binds and host network
cd /root/arr-stack

docker run -d \
  --name transmission \
  --network host \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Warsaw \
  -e USER=transmission \
  -e PASS="$NEWPASS" \
  -v /root/arr-stack/config/transmission:/config \
  -v /root/arr-stack/media/downloads:/downloads \
  -v /root/arr-stack/media/downloads/incomplete:/incomplete \
  --restart unless-stopped \
  lscr.io/linuxserver/transmission:latest >/dev/null

echo "recreated transmission"
