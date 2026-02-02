#!/bin/bash
curl -s -c /tmp/jelly-final.txt \
  -X POST http://localhost:5055/api/v1/auth/local \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@arr.local","password":"arradmin123"}' > /dev/null

echo "📺 Próbuję POST dla Jellyfin..."
curl -s -b /tmp/jelly-final.txt \
  -X POST http://localhost:5055/api/v1/settings/jellyfin \
  -H "Content-Type: application/json" \
  -d '{"ip":"192.168.11.66","port":8096,"apiKey":"61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"}' | python3 -m json.tool
