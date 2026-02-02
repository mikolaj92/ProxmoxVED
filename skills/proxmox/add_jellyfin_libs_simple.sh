#!/usr/bin/env bash
set -euo pipefail

API_KEY="61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
BASE="http://192.168.11.66:8096"

echo "== Add TV library (minimal JSON) =="
curl -s -X POST "$BASE/Library/VirtualFolders?api_key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"Name":"TV Shows","CollectionType":"tvshows","Paths":["/root/arr-stack/media/tv"]}' \
  | head -c 400; echo

echo
echo "== Add Movies library =="
curl -s -X POST "$BASE/Library/VirtualFolders?api_key=$API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"Name":"Movies","CollectionType":"movies","Paths":["/root/arr-stack/media/movies"]}' \
  | head -c 400; echo

echo
echo "== Verify =="
sleep 3
curl -s "$BASE/Library/VirtualFolders?api_key=$API_KEY" | head -c 600; echo
