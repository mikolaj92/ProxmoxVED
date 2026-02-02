#!/usr/bin/env python3
"""Install Docker and deploy ARR stack using Proxmox API"""
from proxmoxer import ProxmoxAPI
import time
import json

container_id = 220

# Connect
proxmox = ProxmoxAPI(
    "192.168.11.199:8006",
    user='root@pam',
    token_name='mini_m4_1_bot',
    token_value='07099881-6fcc-4498-ab50-3df80f180c6e',
    verify_ssl=False
)

print("="*60)
print("🐳 DOCKER + ARR STACK INSTALLATION")
print("="*60)

# Install Docker
print(f"\n📦 Installing Docker...")
install_cmd = """
apt-get update && apt-get upgrade -y && \
apt-get install -y curl git ca-certificates gnupg && \
install -m 0755 -d /etc/apt/keyrings && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
chmod a+r /etc/apt/keyrings/docker.gpg && \
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
"""

print(f"   → Installing (this will take 2-3 minutes)...")
task = proxmox.nodes('pve').lxc(container_id).exec.post(
    command='bash',
    input=install_cmd.strip()
)

# Wait for completion
for i in range(180):
    try:
        status = proxmox.nodes('pve').tasks(task).status.get()
        if status.get('status') == 'stopped':
            if status.get('exitstatus') == 'OK':
                print(f"✅ Docker installed!")
                break
            else:
                print(f"❌ Installation failed!")
                print(f"   Exit status: {status.get('exitstatus')}")
                exit(1)
    except:
        pass
    if i % 30 == 0:
        print(f"   Progress: {i//30}/6 min...")
    time.sleep(1)

# Verify
result = proxmox.nodes('pve').lxc(container_id).exec.post(
    command='bash',
    input='docker --version && docker compose version',
    capture_output=True
)
time.sleep(5)
print(f"   {result}")

# Create directories
print(f"\n📁 Creating directories...")
dirs_cmd = """
mkdir -p ~/arr-stack/config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin} && \
mkdir -p ~/arr-stack/media/{tv,movies,music,books,downloads}
"""
proxmox.nodes('pve').lxc(container_id).exec.post(command='bash', input=dirs_cmd.strip())
time.sleep(3)
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

write_cmd = f'''cat > ~/arr-stack/docker-compose.yml <<'EOF'
{compose}
EOF
'''
proxmox.nodes('pve').lxc(container_id).exec.post(command='bash', input=write_cmd.strip())
time.sleep(2)
print(f"✅ docker-compose.yml created!")

# Pull images
print(f"\n📥 Pulling Docker images (5-10 min)...")
pull_cmd = 'cd ~/arr-stack && docker compose pull'
print(f"   → This will take a while, please be patient...")
task = proxmox.nodes('pve').lxc(container_id).exec.post(command='bash', input=pull_cmd)

# Wait with progress
for i in range(600):
    try:
        status = proxmox.nodes('pve').tasks(task).status.get()
        if status.get('status') == 'stopped':
            if status.get('exitstatus') == 'OK':
                print(f"✅ Images pulled!")
                break
    except:
        pass
    if i % 60 == 0 and i > 0:
        print(f"   Progress: {i//60} min...")
    time.sleep(1)

# Start containers
print(f"\n▶️  Starting containers...")
start_cmd = 'cd ~/arr-stack && docker compose up -d'
task = proxmox.nodes('pve').lxc(container_id).exec.post(command='bash', input=start_cmd)
time.sleep(10)

# Get container IP
print(f"\n🔍 Getting container IP...")
ip_cmd = 'ip addr show eth0 | grep "inet " | awk \'{print $2}\' | cut -d/ -f1'
task = proxmox.nodes('pve').lxc(container_id).exec.post(
    command='bash',
    input=ip_cmd,
    capture_output=True
)
time.sleep(3)

# Get IP from task output
try:
    # Try to get output from exec status
    exec_status = proxmox.nodes('pve').lxc(container_id).exec.get()
    # Find the most recent exec task
    ip = None
    for task_info in reversed(exec_status[-10:]):
        if task_info.get('command') == 'bash':
            # Fetch output
            try:
                out = proxmox.nodes('pve').lxc(container_id).exec(task_info['pid']).get('output')
                if out and out.strip():
                    ip = out.strip()
                    break
            except:
                pass
    if not ip:
        ip = "<container-ip>"
except:
    ip = "<container-ip>"

# Check container status
print(f"\n📊 Docker Container Status:")
ps_cmd = 'docker ps --format \'table {{.Names}}\\t{{.Status}}\''
task = proxmox.nodes('pve').lxc(container_id).exec.post(
    command='bash',
    input=ps_cmd,
    capture_output=True
)
time.sleep(3)

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
print(f"\n🔧 Setup Instructions:")
print(f"   1. Open each URL in browser")
print(f"   2. Create admin user for each service")
print(f"   3. Configure Prowlarr:")
print(f"      - Settings → Indexers → Add your favorite indexers")
print(f"   4. Connect Prowlarr to apps:")
print(f"      - Prowlarr → Settings → Apps → Sonarr → Add")
print(f"      - Repeat for Radarr, Lidarr, Readarr")
print(f"   5. Add download client to Sonarr/Radarr/etc:")
print(f"      - Settings → Download Clients → Add (Transmission/qBittorrent)")
print(f"   6. Setup Jellyfin:")
print(f"      - Add media libraries pointing to /media folders")
print(f"\n🐧 Manage Container:")
print(f"   pct enter {container_id}     # SSH into container")
print(f"   pct start {container_id}     # Start container")
print(f"   pct stop {container_id}      # Stop container")
print(f"{'='*60}\n")
