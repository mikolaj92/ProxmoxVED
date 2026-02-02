#!/usr/bin/env bash
set -euo pipefail

echo "== Sonarr: Breaking Bad monitored status =="
SERIES_ID=$(curl -s "http://192.168.11.66:8989/api/v3/series/lookup?term=81189&apikey=0375672f0f64474c8843b922d0ab595e" | jq -r '.[0].id')
if [ -n "$SERIES_ID" ] && [ "$SERIES_ID" != "null" ]; then
  echo "Sonarr series ID: $SERIES_ID"
  curl -s "http://192.168.11.66:8989/api/v3/series/$SERIES_ID?apikey=0375672f0f64474c8843b922d0ab595e" | jq '{title: .title, monitored: .monitored, path: .path, addOptions: .addOptions}'
fi

echo
echo "== Sonarr: queue (is it searching?) =="
QUEUE=$(curl -s "http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e")
echo "$QUEUE" | jq -r '{totalRecords: .totalRecords, pageSize: .pageSize}' 2>/dev/null || echo "queue failed"

echo
echo "== Prowlarr: indexers status =="
curl -s "http://192.168.11.66:9696/api/v1/indexer?apikey=8c6dca6adf3644ba9a7981b736ef636f" | jq '.[] | {name: .name, enabled: .enable}' 2>/dev/null || echo "indexers failed"

echo
echo "== Prowlarr: check if Sonarr is synced =="
curl -s "http://192.168.11.66:9696/api/v1/applications?apikey=8c6dca6adf3644ba9a7981b736ef636f" | jq '.[] | {name: .name, syncLevel: .syncLevel, indexerCount: .indexerCount}' 2>/dev/null || echo "applications failed"
