#!/usr/bin/env bash
set -euo pipefail
html=$(curl -s http://localhost:5055/api-docs/)

echo "== lines with SwaggerUIBundle =="
echo "$html" | grep -n "SwaggerUIBundle" | head -5 || true

echo "== lines with url: =="
echo "$html" | grep -n "url:" | head -20 || true

echo "== lines with urls =="
echo "$html" | grep -n "urls" | head -20 || true
