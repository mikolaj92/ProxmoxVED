#!/usr/bin/env python3
import json, shutil, time
from urllib.request import Request, urlopen

def get_json(url, headers=None):
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode('utf-8'))

def main():
    settings_path = '/root/arr-stack/config/jellyseerr/settings.json'
    backup_path = f"{settings_path}.bak-{int(time.time())}"
    shutil.copy2(settings_path, backup_path)

    d = json.load(open(settings_path))

    def pick_default(arr):
        if not isinstance(arr, list) or not arr:
            return None
        for x in arr:
            if x.get('isDefault'):
                return x
        return arr[-1]

    sonarr = pick_default(d.get('sonarr', []))
    radarr = pick_default(d.get('radarr', []))

    if not sonarr or not radarr:
        raise SystemExit('Missing sonarr or radarr entries in settings.json')

    # Fetch profiles/rootfolders/tags from ARR apps
    sonarr_headers = {'X-Api-Key': sonarr['apiKey']}
    radarr_headers = {'X-Api-Key': radarr['apiKey']}

    sonarr_profiles = get_json(f"http://{sonarr['hostname']}:{sonarr['port']}/api/v3/qualityprofile", headers=sonarr_headers)
    sonarr_root = get_json(f"http://{sonarr['hostname']}:{sonarr['port']}/api/v3/rootfolder", headers=sonarr_headers)
    try:
        sonarr_tags = get_json(f"http://{sonarr['hostname']}:{sonarr['port']}/api/v3/tag", headers=sonarr_headers)
    except Exception:
        sonarr_tags = []

    radarr_profiles = get_json(f"http://{radarr['hostname']}:{radarr['port']}/api/v3/qualityprofile", headers=radarr_headers)
    radarr_root = get_json(f"http://{radarr['hostname']}:{radarr['port']}/api/v3/rootfolder", headers=radarr_headers)
    try:
        radarr_tags = get_json(f"http://{radarr['hostname']}:{radarr['port']}/api/v3/tag", headers=radarr_headers)
    except Exception:
        radarr_tags = []

    # Inject expected arrays
    sonarr['profiles'] = sonarr_profiles
    sonarr['rootFolders'] = sonarr_root
    sonarr['tags'] = sonarr_tags

    radarr['profiles'] = radarr_profiles
    radarr['rootFolders'] = radarr_root
    radarr['tags'] = radarr_tags

    # Ensure activeProfileName matches activeProfileId
    def sync_profile(server):
        pid = server.get('activeProfileId')
        name = None
        for p in server.get('profiles') or []:
            if p.get('id') == pid:
                name = p.get('name')
                break
        if name:
            server['activeProfileName'] = name

    sync_profile(sonarr)
    sync_profile(radarr)

    # Keep only one server per list to avoid weird merges
    sonarr['isDefault'] = True
    radarr['isDefault'] = True
    d['sonarr'] = [sonarr]
    d['radarr'] = [radarr]

    json.dump(d, open(settings_path, 'w'), indent=2)
    print('OK')
    print('backup:', backup_path)
    print('sonarr_profiles:', len(sonarr_profiles), 'rootFolders:', len(sonarr_root))
    print('radarr_profiles:', len(radarr_profiles), 'rootFolders:', len(radarr_root))

if __name__ == '__main__':
    main()
