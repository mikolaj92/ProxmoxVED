#!/usr/bin/env bash
set -euo pipefail

echo "== Trigger Sonarr search for Breaking Bad S1E1 =="
# Command: SeasonSearch (search all episodes in season)
# Breaking Bad Sonarr series ID: 3, Season 1
SERIES_ID=3
SEASON_NUMBER=1

# Trigger season search
curl -s -X POST "http://192.168.11.66:8989/api/v3/command?apikey=0375672f0f64474c8843b922d0ab595e" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"SeasonSearch\",\"seriesId\":$SERIES_ID,\"seasonNumber\":$SEASON_NUMBER}" \
  | head -c 300; echo

sleep 3

echo
echo "== Check Sonarr queue (should show search) =="
python3 -c "
import json, urllib.request
q = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e'))
print(f'totalRecords: {q.get(\"totalRecords\")}')
for r in q.get('records',[])[:5]:
    print(f'  - {r.get(\"series\",{}).get(\"title\")} S{r.get(\"episode\",{}).get(\"seasonNumber\")}E{r.get(\"episode\",{}).get(\"episodeNumber\")}: {r.get(\"status\")} ({r.get(\"trackedDownloadStatus\")})')
" 2>/dev/null || echo "queue check failed"

sleep 2

echo
echo "== Check Transmission torrents =="
SESSION_ID=$(curl -s -i "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" | grep -i 'X-Transmission-Session-Id:' | cut -d' ' -f2 | tr -d '\r')
if [ -n "$SESSION_ID" ]; then
  curl -s -H "X-Transmission-Session-Id: $SESSION_ID" "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" \
    -d '{"method":"torrent-get","arguments":{"fields":["id","name","status","percentDone","rateDownload"]}}' \
    | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'result: {d.get(\"result\")}')
for t in d.get('arguments',{}).get('torrents',[]):
    print(f'  - {t.get(\"name\")}: {t.get(\"status\")}, {t.get(\"percentDone\")*100:.1f}%')
" 2>/dev/null || echo "torrent check failed"
fi
