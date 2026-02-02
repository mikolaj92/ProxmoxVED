#!/usr/bin/env bash
set -euo pipefail

echo "== Sonarr: check download client =="
curl -s "http://192.168.11.66:8989/api/v3/downloadclient?apikey=0375672f0f64474c8843b922d0ab595e" | jq '.[] | {name: .name, enabled: .enable, protocol: .protocol}' 2>/dev/null || curl -s "http://192.168.11.66:8989/api/v3/downloadclient?apikey=0375672f0f64474c8843b922d0ab595e" | head -c 500; echo

echo
echo "== Sonarr: check Breaking Bad details =="
SERIES_ID=$(curl -s "http://192.168.11.66:8989/api/v3/series/lookup?term=81189&apikey=0375672f0f64474c8843b922d0ab595e" | jq -r '.[0].id' 2>/dev/null)
echo "TVDB 81189 Sonarr ID: $SERIES_ID"

if [ -n "$SERIES_ID" ] && [ "$SERIES_ID" != "null" ]; then
  curl -s "http://192.168.11.66:8989/api/v3/series/$SERIES_ID?apikey=0375672f0f64474c8843b922d0ab595e" | jq '{title: .title, monitored: .monitored, path: .path, seasons: [.seasons[] | {seasonNumber: .seasonNumber, monitored: .monitored}]}' 2>/dev/null || echo "series details failed"
fi

echo
echo "== Transmission: check session (get X-Transmission-Session-Id) =="
SESSION_ID=$(curl -s -i "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" | grep -i 'X-Transmission-Session-Id:' | cut -d' ' -f2 | tr -d '\r')
echo "Session ID: $SESSION_ID"

if [ -n "$SESSION_ID" ]; then
  echo
  echo "== Transmission: torrent list =="
  curl -s -H "X-Transmission-Session-Id: $SESSION_ID" "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" -d '{"method":"torrent-get","arguments":{"fields":["id","name","status","percentDone","rateDownload"]}}' | jq '.result, .arguments.torrents[] | {name, status, percentDone, rateDownload}' 2>/dev/null || echo "torrent list failed"
fi

echo
echo "== Media files: check /root/arr-stack/media/ =="
ls -la /root/arr-stack/media/downloads/ 2>/dev/null | head -20 || echo "downloads dir not found"
ls -la /root/arr-stack/media/tv/ 2>/dev/null | head -20 || echo "tv dir not found"
