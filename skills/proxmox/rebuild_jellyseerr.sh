#!/usr/bin/env bash
set -euo pipefail

TS=$(date +%Y%m%d-%H%M%S)
BACK=/root/arr-stack/config/jellyseerr-backup-$TS.tgz
cd /root/arr-stack/config

tar -czf "$BACK" jellyseerr
ls -lh "$BACK"

echo "== pull image =="
docker pull fallenbagel/jellyseerr:latest

echo "== recreate container =="
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

sleep 10

echo "== logs (version/ready) =="
docker logs jellyseerr --tail 80 2>&1 | egrep -i 'Starting Jellyseerr version|Server ready' || true

echo "== test /api/v1/request =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null
curl -s -b /tmp/jelly.cookie "$JELLY/api/v1/request?take=10&skip=0" | head -c 400; echo
