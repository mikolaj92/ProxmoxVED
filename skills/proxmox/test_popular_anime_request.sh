#!/usr/bin/env bash
set -euo pipefail

echo "== Cleanup old requests =="
sqlite3 /root/arr-stack/config/jellyseerr/db/db.sqlite3 "delete from season_request where requestId in (select id from media_request); delete from media_request;" || true
docker restart jellyseerr >/dev/null
sleep 6

echo "== Request Cyberpunk: Edgerunners S1 (tmdb 94555) =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

code=$(curl -s -o /tmp/jelly_anime.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":94555,"seasons":[1],"is4k":false}')
echo "HTTP $code"
head -c 300 /tmp/jelly_anime.out; echo

sleep 3

echo
echo "== Trigger Sonarr search for Cyberpunk S1 =="
# Get series ID from Sonarr
SERIES_ID=$(python3 -c "
import json, urllib.request, sys
s = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/series/lookup?term=402868&apikey=0375672f0f64474c8843b922d0ab595e'))
if s:
    print(s[0].get('id'))
")
echo "Series ID: $SERIES_ID"

if [ -n "$SERIES_ID" ]; then
  # Trigger season search
  curl -s -X POST "http://192.168.11.66:8989/api/v3/command?apikey=0375672f0f64474c8843b922d0ab595e" \
    -H 'Content-Type: application/json' \
    -d "{\"name\":\"SeasonSearch\",\"seriesId\":$SERIES_ID,\"seasonNumber\":1}" | head -c 200; echo
fi

sleep 5

echo
echo "== Check Sonarr queue =="
python3 -c "
import json, urllib.request
q = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e'))
print(f'totalRecords: {q.get(\"totalRecords\")}')
for r in q.get('records',[])[:10]:
    print(f'  - {r.get(\"series\",{}).get(\"title\")} S{r.get(\"episode\",{}).get(\"seasonNumber\")}E{r.get(\"episode\",{}).get(\"episodeNumber\")}: {r.get(\"status\")} | size: {r.get(\"size\")} bytes')
" 2>/dev/null

sleep 3

echo
echo "== Check Transmission =="
SESSION_ID=$(curl -s -i "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" | grep -i 'X-Transmission-Session-Id:' | cut -d' ' -f2 | tr -d '\r')
if [ -n "$SESSION_ID" ]; then
  curl -s -H "X-Transmission-Session-Id: $SESSION_ID" "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" \
    -d '{"method":"torrent-get","arguments":{"fields":["id","name","status","percentDone","rateDownload","totalSize"]}}' \
    | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f'result: {d.get(\"result\")}')
for t in d.get('arguments',{}).get('torrents',[]):
    print(f'  - {t.get(\"name\")}: status={t.get(\"status\")}, {t.get(\"percentDone\")*100:.1f}%, {t.get(\"totalSize\")/(1024*1024):.1f} MB')
" 2>/dev/null
fi
