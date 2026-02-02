#!/usr/bin/env python3
import json, urllib.request, sys, time, base64

MAGNET = "magnet:?xt=urn:btih:c9e15763f722f23e98a29decdfae341b98d53056&dn=ubuntu-22.04.3-desktop-amd64.iso&tr=udp%3A%2F%2Ftracker.ubuntu.com%3A6969&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969"

print(f"== Adding test magnet to Transmission ==")

base_url = "http://192.168.11.66:9091/transmission/rpc"
auth_header = "Basic " + base64.b64encode(b"transmission:Test123").decode("ascii")

# First request to get session ID (will get 409)
session_id = None
try:
    req = urllib.request.Request(base_url, headers={"Authorization": auth_header})
    with urllib.request.urlopen(req) as r:
        pass  # Won't reach here
except urllib.error.HTTPError as e:
    if e.code == 409:
        for line in e.headers.items():
            if line[0].lower() == 'x-transmission-session-id':
                session_id = line[1]
                break
    else:
        raise

print(f"Session ID: {session_id[:50] if session_id else 'None'}...")

# Add torrent
add_data = json.dumps({
    "method": "torrent-add",
    "arguments": {
        "filename": MAGNET,
        "download-dir": "/root/arr-stack/media/downloads/complete"
    }
}).encode('utf-8')

req = urllib.request.Request(
    base_url,
    data=add_data,
    headers={
        "Authorization": auth_header,
        "X-Transmission-Session-Id": session_id,
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req) as r:
    result = json.load(r)
    print(f"Result: {result.get('result')}")
    if result.get('arguments', {}).get('torrent-added'):
        print(f"Torrent added: {result['arguments']['torrent-added'].get('name')}")
    else:
        print(f"Full response: {json.dumps(result, indent=2)}")

print()
print("== Waiting 15 seconds for metadata to download ==")
time.sleep(15)

print()
print("== Check torrent status ==")
status_data = json.dumps({
    "method": "torrent-get",
    "arguments": {
        "fields": ["id", "name", "status", "percentDone", "rateDownload", "totalSize", "downloadDir"]
    }
}).encode('utf-8')

req2 = urllib.request.Request(
    base_url,
    data=status_data,
    headers={
        "Authorization": auth_header,
        "X-Transmission-Session-Id": session_id,
        "Content-Type": "application/json"
    }
)

with urllib.request.urlopen(req2) as r:
    result = json.load(r)
    print(f"Result: {result.get('result')}")
    for t in result.get('arguments', {}).get('torrents', []):
        print(f"  - {t.get('name')}")
        print(f"    status: {t.get('status')}")
        print(f"    done: {t.get('percentDone')*100:.1f}%")
        print(f"    rate: {t.get('rateDownload')/1024:.1f} KB/s")
        print(f"    size: {t.get('totalSize')/(1024*1024):.1f} MB")
        print(f"    dir: {t.get('downloadDir')}")
