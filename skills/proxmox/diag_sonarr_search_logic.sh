#!/usr/bin/env python3
import json, urllib.request, sys, time

print("== Sonarr: Why is Breaking Bad NOT downloading? ==")

# Get Breaking Bad series details
s = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/series/3?apikey=0375672f0f64474c8843b922d0ab595e"))
print(f"title: {s.get('title')}")
print(f"monitored: {s.get('monitored')}")
print(f"qualityProfileId: {s.get('qualityProfileId')}")
print(f"path: {s.get('path')}")

# Get all episodes for S1
episodes = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/episode?seriesId=3&seasonNumber=1&apikey=0375672f0f64474c8843b922d0ab595e"))
print(f"\nSeason 1 episodes: {len(episodes)}")
for ep in episodes[:3]:
    print(f"  S{ep.get('seasonNumber')}E{ep.get('episodeNumber')}: monitored={ep.get('monitored')}, hasFile={ep.get('hasFile')}")

# Check if there are missing episodes
missing = [e for e in episodes if e.get('monitored') and not e.get('hasFile')]
print(f"\nMissing episodes: {len(missing)}")

if len(missing) == 0:
    print("ERROR: No missing episodes to download!")
    sys.exit(0)

print("\n== Triggering automatic search for missing episodes ==")

# Trigger RSS sync search
cmd = {
    "name": "MissingEpisodeSearch",
    "seriesId": 3,
    "filterKey": "monitored"
}

req = urllib.request.Request(
    "http://192.168.11.66:8989/api/v3/command?apikey=0375672f0f64474c8843b922d0ab595e",
    data=json.dumps(cmd).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)

with urllib.request.urlopen(req) as r:
    result = json.load(r)
    print(f"Command sent: {result.get('name')}")
    print(f"ID: {result.get('id')}")

print("\nWaiting 15 seconds for search...")
time.sleep(15)

print("\n== Check queue ==")
q = json.load(urllib.request.urlopen("http://192.168.11.66:8989/api/v3/queue?apikey=0375672f0f64474c8843b922d0ab595e"))
print(f"Queue totalRecords: {q.get('totalRecords')}")
for r in q.get('records',[])[:5]:
    print(f"  - {r.get('series',{}).get('title')} S{r.get('episode',{}).get('seasonNumber')}E{r.get('episode',{}).get('episodeNumber')}: {r.get('status')}")
