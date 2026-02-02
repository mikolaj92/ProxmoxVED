#!/usr/bin/env bash
set -euo pipefail
# If auth is correct, first call usually returns 409 with X-Transmission-Session-Id
curl -i -s -u transmission:Test123 -X POST http://localhost:9091/transmission/rpc -d '{"method":"session-get"}' | head -20
