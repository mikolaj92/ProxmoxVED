#!/usr/bin/env bash
set -euo pipefail
url='http://localhost:8989/api/v3/languageprofile?apiKey=0375672f0f64474c8843b922d0ab595e'
code=$(curl -s -o /tmp/lp -w "%{http_code}" "$url")
echo "HTTP $code"
head -80 /tmp/lp || true
