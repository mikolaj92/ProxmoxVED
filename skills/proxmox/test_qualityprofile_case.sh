#!/usr/bin/env bash
set -euo pipefail

for url in \
  "http://localhost:8989/api/v3/qualityProfile?apiKey=0375672f0f64474c8843b922d0ab595e" \
  "http://localhost:8989/api/v3/qualityprofile?apiKey=0375672f0f64474c8843b922d0ab595e" \
  "http://localhost:7878/api/v3/qualityProfile?apiKey=e2166ae2a7284752a3d6b95423485f42" \
  "http://localhost:7878/api/v3/qualityprofile?apiKey=e2166ae2a7284752a3d6b95423485f42"; do
  echo "== $url =="
  code=$(curl -s -o /tmp/out -w "%{http_code}" "$url")
  echo "HTTP $code"; head -c 1 /tmp/out | od -An -t c
  echo
  rm -f /tmp/out
done
