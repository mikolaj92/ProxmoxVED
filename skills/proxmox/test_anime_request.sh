#!/usr/bin/env bash
set -euo pipefail

echo "== Cleanup old requests =="
sqlite3 /root/arr-stack/config/jellyseerr/db/db.sqlite3 "delete from season_request where requestId in (select id from media_request); delete from media_request;" || true
docker restart jellyseerr >/dev/null
sleep 6

echo
echo "== Request Cyberpunk: Edgerunners S1 (anime - should be on Nyaa) =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

code=$(curl -s -o /tmp/jelly_anime.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":94555,"seasons":[1],"is4k":false}')
echo "HTTP $code"
head -c 300 /tmp/jelly_anime.out; echo

sleep 5

echo
echo "== Check Jellyseerr logs =="
docker logs jellyseerr --tail 50 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Failed' | tail -50 || true

echo
echo "== Trigger Sonarr season search =="
python3 -c "
import json, urllib.request
s = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/series/lookup?term=402868&apikey=0375672f0f64474c8843b922d0ab595e'))
if s and len(s) > 0:
    sid = s[0].get('id')
    if sid:
        print(f'Series ID: {sid}')
        cmd = json.dumps({'name':'SeasonSearch','seriesId':sid,'seasonNumber':1}).encode('utf-8')
        req = urllib.request.Request('http://192.168.11.66:8989/api/v3/command?apikey=0375672f0f64474c8843b922d0ab595e', data=cmd, headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req) as r:
            result = json.load(r)
            print(f'Command sent: {result.get(\"name\")}')
    else:
        print('Series not found in lookup')
else:
    print('No lookup results')
"

sleep 15

echo
echo "== Check Sonarr queue =="
python3 -c "
import json, urllib.request
q = json.load(urllib.request.urlopen('http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e'))
print(f'Queue totalRecords: {q.get(\"totalRecords\")}')
for r in q.get('records',[])[:5]:
    print(f'  - {r.get(\"series\",{}).get(\"title\")} S{r.get(\"episode\",{}).get(\"seasonNumber\")}E{r.get(\"episode\",{}).get(\"episodeNumber\")}: {r.get(\"status\")} | {r.get(\"size\")/(1024*1024):.1f} MB')
"

echo
echo "== Check Transmission =="
python3 -c "
import json, urllib.request
import base64
auth = base64.b64encode(b'transmission:Test123').decode('ascii')
req1 = urllib.request.Request('http://192.168.11.66:9091/transmission/rpc', headers={'Authorization': f'Basic {auth}'})
try:
    urllib.request.urlopen(req1)
except urllib.error.HTTPError as e:
    if e.code == 409:
        session_id = e.headers.get('X-Transmission-Session-Id')
        if session_id:
            cmd = json.dumps({'method':'torrent-get','arguments':{'fields':['id','name','status','percentDone','rateDownload','totalSize']}}).encode('utf-8')
            req2 = urllib.request.Request('http://192.168.11.66:9091/transmission/rpc', data=cmd, headers={'Authorization': f'Basic {auth}', 'X-Transmission-Session-Id': session_id, 'Content-Type':'application/json'})
            with urllib.request.urlopen(req2) as r:
                result = json.load(r)
                print(f'Result: {result.get(\"result\")}')
                for t in result.get('arguments',{}).get('torrents',[]):
                    print(f'  - {t.get(\"name\")}: {t.get(\"percentDone\")*100:.1f}%, {t.get(\"totalSize\")/(1024*1024):.1f} MB')
"
