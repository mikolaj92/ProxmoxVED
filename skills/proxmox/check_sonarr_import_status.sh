#!/usr/bin/env python3
import json, urllib.request, time, os

print("=== Sonarr Import Status ===")

# Check Breaking Bad series
try:
    s = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/series/3?apikey=0375672f0f64474c8843b922d0ab595e"))
    print(f"Series: {s.get('title')}")
    print(f"Path: {s.get('path')}")
    print(f"Monitored: {s.get('monitored')}")

    # Get season 1 statistics
    for sn in s.get('seasons', []):
        if sn.get('seasonNumber') == 1:
            stats = sn.get('statistics', {})
            print(f"\nSeason 1:")
            print(f"  EpisodeFileCount: {stats.get('episodeFileCount')} / {stats.get('totalEpisodeCount')}")
            print(f"  SizeOnDisk: {stats.get('sizeOnDisk')/(1024*1024*1024):.2f} GB")
            print(f"  PercentOfEpisodes: {stats.get('percentOfEpisodes'):.1f}%")

    # Get episodes
    eps = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/episode?seriesId=3&seasonNumber=1&apikey=0375672f0f64474c8843b922d0ab595e"))
    print(f"\nEpisodes with files:")
    for ep in eps:
        if ep.get('hasFile'):
            print(f"  S{ep.get('seasonNumber')}E{ep.get('episodeNumber')}: {ep.get('hasFile')}")

except Exception as e:
    print(f"ERROR: {e}")

print("\n=== Check TV folder ===")
import os
tv_path = "/root/arr-stack/media/tv"
try:
    items = os.listdir(tv_path)
    print(f"TV folder items: {len(items)}")
    for item in items:
        path = os.path.join(tv_path, item)
        if os.path.isdir(path):
            files = os.listdir(path)
            print(f"  - {item}/ ({len(files)} files)")
            # Show first few files
            for f in sorted(files)[:3]:
                file_path = os.path.join(path, f)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)/(1024*1024)
                    print(f"      {f} ({size:.1f} MB)")
        else:
            print(f"  - {item}")
except Exception as e:
    print(f"ERROR: {e}")
