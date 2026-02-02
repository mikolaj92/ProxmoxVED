#!/bin/bash
curl -s -X POST "http://192.168.11.66:9696/api/v1/indexer" \
  -H "X-Api-Key: 8c6dca6adf3644ba9a7981b736ef636f" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1337x",
    "implementation": "Cardigann",
    "configContract": "CardigannSettings",
    "enable": true,
    "appProfileId": 1,
    "priority": 25,
    "downloadClientId": 0,
    "fields": [
      {"order": 0, "name": "definitionFile", "value": "1337x"},
      {"order": 1, "name": "baseUrl", "value": "https://1337x.to"}
    ]
  }'
