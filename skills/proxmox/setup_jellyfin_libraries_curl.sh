#!/usr/bin/env bash
set -euo pipefail

API_KEY="61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
BASE="http://192.168.11.66:8096"

echo "== Add TV Shows library =="
curl -s -X POST "$BASE/Library/VirtualFolders?api_key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"Name":"TV Shows","CollectionType":"tvshows","Locations":["/root/arr-stack/media/tv"],"RefreshLibrary":true}' \
  | head -c 300; echo

echo
echo "== Add Movies library =="
curl -s -X POST "$BASE/Library/VirtualFolders?api_key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"Name":"Movies","CollectionType":"movies","Locations":["/root/arr-stack/media/movies"],"RefreshLibrary":true}' \
  | head -c 300; echo

echo
echo "== Wait 10s for scan =="
sleep 10

echo
echo "== Verify libraries =="
curl -s "$BASE/Library/VirtualFolders?api_key=$API_KEY" | head -c 500; echo

echo
echo "== Check items =="
curl -s "$BASE/Items?api_key=$API_KEY&Recursive=true&limit=10" | head -c 500; echo
