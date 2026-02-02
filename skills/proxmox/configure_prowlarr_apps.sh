#!/usr/bin/env bash
set -euo pipefail
APIKEY=$(sed -n 's:.*<ApiKey>\([^<]*\)</ApiKey>.*:\1:p' /root/arr-stack/config/prowlarr/config.xml | head -n 1)
SONARR_KEY="0375672f0f64474c8843b922d0ab595e"
RADARR_KEY="e2166ae2a7284752a3d6b95423485f42"

base="http://localhost:9696/api/v1"

# Clean existing apps (if rerun)
existing=$(curl -s "$base/applications?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print(" ".join(str(x.get("id")) for x in a if x.get("implementation") in ("Sonarr","Radarr")))')
for id in $existing; do
  curl -s -X DELETE "$base/applications/$id?apikey=$APIKEY" >/dev/null || true
done

SONARR_PAYLOAD=$(cat <<JSON
{
  "name": "Sonarr",
  "implementation": "Sonarr",
  "configContract": "SonarrSettings",
  "syncLevel": "fullSync",
  "enable": true,
  "fields": [
    {"name":"prowlarrUrl","value":"http://192.168.11.66:9696"},
    {"name":"baseUrl","value":"http://192.168.11.66:8989"},
    {"name":"apiKey","value":"$SONARR_KEY"},
    {"name":"syncCategories","value":[5000,5010,5020,5030,5040,5045,5050,5090]}
  ]
}
JSON
)

RADARR_PAYLOAD=$(cat <<JSON
{
  "name": "Radarr",
  "implementation": "Radarr",
  "configContract": "RadarrSettings",
  "syncLevel": "fullSync",
  "enable": true,
  "fields": [
    {"name":"prowlarrUrl","value":"http://192.168.11.66:9696"},
    {"name":"baseUrl","value":"http://192.168.11.66:7878"},
    {"name":"apiKey","value":"$RADARR_KEY"},
    {"name":"syncCategories","value":[2000,2010,2020,2030,2040,2045,2050,2060,2070,2080,2090]}
  ]
}
JSON
)

echo "== create Sonarr app in Prowlarr =="
curl -s -X POST "$base/applications?apikey=$APIKEY" \
  -H 'Content-Type: application/json' \
  --data-binary "$SONARR_PAYLOAD" > /tmp/prowlarr_add_sonarr.json
python3 -c 'import json; print(json.load(open("/tmp/prowlarr_add_sonarr.json"))["implementation"], "id", json.load(open("/tmp/prowlarr_add_sonarr.json")).get("id"))' 2>/dev/null || head -c 200 /tmp/prowlarr_add_sonarr.json; echo

echo "== create Radarr app in Prowlarr =="
curl -s -X POST "$base/applications?apikey=$APIKEY" \
  -H 'Content-Type: application/json' \
  --data-binary "$RADARR_PAYLOAD" > /tmp/prowlarr_add_radarr.json
python3 -c 'import json; print(json.load(open("/tmp/prowlarr_add_radarr.json"))["implementation"], "id", json.load(open("/tmp/prowlarr_add_radarr.json")).get("id"))' 2>/dev/null || head -c 200 /tmp/prowlarr_add_radarr.json; echo

echo "== list applications =="
curl -s "$base/applications?apikey=$APIKEY" | python3 -c 'import sys,json; a=json.load(sys.stdin); print("apps", len(a)); print([(x.get("id"), x.get("name"), x.get("implementation"), x.get("enable")) for x in a])'

echo "== trigger application sync command =="
curl -s -X POST "$base/command?apikey=$APIKEY" -H 'Content-Type: application/json' --data-binary '{"name":"ApplicationIndexerSync"}' | head -c 300; echo
