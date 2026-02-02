#!/usr/bin/env bash
set -euo pipefail
html=$(curl -s http://localhost:5055/api-docs/)
echo "$html" | grep -i -E "(openapi|swagger).*(json|yaml)" | head -50
