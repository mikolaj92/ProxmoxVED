#!/usr/bin/env python3
import json, time, shutil
p='/root/arr-stack/config/jellyseerr/settings.json'
bak=f"{p}.bak-baseurl-{int(time.time())}"
shutil.copy2(p,bak)
d=json.load(open(p))
changed=[]
for key in ('sonarr','radarr'):
    arr=d.get(key)
    if not isinstance(arr,list):
        continue
    for s in arr:
        if s.get('baseUrl') in ('/','//'):
            s['baseUrl']=''
            changed.append((key,s.get('id')))
json.dump(d, open(p,'w'), indent=2)
print('backup',bak)
print('changed',changed)
