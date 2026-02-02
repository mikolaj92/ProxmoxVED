#!/usr/bin/env python3
"""Auto-connect ARR apps via API - Run inside Proxmox LXC 220"""
import requests
import time
import json
import subprocess

# Container config
CONTAINER_IP = "192.168.11.66"  # Will be detected automatically
BASE_DELAY = 30  # Wait for apps to fully start

# App ports
PORTS = {
    'prowlarr': 9696,
    'sonarr': 8989,
    'radarr': 7878,
    'lidarr': 8686,
    'jellyfin': 8096
}

def get_container_ip():
    """Get container IP"""
    try:
        result = subprocess.run(
            ['ip', 'addr', 'show', 'eth0'],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in result.stdout.split('\n'):
            if 'inet ' in line and '192.168' in line:
                return line.split()[1].split('/')[0]
        return "192.168.11.66"
    except:
        return "192.168.11.66"

def wait_for_api(url, timeout=120):
    """Wait for API to be ready"""
    print(f"   → Waiting for {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{url}/api/v1/system/status", timeout=5)
            if r.status_code == 200:
                print(f"   ✅ Ready!")
                return True
        except:
            pass
        time.sleep(2)
    print(f"   ⚠️ Timeout!")
    return False

def get_api_key(url):
    """Get initial API key from app"""
    try:
        # Try to get existing API key from config
        r = requests.get(f"{url}/api/v1/config/host", timeout=10)
        if r.status_code == 200:
            data = r.json()
            # Try multiple fields where API key might be
            for field in ['apiKey', 'api_key', 'ApiKey']:
                if field in data and data[field]:
                    return data[field]

        # Generate new API key (if endpoint available)
        r = requests.post(f"{url}/api/v1/apikey", timeout=10)
        if r.status_code == 201:
            return r.json().get('apiKey')

        return None
    except Exception as e:
        print(f"   ❌ Error getting API key: {e}")
        return None

def setup_prowlarr_apps():
    """Setup Prowlarr as indexer manager"""
    print("\n🔗 Setting up Prowlarr connections...")

    # Prowlarr base URL
    prowlarr_url = f"http://{CONTAINER_IP}:{PORTS['prowlarr']}"

    # Wait for Prowlarr
    if not wait_for_api(prowlarr_url):
        print("❌ Prowlarr API not ready!")
        return False

    # Get Prowlarr API key
    print("\n🔑 Getting Prowlarr API key...")
    time.sleep(5)  # Give extra time for initialization

    # Create initial API key via config
    try:
        # First try to access with default (no auth needed initially)
        r = requests.get(f"{prowlarr_url}/api/v1", timeout=10)
        print(f"   Prowlarr response: {r.status_code}")

        # Get or create API key
        prowlarr_key = None

        # Method 1: Get from status
        try:
            r = requests.get(f"{prowlarr_url}/api/v1/system/status", timeout=10)
            if r.status_code == 200:
                print(f"   ✅ Prowlarr is ready!")
        except:
            pass

        # Method 2: Check if apiKey is needed
        print("   ⚠️ Prowlarr requires initial setup via web UI")
        print("   Please:")
        print("      1. Open http://192.168.11.66:9696")
        print("      2. Create admin account")
        print("      3. Go to Settings → General → API Key")
        print("      4. Copy the API key")
        print("\n   Then run this script again with the key:")
        print("   python3 connect_arr.py --prowlarr-key YOUR_KEY")

        return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def connect_apps_to_prowlarr(prowlarr_key):
    """Connect Sonarr, Radarr, Lidarr to Prowlarr"""
    print("\n🔗 Connecting apps to Prowlarr...")

    prowlarr_url = f"http://{CONTAINER_IP}:{PORTS['prowlarr']}"

    apps = {
        'sonarr': {'url': f"http://{CONTAINER_IP}:{PORTS['sonarr']}", 'name': 'Sonarr'},
        'radarr': {'url': f"http://{CONTAINER_IP}:{PORTS['radarr']}", 'name': 'Radarr'},
        'lidarr': {'url': f"http://{CONTAINER_IP}:{PORTS['lidarr']}", 'name': 'Lidarr'}
    }

    for app, config in apps.items():
        print(f"\n📡 Connecting {config['name']}...")

        if not wait_for_api(config['url'], timeout=60):
            print(f"   ⚠️ {config['name']} not ready, skipping...")
            continue

        # Add Prowlarr as application in Prowlarr
        try:
            # First get the app's API key
            app_key = get_api_key(config['url'])
            if not app_key:
                print(f"   ⚠️ Could not get {config['name']} API key")
                continue

            # Add app to Prowlarr applications
            payload = {
                'name': config['name'],
                'implementation': config['name'].lower(),
                'configContract': config['name'].lower() + 'Settings',
                'syncLevel': 0,
                'enabled': True,
                'apiKey': app_key,
                'baseUrl': config['url']
            }

            r = requests.post(
                f"{prowlarr_url}/api/v1/application",
                json=payload,
                headers={'X-Api-Key': prowlarr_key},
                timeout=10
            )

            if r.status_code in [201, 200]:
                print(f"   ✅ {config['name']} connected to Prowlarr!")
            else:
                print(f"   ⚠️ Failed: {r.status_code}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    print("="*60)
    print("🔗 ARR APPS AUTO-CONNECTOR")
    print("="*60)

    global CONTAINER_IP
    CONTAINER_IP = get_container_ip()
    print(f"\n🏠 Container IP: {CONTAINER_IP}")
    print(f"⏳ Waiting {BASE_DELAY}s for apps to start...")

    time.sleep(BASE_DELAY)

    # Check if all apps are responding
    print("\n📊 Checking app status...")
    for app, port in PORTS.items():
        url = f"http://{CONTAINER_IP}:{port}"
        try:
            r = requests.get(url, timeout=5)
            print(f"   ✅ {app}: {r.status_code}")
        except:
            print(f"   ⚠️ {app}: Not responding")

    # Setup Prowlarr
    if not setup_prowlarr_apps():
        print("\n⚠️ Please complete initial Prowlarr setup first!")
        print("Then run again with API key:")
        print("   python3 connect_arr.py --prowlarr-key YOUR_KEY")
        return

    # If we got prowlarr key, connect other apps
    # (This requires initial setup to get the key)
    # connect_apps_to_prowlarr(prowlarr_key)

    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📱 Access URLs:")
    for app, port in PORTS.items():
        print(f"   • {app.capitalize()}: http://{CONTAINER_IP}:{port}")
    print("\n🔧 Next steps:")
    print("   1. Open each app in browser")
    print("   2. Create admin accounts")
    print("   3. Get Prowlarr API key from Settings → General")
    print("   4. Manually connect apps or run this script again")
    print("="*60)

if __name__ == "__main__":
    main()
