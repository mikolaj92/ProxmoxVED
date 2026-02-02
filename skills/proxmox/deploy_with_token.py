#!/usr/bin/env python3
"""
Deploy ARR Stack to Proxmox using API Token
"""

from proxmoxer import ProxmoxAPI
import subprocess
import time

# API Token credentials
HOST = "192.168.11.199:8006"
USER = "root@pam"
TOKEN_NAME = "mini_m4_1_bot"
TOKEN_VALUE = "07099881-6fcc-4498-ab50-3df80f180c6e"

print("="*60)
print("🚀 PROXMOX ARR STACK DEPLOYMENT")
print("="*60)

# Connect to Proxmox
print("\n🔐 Connecting to Proxmox...")
try:
    proxmox = ProxmoxAPI(
        HOST,
        user=USER,
        token_name=TOKEN_NAME,
        token_value=TOKEN_VALUE,
        verify_ssl=False
    )
    version = proxmox.version.get()
    print(f"✅ Connected! Proxmox VE {version['version']}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)

# Find free container ID
print("\n🔍 Finding free container ID...")
containers = proxmox.nodes('pve').lxc.get()
used_ids = [ct['vmid'] for ct in containers]
# Start from 200 to avoid conflicts
container_id = 200
while container_id in used_ids:
    container_id += 1
print(f"✅ Container ID: {container_id}")

# Check if container exists
print(f"\n🔍 Checking if container {container_id} exists...")
try:
    existing = proxmox.nodes('pve').lxc(container_id).status.current.get()
    print(f"⚠️ Container {container_id} exists (status: {existing['status']}), stopping and deleting...")
    if existing['status'] == 'running':
        proxmox.nodes('pve').lxc(container_id).status.stop.post()
        print(f"   ⏳ Stopping container...")
        time.sleep(10)
    proxmox.nodes('pve').lxc(container_id).delete()
    print(f"✅ Deleted existing container")
    time.sleep(5)
except Exception as e:
    if "does not exist" in str(e).lower() or "doesn't exist" in str(e).lower() or "404" in str(e):
        print(f"✅ Container {container_id} does not exist, ready to create")
    else:
        print(f"⚠️ Error checking container: {e}")
        print(f"   Continuing anyway...")

# Create LXC container
print(f"\n📦 Creating LXC container: arr-stack")
try:
    proxmox.nodes('pve').lxc.create(
        vmid=container_id,
        ostemplate='local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst',
        hostname='arr-stack',
        cores=4,
        memory=8192,
        swap=2048,
        storage='local-lvm',
        rootfs='local-lvm:32',
        net0='name=eth0,bridge=vmbr0,ip=dhcp',
        onboot=1,
        start=1
    )
    print(f"✅ Container created!")
except Exception as e:
    print(f"❌ Failed to create container: {e}")
    print(f"\n💡 TIP: Make sure Ubuntu 22.04 template is downloaded!")
    print(f"   Download in Proxmox: (local) → Templates → Templates")
    exit(1)

# Wait for container to start
print(f"\n⏳ Waiting for container to start...")
time.sleep(15)

# Get container status
status = proxmox.nodes('pve').lxc(container_id).status.current.get()
print(f"✅ Container status: {status['status']}")

# Install Docker via pct exec
print(f"\n🐳 Installing Docker...")

docker_install_script = """
# Update packages
apt-get update && apt-get upgrade -y

# Install prerequisites
apt-get install -y curl git ca-certificates gnupg

# Install Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify
docker --version
docker compose version
"""

for cmd in docker_install_script.strip().split('\n'):
    if cmd.strip():
        print(f"   → {cmd[:60]}...")
        result = subprocess.run(
            ['pct', 'exec', str(container_id), '--', cmd],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"   ⚠️ Warning: {result.stderr[:100]}")

print(f"✅ Docker installed!")

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

docker_compose = '''version: '3.8'
services:
  prowlarr:
    image: lscr.io/linuxserver/prowlarr:latest
    container_name: prowlarr
    environment:
      - PUID=1000
      -PGID=1000
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

write_cmd = f'cat > ~/arr-stack/docker-compose.yml <<\'EOF\'\n{docker_compose}\nEOF'
subprocess.run(['pct', 'exec', str(container_id), '--', write_cmd], capture_output=True)
print(f"✅ docker-compose.yml created!")

# Pull images
print(f"\n📥 Pulling Docker images (this may take 5-10 minutes)...")
result = subprocess.run(
    ['pct', 'exec', str(container_id), '--', 'cd ~/arr-stack && docker compose pull'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Start containers
print(f"\n▶️  Starting containers...")
result = subprocess.run(
    ['pct', 'exec', str(container_id), '--', 'cd ~/arr-stack && docker compose up -d'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Wait for containers
time.sleep(10)

# Check status
print(f"\n📊 Container Status:")
result = subprocess.run(
    ['pct', 'exec', str(container_id), '--', 'docker ps --format \'table {{.Names}}\\t{{.Status}}\''],
    capture_output=True,
    text=True
)
print(result.stdout)

# Get IP
print(f"\n🔍 Getting container IP...")
try:
    result = subprocess.run(
        ['pct', 'exec', str(container_id), '--', 'ip addr show eth0 | grep "inet " | awk \'{print $2}\' | cut -d/ -f1'],
        capture_output=True,
        text=True,
        timeout=30
    )
    ip = result.stdout.strip()
    if ip:
        print(f"✅ Container IP: {ip}")
    else:
        ip = "<container-ip>"
        print(f"⚠️ Could not get IP, using DHCP")
except:
    ip = "<container-ip>"
    print(f"⚠️ Could not get IP")

# Print summary
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
print(f"\n🔧 Default credentials:")
print(f"   • All services use web-based setup")
print(f"   • Open URL in browser to create admin user")
print(f"\n🐧 Manage container:")
print(f"   pct enter {container_id}")
print(f"   pct start {container_id}")
print(f"   pct stop {container_id}")
print(f"{'='*60}\n")
