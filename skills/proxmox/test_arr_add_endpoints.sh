#!/usr/bin/env bash
set -euo pipefail
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
SONARR="http://localhost:8989"
RADARR="http://localhost:7878"

echo "== Radarr: test POST /api/v3/movie =="
code=$(curl -s -o /tmp/radarr_add.out -w "%{http_code}" \
  -X POST "$RADARR/api/v3/movie" \
  -H "X-Api-Key: $RADARR_KEY" \
  -H "Content-Type: application/json" \
  --data-binary '{"title":"_JELLYSEERR_TEST_DO_NOT_USE_","qualityProfileId":1,"titleSlug":"jellyseerr-test-do-not-use","tmdbId":1,"year":2000,"rootFolderPath":"/movies","monitored":false,"addOptions":{"searchForMovie":false}}')
echo "HTTP $code"
head -200 /tmp/radarr_add.out || true

echo

echo "== Sonarr: lookup + test POST /api/v3/series =="
# Lookup by tvdb
curl -s "$SONARR/api/v3/series/lookup?term=tvdb:81797&apiKey=$SONARR_KEY" | python3 -c 'import sys,json; d=json.load(sys.stdin); print("lookup_count", len(d));
if d: print({k:d[0].get(k) for k in ["title","tvdbId","year","id"]}); print("seasons", d[0].get("seasons") and len(d[0]["seasons"]) )'

echo "-- Try add series One Piece (tvdb 81797) monitored false, seasons all false"
code=$(curl -s -o /tmp/sonarr_add.out -w "%{http_code}" \
  -X POST "$SONARR/api/v3/series" \
  -H "X-Api-Key: $SONARR_KEY" \
  -H "Content-Type: application/json" \
  --data-binary '{"tvdbId":81797,"title":"One Piece","qualityProfileId":1,"languageProfileId":1,"rootFolderPath":"/tv","seasonFolder":false,"monitored":false,"seriesType":"anime","addOptions":{"searchForMissingEpisodes":false}}')
echo "HTTP $code"
head -200 /tmp/sonarr_add.out || true
