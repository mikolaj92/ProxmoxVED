#!/usr/bin/env python3
import json
import sys

# Read settings
with open('/root/arr-stack/config/jellyseerr/settings.json', 'r') as f:
    data = json.load(f)

# Update initialized
data['public']['initialized'] = True

# Update Jellyfin connection
data['jellyfin'] = {
    "name": "Jellyfin",
    "ip": "192.168.11.66",
    "port": 8096,
    "useSsl": False,
    "urlBase": "",
    "externalHostname": "",
    "jellyfinForgotPasswordUrl": "",
    "libraries": [],
    "serverId": "",
    "apiKey": ""
}

# Add Sonarr connection
data['sonarr'] = [{
    "id": 1,
    "name": "Sonarr",
    "hostname": "192.168.11.66",
    "port": 8989,
    "apiKey": "0375672f0f64474c8843b922d0ab595e",
    "useSsl": False,
    "baseUrl": "/",
    "active": True,
    "is4k": False,
    "isDefault": True
}]

# Add Radarr connection
data['radarr'] = [{
    "id": 1,
    "name": "Radarr",
    "hostname": "192.168.11.66",
    "port": 7878,
    "apiKey": "e2166ae2a7284752a3d6b95423485f42",
    "useSsl": False,
    "baseUrl": "/",
    "active": True,
    "is4k": False,
    "isDefault": True
}]

# Write settings
with open('/root/arr-stack/config/jellyseerr/settings.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Settings updated successfully!")
print("\nJellyfin:")
print(f"  - URL: http://192.168.11.66:8096")
print("\nSonarr:")
print(f"  - ID: 1")
print(f"  - URL: http://192.168.11.66:8989")
print(f"  - API Key: 0375672f0f64474c8843b922d0ab595e")
print("\nRadarr:")
print(f"  - ID: 1")
print(f"  - URL: http://192.168.11.66:7878")
print(f"  - API Key: e2166ae2a7284752a3d6b95423485f42")
print("\nInitialized: True")
