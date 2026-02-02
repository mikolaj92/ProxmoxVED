#!/usr/bin/env python3
"""Install Docker + ARR stack via SSH to Proxmox host"""
import subprocess
import time

PROXMOX_HOST = "192.168.11.199"
CT_ID = 220

print("="*60)
print("🐳 DOCKER + ARR STACK INSTALLATION (SSH)")
print("="*60)

# SSH command helper
def ssh_exec(cmd, timeout=600):
    """Execute command on Proxmox host via SSH"""
    full_cmd = f"ssh root@{PROXMOX_HOST} '{cmd}'"
    print(f"   → {cmd[:60]}...")

    result = subprocess.run(
        full_cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout
    )

    if result.returncode != 0:
        print(f"   ⚠️ Error: {result.stderr[:150]}")
        return False

    print(f"   ✅ Success!")
    return True

# Install Docker in container
print(f"\n📦 Installing Docker in CT {CT_ID}...")
docker_install = f"""
pct exec {CT_ID} -- bash -c '
apt-get update && apt-get upgrade -y && \\
apt-get install -y curl git ca-certificates gnupg && \\
install -m 0755 -d /etc/apt/keyrings && \\
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \\
chmod a+r /etc/apt/keyrings/docker.gpg && \\
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \\
apt-get update && \\
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin && \\
docker --version && \\
docker compose version
'
"""

if not ssh_exec(docker_install, timeout=600):
    print("❌ Docker installation failed!")
    exit(1)

print(f"✅ Docker installed!")

# Create directories
print(f"\n📁 Creating directories...")
ssh_exec(f"pct exec {CT_ID} -- mkdir -p ~/arr-stack/config/{{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}}")
ssh_exec(f"pct exec {CT_ID} -- mkdir -p ~/arr-stack/media/{{tv,movies,music,books,downloads}}")
print(f"✅ Directories created!")

# Create docker-compose.yml
print(f"\n📝 Creating docker-compose.yml...")
compose = '''version: '"'"'3.8'"'"'
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

write_cmd = f"""ssh root@{PROXMOX_HOST} "pct exec {CT_ID} -- bash -c 'cat > ~/arr-stack/docker-compose.yml <<'"'"'EOF'"'"'
{compose}
EOF
'"
"""
subprocess.run(write_cmd, shell=True, capture_output=True)
print(f"✅ docker-compose.yml created!")

# Pull images
print(f"\n📥 Pulling Docker images...")
print(f"   This will take 5-10 minutes...")
ssh_exec(f"pct exec {CT_ID} -- bash -c 'cd ~/arr-stack && docker compose pull'", timeout=900)
print(f"✅ Images pulled!")

# Start containers
print(f"\n▶️  Starting containers...")
ssh_exec(f"pct exec {CT_ID} -- bash -c 'cd ~/arr-stack && docker compose up -d'", timeout=120)
print(f"✅ Containers started!")

# Get IP
print(f"\n🔍 Getting container IP...")
result = subprocess.run(
    f"ssh root@{PROXMOX_HOST} 'pct exec {CT_ID} -- ip addr show eth0 | grep \"inet \" | awk '"'"'{{print $2}}'"'"' | cut -d/ -f1'",
    shell=True,
    capture_output=True,
    text=True,
    timeout=30
)
ip = result.stdout.strip()
if not ip:
    ip = "<container-ip>"
print(f"✅ Container IP: {ip}")

# Check status
print(f"\n📊 Docker Container Status:")
result = subprocess.run(
    f"ssh root@{PROXMOX_HOST} 'pct exec {CT_ID} -- docker ps --format '"'"'table {{{{.Names}}}}\\t{{{{
{.Status}}}}'"'"'",
    shell=True,
    capture_output=True,
    text=True,
    timeout=30
)
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
print(f"   3. Configure Prowlarr → Add indexers")
print(f"   4. Connect Prowlarr → Apps")
print(f"   5. Add download client")
print(f"   6. Setup Jellyfin")
print(f"\n🐧 Container CT {CT_ID} ready!")
print(f"{'='*60}\n")
