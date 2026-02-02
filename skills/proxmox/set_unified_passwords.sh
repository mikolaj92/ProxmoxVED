#!/usr/bin/env bash
set -euo pipefail
NEWPASS="Test123"
export NEWPASS

echo "== Transmission: set RPC username/password in config =="
python3 - <<PY
import json, os
p='/root/arr-stack/config/transmission/settings.json'
with open(p) as f: d=json.load(f)
d['rpc-authentication-required']=True
d['rpc-username']='transmission'
d['rpc-password']=os.environ['NEWPASS']
with open(p,'w') as f: json.dump(d,f,indent=2)
print('updated', p)
PY

echo "== Jellyseerr: update admin password in sqlite (bcrypt) =="
HASH=$(docker exec -e PASS="$NEWPASS" jellyseerr node -e 'let bcrypt; try{bcrypt=require("bcryptjs")}catch(e){try{bcrypt=require("bcrypt")}catch(e2){console.error("No bcrypt module");process.exit(1)}}; const pass=process.env.PASS; (async()=>{ const h=bcrypt.hashSync?bcrypt.hashSync(pass,10):await bcrypt.hash(pass,10); console.log(h); })();')
DB=/root/arr-stack/config/jellyseerr/db/db.sqlite3
sqlite3 "$DB" "UPDATE user SET password='${HASH}' WHERE id=1;"

echo "== Jellyfin: set admin password via API (using abc no-pass user) =="
# get admin user id
ADMIN_ID=$(sqlite3 /root/arr-stack/config/jellyfin/data/data/jellyfin.db "SELECT Id FROM Users WHERE Username='admin' LIMIT 1;")
# auth as abc to get token
TOKEN=$(curl -s -X POST http://localhost:8096/Users/authenticatebyname \
  -H 'Content-Type: application/json' \
  -H 'X-Emby-Authorization: MediaBrowser Client="Setup", Device="Setup", DeviceId="setup", Version="10.0.0"' \
  --data-binary '{"Username":"abc","Pw":""}' \
| python3 -c 'import sys,json; print(json.load(sys.stdin)["AccessToken"])')

# set admin password (current might be admin123)
# Jellyfin expects JSON: {"CurrentPw":"...","NewPw":"..."}
# If CurrentPw wrong, we can set via /Users/{id}/Password with ResetPassword true is not available; so we try both empty and admin123.
for cur in "admin123" ""; do
  code=$(curl -s -o /tmp/jf_pw.out -w "%{http_code}" \
    -X POST "http://localhost:8096/Users/${ADMIN_ID}/Password" \
    -H "X-MediaBrowser-Token: ${TOKEN}" \
    -H 'Content-Type: application/json' \
    --data-binary "{\"CurrentPw\":\"${cur}\",\"NewPw\":\"${NEWPASS}\"}")
  if [ "$code" = "204" ] || [ "$code" = "200" ]; then
    echo "Jellyfin admin password updated (cur='$cur')"
    break
  fi
  echo "Jellyfin password update attempt failed (HTTP $code)"
  head -200 /tmp/jf_pw.out || true
  sleep 1
done

echo "== Restart affected containers =="
docker restart transmission >/dev/null
sleep 2
docker restart jellyseerr >/dev/null

# jellyfin doesn't need restart for password

echo "DONE"
echo "New unified password set for: Jellyseerr/Jellyfin(admin)/Transmission"
