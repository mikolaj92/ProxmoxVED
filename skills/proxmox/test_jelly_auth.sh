#!/usr/bin/env bash
set -euo pipefail
curl -i -s -X POST http://localhost:5055/api/v1/auth/local \
  -H 'Content-Type: application/json' \
  --data-binary '{"email":"admin@arr.local","password":"arradmin123"}' \
| head -40
