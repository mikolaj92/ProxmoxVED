#!/bin/bash
# Final attempt - refresh library to scan folder
API_KEY="61e7d42062b5cae80be0a92e01465a6afe1f3be98602e4b1fa6ba24d28cbf888"
BASE="http://localhost:8096"

echo "=== Uruchamiam skan biblioteki TV Shows ==="

# Get ItemId
TV_ID=$(curl -s "$BASE/Library/VirtualFolders?api_key=$API_KEY" | python3 -c "import json,sys; libs=json.load(sys.stdin); print([l.get('ItemId') for l in libs if l.get('Name')=='TV Shows'][0])")

echo "TV ID: $TV_ID"

# Refresh library
curl -s -X POST "$BASE/Library/Refresh?api_key=$API_KEY" \
  -H "Content-Type: application/json" \
  -d "{}" \
  | head -c 200

echo
echo "Skanowanie uruchomione. Czekam 10 sekund..."
sleep 10

echo "Sprawdzam czy Breaking Bad jest wykryty..."
curl -s "$BASE/Items?api_key=$API_KEY&Recursive=true&searchTerm=Breaking%20Bad" | python3 -c "import json,sys; items=json.load(sys.stdin); print(f'Znaleziono: {items.get(\"TotalRecordCount\")}'); [print(f'  - {i.get(\"Name\")} ({i.get(\"Type\")})') for i in items.get('Items',[])]"
