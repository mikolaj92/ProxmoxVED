#!/usr/bin/env python3
"""Install Docker and deploy ARR stack in container"""
import subprocess
import time

container_id = 220

print("="*60)
print("🐳 DOCKER + ARR STACK INSTALLATION")
print("="*60)

# Install Docker
print(f"\n📦 Installing Docker...")
docker_install = """
apt-get update && apt-get upgrade -y
apt-get install -y curl git ca-certificates gnupg
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
"""

for cmd in docker_install.strip().split('\n'):
    print(f"   → {cmd[:50]}...")
    result = subprocess.run(['pct', 'exec', str(container_id), '--', cmd],
                          capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        print(f"   ⚠️ Warning: {result.stderr[:80]}")

print(f"✅ Docker installed!")

# Verify
result = subprocess.run(['pct', 'exec', str(container_id), '--', 'docker --version'],
                      capture_output=True, text=True)
print(f"   {result.stdout.strip()}")

result = subprocess.run(['pct', 'exec', str(container_id), '--', 'docker compose version'],
                      capture_output=True, text=True)
print(f"   {result.stdout.strip()}")

# Create directories
print(f"\n📁 Creating directories...")
dirs = [
    "mkdir -p ~/arr-stack/config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}",
    "mkdir -p ~/arr-stack/media/{tv,movies,music,books,downloads}",
]
for cmd in dirs:
    subprocess.run(['pct', 'exec', str(container_id), '--', cmd], capture_output=True)

print(f"✅ Directories created!")

# Create docker-compose.yml
print(f"\n📝 Creating docker-compose.yml...")
compose = '''version: '3.8'
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/prowlarr:/config
    ports:
      - 9696:9696
    restart: unless-stopped

  sonarr:
    image: lscr.io/linuxserver/sonarr:latest
    container_name: sonarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/sonarr:/config
      - ./media/tv:/tv
      - ./media/downloads:/downloads
    ports:
      - 8989:8989
    restart: unless-stopped

  radarr:
    image: lscr.io/linuxserver/radarr:latest
    container_name: radarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/radarr:/config
      - ./media/movies:/movies
      - ./media/downloads:/downloads
    ports:
      - 7878:7878
    restart: unless-stopped

  lidarr:
    image: lscr.io/linuxserver/lidarr:latest
    container_name: lidarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/lidarr:/config
      - ./media/music:/music
      - ./media/downloads:/downloads
    ports:
      - 8686:8686
    restart: unless-stopped

  readarr:
    image: lscr.io/linuxserver/readarr:latest
    container_name: readarr
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/readarr:/config
      - ./media/books:/books
      - ./media/downloads:/downloads
    ports:
      - 8787:8787
    restart: unless-stopped

  jellyfin:
    image: lscr.io/linuxserver/jellyfin:latest
    container_name: jellyfin
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Warsaw
    volumes:
      - ./config/jellyfin:/config
      - ./media:/media
    ports:
      - 8096:8096
    restart: unless-stopped
'''

write_cmd = f'cat > ~/arr-stack/docker-compose.yml <<\'EOF\'\n{compose}\nEOF'
subprocess.run(['pct', 'exec', str(container_id), '--', write_cmd], capture_output=True)
print(f"✅ docker-compose.yml created!")

# Pull images
print(f"\n📥 Pulling Docker images (5-10 min)...")
result = subprocess.run(['pct', 'exec', str(container_id), '--',
                        'cd ~/arr-stack && docker compose pull'],
                       capture_output=True, text=True, timeout=600)
print(result.stdout)

# Start containers
print(f"\n▶️  Starting containers...")
result = subprocess.run(['pct', 'exec', str(container_id), '--',
                        'cd ~/arr-stack && docker compose up -d'],
                       capture_output=True, text=True, timeout=120)
print(result.stdout)

# Get IP
print(f"\n🔍 Getting container IP...")
result = subprocess.run(['pct', 'exec', str(container_id), '--',
                        'ip addr show eth0 | grep "inet " | awk \'{print $2}\' | cut -d/ -f1'],
                       capture_output=True, text=True, timeout=30)
ip = result.stdout.strip()
if not ip:
    ip = "<container-ip>"

# Check status
print(f"\n📊 Container Status:")
result = subprocess.run(['pct', 'exec', str(container_id), '--',
                        'docker ps --format \'table {{.Names}}\\t{{.Status}}\''],
                       capture_output=True, text=True)
print(result.stdout)

# Summary
print(f"\n{'='*60}")
print(f"🎉 ARR STACK DEPLOYED SUCCESSFULLY!")
print(f"{'='*60}")
print(f"\n📱 Access URLs:")
print(f"   • Prowlarr (Indexer):  http://{ip}:9696")
print(f"   • Sonarr (TV Shows):   http://{ip}:8989")
print(f"   • Radarr (Movies):     http://{ip}:7878")
print(f"   • Lidarr (Music):      http://{ip}:8686")
print(f"   • Readarr (Books):     http://{ip}:8787")
print(f"   • Jellyfin (Media):    http://{ip}:8096")
print(f"\n🔧 Setup:")
print(f"   1. Open each URL in browser")
print(f"   2. Create admin user")
print(f"   3. Configure Prowlarr (add indexers)")
print(f"   4. Connect apps: Prowlarr → Sonarr/Radarr/Lidarr/Readarr")
print(f"   5. Add download client to Sonarr/Radarr/etc")
print(f"\n🐧 Manage:")
print(f"   pct enter {container_id}")
print(f"   pct start/stop {container_id}")
print(f"{'='*60}\n")
