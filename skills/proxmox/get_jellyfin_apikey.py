#!/usr/bin/env python3
import json

# Read Jellyfin settings
with open('/root/arr-stack/config/jellyfin/config/config.xml', 'r') as f:
    import xml.etree.ElementTree as ET
    tree = ET.parse(f)
    root = tree.getroot()

# Find API key in config
for elem in root.iter():
    if 'ApiKey' in elem.tag or elem.text and len(elem.text) > 20 and elem.text.isalnum():
        print(f"Found potential API key: {elem.tag} = {elem.text}")

# Generate new API key if not found
print("\nGenerating new API key in Jellyfin...")
import subprocess
result = subprocess.run(['docker', 'exec', 'jellyfin', '/usr/lib/jellyfin-web/generate_api_key.sh'], capture_output=True, text=True)
if result.returncode == 0:
    print(f"New API Key: {result.stdout.strip()}")
else:
    # Alternative: use jellyfin API
    import requests
    import time
    
    # Check if jellyfin is running
    try:
        response = requests.get('http://localhost:8096/health', timeout=5)
        print("Jellyfin is running")
    except:
        print("Jellyfin not accessible")
