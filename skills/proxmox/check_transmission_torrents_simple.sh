#!/usr/bin/env bash
set -euo pipefail

echo "== Get Transmission session ID =="
SESSION_ID=$(curl -s -i "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" | grep -i 'X-Transmission-Session-Id:' | cut -d' ' -f2 | tr -d '\r')
echo "Session ID: $SESSION_ID"

if [ -z "$SESSION_ID" ]; then
  echo "ERROR: Could not get Transmission session ID"
  exit 1
fi

echo
echo "== Transmission: torrent list =="
curl -s -H "X-Transmission-Session-Id: $SESSION_ID" "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" \
  -d '{"method":"torrent-get","arguments":{"fields":["id","name","status","percentDone","rateDownload"]}}' \
  | jq -r '.result, (.arguments.torrents // [] | .[] | "\(.name) - status: \(.status), done: \(.percentDone*100)%")' 2>/dev/null || echo "failed"

echo
echo "== Media directories =="
echo "Downloads:"
ls -lh /root/arr-stack/media/downloads/ 2>/dev/null || echo "empty/not found"
echo
echo "TV:"
ls -lh /root/arr-stack/media/tv/ 2>/dev/null || echo "empty/not found"
