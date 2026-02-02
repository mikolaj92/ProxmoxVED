#!/usr/bin/env bash
set -euo pipefail
KEY="0375672f0f64474c8843b922d0ab595e"
URL="http://192.168.11.66:8989//api/v3/series?apikey=$KEY"

echo "== POST $URL =="
code=$(curl -s -o /tmp/out -w "%{http_code}" -X POST "$URL" \
  -H 'Content-Type: application/json' \
  --data-binary '{"tvdbId":81189,"title":"Breaking Bad","qualityProfileId":1,"languageProfileId":1,"rootFolderPath":"/tv","seasonFolder":false,"monitored":true,"seriesType":"standard","seasons":[{"seasonNumber":1,"monitored":true}],"addOptions":{"searchForMissingEpisodes":false,"ignoreEpisodesWithFiles":true}}')
echo "HTTP $code"
head -200 /tmp/out || true
