# Tunarr Setup - Completion Instructions

## Current Status
✅ Tunarr installed and running on port 8000
✅ Jellyfin configured as media source (Movies + TV Shows)
✅ Sample channel "Movies 24/7" created (channel #1)
⏳ Awaiting: Programming/flex configuration for channel

## URLs
- Tunarr Web UI: http://192.168.11.66:8000
- Jellyfin: http://192.168.11.70:8096
- XMLTV: http://192.168.11.66:8000/xmltv.xml

## Next Steps (Web UI)

### 1. Access Tunarr
Navigate to: http://192.168.11.66:8000

### 2. Configure Channel Programming
- Go to: Channels → Select "Movies 24/7"
- Tab: "Programming"
- Click: "Add Programming"
- Select:
  - Source: "Jellyfin Movies"
  - Type: "Flex" (random/shuffle)
  - Set start time: e.g., 00:00
- Add the programming (Tunarr will fetch movie list from Jellyfin)

### 3. Enable Channel
- Toggle channel to "On"
- Check XMLTV updates at: http://192.168.11.66:8000/xmltv.xml

### 4. Integrate with Jellyfin (Option A - HDHomeRun)
In Jellyfin (CT230):
- Dashboard → Live TV → Add TV tuner
- Select: "HDHomeRun"
- Tunarr should be auto-discovered (enabled in settings)

### 5. Integrate with Jellyfin (Option B - M3U)
After channel has programming, Tunarr generates M3U at:
- http://192.168.11.66:8000/lineups.m3u (available once programming exists)

In Jellyfin:
- Dashboard → Live TV → Add M3U Tuner
- Paste the M3U URL
- Add XMLTV: http://192.168.11.66:8000/xmltv.xml

## For Polish/American Live TV Channels
Tunarr creates channels from YOUR media library. To get actual Polish/American TV channels:
1. Get IPTV subscription (m3u playlist + Xtream Codes or URL)
2. In Tunarr: Settings → Media Sources → Add IPTV source
3. Configure channels from IPTV
4. Stream through Tunarr to Jellyfin

Alternative: Use xTeVe or similar IPTV proxy directly with Jellyfin.

## Container Details
- Container: tunarr
- Image: chrisbenincasa/tunarr:latest
- Config: /root/arr-stack/config/tunarr/
- Database: /root/arr-stack/config/tunarr/tunarr/db.db
- Port: 8000

## Sportarr
- Container: sportarr
- Port: 1867
- URL: http://192.168.11.66:1867
- Status: Installed, ready for configuration
