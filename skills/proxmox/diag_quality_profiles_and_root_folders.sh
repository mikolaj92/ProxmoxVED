#!/usr/bin/env python3
import json, urllib.request, sys

print("== Sonarr: quality profiles ==")
q = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/qualityprofile?apikey=0375672f0f64474c8843b922d0ab595e"))
for p in q:
    print(f"{p.get('name')} (id={p.get('id')}):")
    if 'items' in p:
        for i in p.get('items',[])[:5]:
            print(f"  - {i.get('quality',{}).get('name')}")
    print()

print("== Sonarr: Breaking Bad details (series ID 3) ==")
s = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/series/3?apikey=0375672f0f64474c8843b922d0ab595e"))
print(f"title: {s.get('title')}")
print(f"qualityProfileId: {s.get('qualityProfileId')}")
print(f"path: {s.get('path')}")
print(f"seasons: {len(s.get('seasons',[]))}")
for sn in s.get('seasons',[]):
    print(f"  Season {sn.get('seasonNumber')}: monitored={sn.get('monitored')}, statistics={sn.get('statistics')}")
