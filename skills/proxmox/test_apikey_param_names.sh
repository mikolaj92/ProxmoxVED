#!/usr/bin/env bash
set -euo pipefail

echo "== sonarr apiKey param =="
code=$(curl -s -o /tmp/a -w "%{http_code}" "http://localhost:8989/api/v3/system/status?apiKey=0375672f0f64474c8843b922d0ab595e")
echo "HTTP $code"; head -c 40 /tmp/a; echo

echo "== sonarr apikey param =="
code=$(curl -s -o /tmp/b -w "%{http_code}" "http://localhost:8989/api/v3/system/status?apikey=0375672f0f64474c8843b922d0ab595e")
echo "HTTP $code"; head -c 40 /tmp/b; echo

echo "== radarr apiKey param =="
code=$(curl -s -o /tmp/c -w "%{http_code}" "http://localhost:7878/api/v3/system/status?apiKey=e2166ae2a7284752a3d6b95423485f42")
echo "HTTP $code"; head -c 40 /tmp/c; echo

echo "== radarr apikey param =="
code=$(curl -s -o /tmp/d -w "%{http_code}" "http://localhost:7878/api/v3/system/status?apikey=e2166ae2a7284752a3d6b95423485f42")
echo "HTTP $code"; head -c 40 /tmp/d; echo
