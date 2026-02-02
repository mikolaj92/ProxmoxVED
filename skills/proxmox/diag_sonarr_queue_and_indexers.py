#!/usr/bin/env python3
import json, urllib.request, sys

def fetch(url):
    with urllib.request.urlopen(url) as r:
        return json.load(r)

print("== Sonarr: Breaking Bad series =>")
try:
    s = fetch("http://192.168.11.66:8989/api/v3/series/lookup?term=81189&apikey=0375672f0f64474c8843b922d0ab595e")
    if s:
        sid = s[0].get("id")
        print(f"Sonarr series ID: {sid}")
        if sid:
            d = fetch(f"http://192.168.11.66:8989/api/v3/series/{sid}?apikey=0375672f0f64474c8843b922d0ab595e")
            print(f"title: {d.get('title')}")
            print(f"monitored: {d.get('monitored')}")
            print(f"path: {d.get('path')}")
            print(f"addOptions: {d.get('addOptions')}")
            print(f"seasons: {len(d.get('seasons',[]))}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("== Sonarr: queue =>")
try:
    q = fetch("http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e")
    print(f"totalRecords: {q.get('totalRecords')}")
    print(f"pageSize: {q.get('pageSize')}")
    if q.get('totalRecords',0) > 0:
        for item in q.get('records',[])[:5]:
            print(f"  - {item.get('series',{}).get('title')}: {item.get('status')}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("== Prowlarr: indexers =>")
try:
    idx = fetch("http://192.168.11.66:9696/api/v1/indexer?apikey=8c6dca6adf3644ba9a7981b736ef636f")
    print(f"total indexers: {len(idx)}")
    for i in idx:
        print(f"  - {i.get('name')}: enabled={i.get('enable')}")
except Exception as e:
    print(f"ERROR: {e}")

print()
print("== Prowlarr: applications =>")
try:
    apps = fetch("http://192.168.11.66:9696/api/v1/applications?apikey=8c6dca6adf3644ba9a7981b736ef636f")
    for a in apps:
        print(f"  - {a.get('name')}: syncLevel={a.get('syncLevel')}, indexerCount={a.get('indexerCount')}")
except Exception as e:
    print(f"ERROR: {e}")
