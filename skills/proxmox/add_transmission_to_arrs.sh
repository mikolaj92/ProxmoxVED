#!/usr/bin/env bash
set -euo pipefail
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"
TRAN_USER="transmission"
TRAN_PASS="Test123"

add_client() {
  local base="$1" key="$2" name="$3"
  echo "== $name: add Transmission download client =="
  # If already exists, skip
  if curl -s "$base/api/v3/downloadclient?apiKey=$key" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(any((x.get("implementation") or "").lower().startswith("transmission") for x in a))' | grep -q True; then
    echo "already present"
    return 0
  fi
  payload=$(cat <<JSON
{
  "enable": true,
  "protocol": "torrent",
  "priority": 1,
  "removeCompletedDownloads": true,
  "removeFailedDownloads": true,
  "name": "Transmission",
  "fields": [
    {"name":"host","value":"192.168.11.66"},
    {"name":"port","value":9091},
    {"name":"useSsl","value":false},
    {"name":"urlBase","value":"/transmission/"},
    {"name":"username","value":"$TRAN_USER"},
    {"name":"password","value":"$TRAN_PASS"},
    {"name":"musicCategory","value":""},
    {"name":"tvCategory","value":""},
    {"name":"movieCategory","value":""},
    {"name":"recentTvPriority","value":0},
    {"name":"olderTvPriority","value":0},
    {"name":"addPaused","value":false}
  ],
  "implementation": "Transmission",
  "configContract": "TransmissionSettings",
  "tags": []
}
JSON
)
  curl -s -X POST "$base/api/v3/downloadclient?apiKey=$key" \
    -H 'Content-Type: application/json' \
    --data-binary "$payload" > /tmp/${name}_dlclient.json
  head -c 240 /tmp/${name}_dlclient.json; echo
}

add_client "http://localhost:8989" "$SONARR_KEY" "sonarr"
add_client "http://localhost:7878" "$RADARR_KEY" "radarr"

# show counts
for name in sonarr radarr; do
  if [ "$name" = sonarr ]; then base=http://localhost:8989; key=$SONARR_KEY; else base=http://localhost:7878; key=$RADARR_KEY; fi
  echo "== $name download clients =="
  curl -s "$base/api/v3/downloadclient?apiKey=$key" | python3 -c 'import sys,json; a=json.load(sys.stdin); print([(x.get("id"),x.get("name"),x.get("implementation"),x.get("enable")) for x in a])'
done
