#!/usr/bin/env bash
set -euo pipefail
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3

echo "== STEP 1: FULL CLEANUP - delete ALL requests =="
sqlite3 "$DB" "delete from season_request where requestId in (select id from media_request);" || true
sqlite3 "$DB" "delete from media_request;" || true

echo "Requests after cleanup:"
sqlite3 "$DB" "select count(*) as total_requests from media_request;" || true

docker restart jellyseerr >/dev/null
sleep 6

echo "Jellyseerr restarted"
echo

echo "== STEP 2: Create test request - Breaking Bad S1 =="
JELLY=http://localhost:5055
curl -s -c /tmp/jelly.cookie -X POST "$JELLY/api/v1/auth/local" -H 'Content-Type: application/json' --data-binary '{"email":"admin@arr.local","password":"Test123"}' >/dev/null

code=$(curl -s -o /tmp/jelly_test.out -w "%{http_code}" -b /tmp/jelly.cookie -X POST "$JELLY/api/v1/request" -H 'Content-Type: application/json' --data-binary '{"mediaType":"tv","mediaId":1396,"seasons":[1],"is4k":false}')
echo "HTTP $code"
head -c 300 /tmp/jelly_test.out; echo

sleep 3

echo
echo "== STEP 3: Check Jellyseerr logs =="
docker logs jellyseerr --tail 40 2>&1 | grep -E 'Sent request to Sonarr|Sonarr accepted|Failed' | tail -40 || true

echo
echo "== STEP 4: Check Sonarr series list =="
curl -s "http://192.168.11.66:8989/api/v3/series?apikey=0375672f0f64474c8843b922d0ab595e" | jq '.[] | {title: .title, year: .year, monitored: .monitored, seasons: [.seasons[] | {seasonNumber: .seasonNumber, monitored: .monitored}]}' 2>/dev/null || curl -s "http://192.168.11.66:8989/api/v3/series?apikey=0375672f0f64474c8843b922d0ab595e" | head -c 500; echo

echo
echo "== STEP 5: Check Sonarr queue =="
curl -s "http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e" | jq '.totalRecords' 2>/dev/null || echo "queue query failed"

echo
echo "== STEP 6: Check Transmission =="
curl -s "http://transmission:Test123@192.168.11.66:9091/transmission/rpc" 2>&1 | head -c 200; echo
