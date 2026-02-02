#!/usr/bin/env bash
set -euo pipefail
cd /root/arr-stack
sed -i "s/^\(\s*- PASS=\).*/\1Test123/" docker-compose.yml
# ensure docker-compose talks to local socket
export DOCKER_HOST=unix:///var/run/docker.sock

docker-compose up -d --force-recreate transmission
