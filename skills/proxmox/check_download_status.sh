#!/usr/bin/env python3
import json, urllib.request, base64, time

print("== Breaking Bad Download Status ==\n")

# Check Sonarr queue
print("=== Sonarr Queue ===")
try:
    q = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e"))
    print(f"Total records: {q.get('totalRecords')}")
    for r in q.get('records',[])[:5]:
        series = r.get('series', {})
        ep = r.get('episode', {})
        print(f"  - {series.get('title')} S{ep.get('seasonNumber')}E{ep.get('episodeNumber')}: {r.get('status')}")
        print(f"    Size: {r.get('size')/(1024*1024):.1f} MB | indexer: {r.get('indexer')}")
        print(f"    Timeleft: {r.get('timeleft', 'N/A')}")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== Transmission Torrents ===")
try:
    auth = base64.b64encode(b'transmission:Test123').decode('ascii')
    req1 = urllib.request.Request('http://192.168.11.66:9091/transmission/rpc', headers={'Authorization': f'Basic {auth}'})
    try:
        urllib.request.urlopen(req1)
    except urllib.error.HTTPError as e:
        if e.code == 409:
            session_id = e.headers.get('X-Transmission-Session-Id')
            if session_id:
                cmd = json.dumps({'method':'torrent-get','arguments':{'fields':['id','name','status','percentDone','rateDownload','totalSize','downloadedEver','eta']}}).encode('utf-8')
                req2 = urllib.request.Request('http://192.168.11.66:9091/transmission/rpc', data=cmd, headers={'Authorization': f'Basic {auth}', 'X-Transmission-Session-Id': session_id, 'Content-Type':'application/json'})
                with urllib.request.urlopen(req2) as r:
                    result = json.load(r)
                    torrents = result.get('arguments',{}).get('torrents',[])
                    print(f"Total torrents: {len(torrents)}")
                    for t in torrents:
                        status_name = ['stopped', 'check pending', 'checking', 'download pending', 'downloading', 'seed pending', 'seeding'][t.get('status')] if t.get('status') < 7 else 'unknown'
                        print(f"  - {t.get('name')[:70]}")
                        print(f"    Status: {status_name}")
                        print(f"    Progress: {t.get('percentDone')*100:.1f}% ({t.get('downloadedEver')/(1024*1024):.1f} MB / {t.get('totalSize')/(1024*1024):.1f} MB)")
                        print(f"    Rate: {t.get('rateDownload')/1024:.1f} KB/s | ETA: {t.get('eta')}s")
except Exception as e:
    print(f"ERROR: {e}")

print("\n=== Media Files ===")
import os
for path in ['/root/arr-stack/media/downloads/complete', '/root/arr-stack/media/tv', '/root/arr-stack/media/movies']:
    try:
        files = os.listdir(path)
        if files:
            print(f"{path}: {len(files)} items")
            for f in files[:5]:
                print(f"  - {f}")
        else:
            print(f"{path}: empty")
    except Exception as e:
        print(f"{path}: ERROR - {e}")
