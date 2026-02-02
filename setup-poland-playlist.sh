#!/bin/bash
# Skrypt tworzący polską playlistę M3U z Free-TV/IPTV

cat > /tmp/poland.m3u <<'EOF'
#EXTM3U
#EXTINF:-1 tvg-id="TVP1.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/TVP1_logo.svg/640px-TVP1_logo.svg.png" group-title="Poland",TVP1
https://www.tvkaista.net/stream-forwarder/get.php?x=TVP1
#EXTINF:-1 tvg-id="TVP2.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/TVP2_logo.svg/640px-TVP2_logo.svg.png" group-title="Poland",TVP2
https://strims.top/tv/tvp2.m3u8
#EXTINF:-1 tvg-id="TVP3Warszawa.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/TVP3_%282016%29.svg/640px-TVP3_%282016%29.svg.png" group-title="Poland",TVP3 Warszawa
https://www.tvkaista.net/stream-forwarder/get.php?x=TVP3Warszawa
#EXTINF:-1 tvg-id="TVPPolonia.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/TVP_Polonia_Logo_2020.svg/640px-TVP_Polonia_Logo_2020.svg.png" group-title="Poland",TVP Polonia
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPPolonia
#EXTINF:-1 tvg-id="AlfaTVP.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Alfa_TVP_%282022%29.svg/640px-Alfa_TVP_%282022%29.svg.png" group-title="Poland",Alfa TVP
https://www.tvkaista.net/stream-forwarder/get.php?x=AlfaTVP
#EXTINF:-1 tvg-id="TVPInfo.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/TVP_Info_logo.svg/640px-TVP_Info_logo.svg.png" group-title="Poland",TVP Info
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPInfo
#EXTINF:-1 tvg-id="BelsatTV.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Belsat_%282022%29.svg/768px-Belsat_%282022%29.svg.png" group-title="Poland",Belsat
http://149.5.17.34:20041/play/a076
#EXTINF:-1 tvg-id="TVPWorld.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/TVP_World_%282021%29.svg/640px-TVP_World_%282021%29.svg.png" group-title="Poland",TVP World
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPWorld
#EXTINF:-1 tvg-id="TVPABC2.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/en/thumb/c/cb/TVP_ABC_2_%282022%29.svg/640px-TVP_ABC_2_%282022%29.svg.png" group-title="Poland",TVP ABC 2
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPABC2
#EXTINF:-1 tvg-id="TVPHistoria2.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/TVP_Historia_2_%282021%29.svg/640px-TVP_Historia_2_%282021%29.svg.png" group-title="Poland",TVP Historia 2
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPHistoria2
#EXTINF:-1 tvg-id="TVPKultura2.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/TVP_Kultura_2_%282020%29.svg/640px-TVP_Kultura_2_%282020%29.svg.png" group-title="Poland",TVP Kultura 2
https://www.tvkaista.net/stream-forwarder/get.php?x=TVPKultura2
#EXTINF:-1 tvg-id="TVRepublika.pl" tvg-logo="https://i.imgur.com/ljpK6dZ.png" group-title="Poland",TV Republika
https://redir.cache.orange.pl/jupiter/o1-cl7/ssl/live/tvrepublika/live.m3u8
#EXTINF:-1 tvg-id="4FunTV.pl" tvg-logo="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/4fun.tv_Logo_%282017%29.svg/640px-4fun.tv_Logo_%282017%29.svg.png" group-title="Poland",4fun.tv
https://stream.4fun.tv:8888/hls/4f_high/index.m3u8
EOF

# Upload to xTeVe config directory
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "pct exec 220 -- mkdir -p /root/arr-stack/config/xteve"
scp -i ~/.ssh/proxmox_auto_arr /tmp/poland.m3u root@192.168.11.199:/tmp/
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199 "mv /tmp/poland.m3u /root/arr-stack/config/xteve/"

echo "✅ Polska playlista utworzona!"
echo "Plik: /root/arr-stack/config/xteve/poland.m3u"
echo ""
echo "Kanały:"
echo "- TVP1, TVP2, TVP3 Warszawa"
echo "- TVP Polonia, TVP Info, Alfa TVP"
echo "- TVP World, TVP ABC 2"
echo "- TVP Historia 2, TVP Kultura 2"
echo "- Belsat, TV Republika"
echo "- 4fun.tv"
echo ""
echo "Teraz otwórz xTeVe i dodaj ten plik jako playlistę:"
echo "http://192.168.11.66:34400/web/"
echo "Settings → Playlist → Add File → poland.m3u"
