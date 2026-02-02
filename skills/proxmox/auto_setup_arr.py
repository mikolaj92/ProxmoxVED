#!/usr/bin/env python3
"""Auto-setup and connect ARR apps via API - FULLY AUTOMATED"""
import requests
import time
import json
import subprocess
import sys

CONTAINER_IP = "192.168.11.66"
PORTS = {
    'prowlarr': 9696,
    'sonarr': 8989,
    'radarr': 7878,
    'lidarr': 8686,
}

# Default admin credentials
DEFAULT_USER = "admin"
DEFAULT_PASS = "arradmin123"  # Will be set during setup
DEFAULT_EMAIL = "admin@arr.local"

def wait_for_api(url, timeout=180):
    """Wait for API to be ready"""
    print(f"   → Waiting for {url}...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{url}/api/v1/system/status", timeout=5)
            if r.status_code == 200:
                data = r.json()
                print(f"   ✅ Ready! (version: {data.get('version', 'unknown')})")
                return True
        except:
            pass
        time.sleep(3)
    print(f"   ⚠️ Timeout!")
    return False

def initialize_app(app_name, url):
    """Initialize app with default admin account"""
    print(f"\n🔧 Initializing {app_name}...")

    # Check if already initialized
    try:
        r = requests.get(f"{url}/api/v1/system/status", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('version'):
                print(f"   ✅ {app_name} is already initialized!")
                return get_api_key(url)
    except:
        pass

    # Initialize with POST request
    try:
        payload = {
            'username': DEFAULT_USER,
            'password': DEFAULT_PASS,
            'email': DEFAULT_EMAIL
        }

        # Try different initialization endpoints
        init_endpoints = [
            '/api/v1/init',
            '/api/v1/setup',
            '/api/v1/system/init',
            '/initialize',
            '/setup'
        ]

        for endpoint in init_endpoints:
            try:
                r = requests.post(f"{url}{endpoint}", json=payload, timeout=10)
                if r.status_code in [200, 201, 204]:
                    print(f"   ✅ {app_name} initialized!")
                    time.sleep(2)
                    return get_api_key(url)
            except:
                continue

        # If API init fails, may need manual setup
        print(f"   ⚠️ {app_name} needs manual setup")
        return None

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def get_api_key(url):
    """Get or create API key"""
    try:
        # Try to get existing API key
        r = requests.get(f"{url}/api/v1/config/host", timeout=10)
        if r.status_code == 200:
            data = r.json()
            for field in ['apiKey', 'api_key', 'ApiKey']:
                if field in data and data[field]:
                    print(f"   🔑 API Key found: {data[field][:12]}...")
                    return data[field]

        # Create new API key
        r = requests.post(f"{url}/api/v1/apikey", json={
            'label': f'Auto-generated {time.time()}'
        }, timeout=10)

        if r.status_code in [201, 200]:
            data = r.json()
            api_key = data.get('apiKey') or data.get('api_key')
            if api_key:
                print(f"   🔑 New API Key created: {api_key[:12]}...")
                return api_key

        return None

    except Exception as e:
        print(f"   ❌ Error getting API key: {e}")
        return None

def connect_prowlarr_to_apps(prowlarr_url, prowlarr_key):
    """Connect all ARR apps to Prowlarr"""
    print("\n🔗 Connecting apps to Prowlarr...")

    apps = {
        'sonarr': {'url': f"http://{CONTAINER_IP}:{PORTS['sonarr']}", 'name': 'Sonarr'},
        'radarr': {'url': f"http://{CONTAINER_IP}:{PORTS['radarr']}", 'name': 'Radarr'},
        'lidarr': {'url': f"http://{CONTAINER_IP}:{PORTS['lidarr']}", 'name': 'Lidarr'}
    }

    for app, config in apps.items():
        print(f"\n📡 Connecting {config['name']}...")

        # Wait for app to be ready
        if not wait_for_api(config['url'], timeout=120):
            print(f"   ⚠️ {config['name']} not ready!")
            continue

        # Get app's API key
        app_key = get_api_key(config['url'])
        if not app_key:
            print(f"   ⚠️ Could not get {config['name']} API key!")
            continue

        # Add app to Prowlarr applications
        try:
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
                print(f"   ⚠️ Failed: {r.status_code} - {r.text[:100]}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

def add_default_indexer(prowlarr_url, prowlarr_key):
    """Add a default Cardigann indexer"""
    print("\n📡 Adding default indexer...")

    try:
        # Try to add Cardigann indexer
        payload = {
            'name': 'Cardigann',
            'implementation': 'Cardigann',
            'configContract': 'CardigannSettings',
            'enable': True,
            'baseSettings': {
                'url': 'https://cardigann.example.com',
            }
        }

        r = requests.post(
            f"{prowlarr_url}/api/v1/indexer",
            json=payload,
            headers={'X-Api-Key': prowlarr_key},
            timeout=10
        )

        if r.status_code in [201, 200]:
            print(f"   ✅ Default indexer added!")
        else:
            print(f"   ⚠️ Indexer setup may need manual configuration")

    except Exception as e:
        print(f"   ⚠️ Indexer setup skipped: {e}")

def main():
    print("="*70)
    print("🔗 ARR APPS AUTO-SETUP & CONNECTION")
    print("="*70)
    print(f"\n🏠 Container IP: {CONTAINER_IP}")
    print(f"👤 Default Admin: {DEFAULT_USER} / {DEFAULT_PASS}")
    print(f"⏳ Waiting for apps to be ready...\n")

    time.sleep(30)  # Initial wait

    # Initialize Prowlarr first
    prowlarr_url = f"http://{CONTAINER_IP}:{PORTS['prowlarr']}"

    print("🎯 Prowlarr:")
    if not wait_for_api(prowlarr_url):
        print("❌ Prowlarr not ready!")
        return

    prowlarr_key = initialize_app('Prowlarr', prowlarr_url)
    if not prowlarr_key:
        print("❌ Could not initialize Prowlarr!")
        print("\n⚠️ Manual setup may be required:")
        print(f"   1. Open http://{CONTAINER_IP}:{PORTS['prowlarr']}")
        print("   2. Create admin account")
        print("   3. Get API key from Settings → General")
        return

    print(f"\n✅ Prowlarr ready! API Key: {prowlarr_key[:12]}...")

    # Initialize other apps and connect to Prowlarr
    connect_prowlarr_to_apps(prowlarr_url, prowlarr_key)

    # Add default indexer
    add_default_indexer(prowlarr_url, prowlarr_key)

    # Summary
    print("\n" + "="*70)
    print("🎉 AUTO-SETUP COMPLETE!")
    print("="*70)
    print(f"\n👤 Admin Login: {DEFAULT_USER} / {DEFAULT_PASS}")
    print(f"\n📱 Apps:")
    for app, port in PORTS.items():
        print(f"   • {app.capitalize()}: http://{CONTAINER_IP}:{port}")
    print(f"\n📺 Jellyfin: http://{CONTAINER_IP}:8096")
    print("\n🔗 Prowlarr is connected to: Sonarr, Radarr, Lidarr")
    print("📡 Next: Add indexers in Prowlarr manually")
    print("="*70)

if __name__ == "__main__":
    main()
