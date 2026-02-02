#!/usr/bin/env bash
set -euo pipefail
KEY="0375672f0f64474c8843b922d0ab595e"
BASE="http://localhost:8989/api/v3/series/lookup"

for term in 'tvdb:81797' 'tvdbid:81797' 'tvdbId:81797' 'tvdb=81797'; do
  echo "term=$term"
  url="$BASE?term=$term&apiKey=$KEY"
  cnt=$(curl -s "$url" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d))')
  echo "  count=$cnt"
done
