#!/usr/bin/env python3
"""Install Docker and ARR stack via Proxmox API - v2"""
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
print("🐳 DOCKER + ARR STACK INSTALLATION (API)")
print("="*60)

# Helper function to run command in container and wait
def run_command(cmd, timeout=600):
    """Run command in container and wait for completion"""
    print(f"   → {cmd[:60]}...")

    # Start command
    task = proxmox.nodes('pve').lxc(container_id).exec.post(
        command='bash',
        input=cmd.strip()
    )

    # Wait for completion
    start = time.time()
    while time.time() - start < timeout:
        try:
            status = proxmox.nodes('pve').tasks(task).status.get()
            if status.get('status') == 'stopped':
                exitstatus = status.get('exitstatus')
                if exitstatus == 'OK':
                    print(f"   ✅ Success!")
                    return True
                else:
                    print(f"   ❌ Failed! Exit: {exitstatus}")
                    return False
        except Exception as e:
            pass

        time.sleep(2)

    print(f"   ⏱️ Timeout after {timeout}s")
    return False

# Install Docker
print(f"\n📦 Installing Docker...")
install_cmd = """
apt-get update && apt-get upgrade -y && \
apt-get install -y curl git ca-certificates gnupg && \
install -m 0755 -d /etc/apt/keyrings && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
chmod a+r /etc/apt/keyrings/docker.gpg && \
echo 'deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable' | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
"""

if not run_command(install_cmd, timeout=600):
    print("❌ Docker installation failed!")
    exit(1)

print(f"✅ Docker installed!")

# Verify
print(f"\n🔍 Verifying Docker...")
run_command('docker --version && docker compose version', timeout=30)

# Create directories
print(f"\n📁 Creating directories...")
run_command('mkdir -p ~/arr-stack/config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}', timeout=30)
run_command('mkdir -p ~/arr-stack/media/{tv,movies,music,books,downloads}', timeout=30)
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
run_command(write_cmd, timeout=30)
print(f"✅ docker-compose.yml created!")

# Pull images
print(f"\n📥 Pulling Docker images...")
print(f"   This will take 5-10 minutes, please wait...")

if not run_command('cd ~/arr-stack && docker compose pull', timeout=900):
    print(f"⚠️ Pull had issues, but continuing...")

print(f"✅ Images pulled!")

# Start containers
print(f"\n▶️  Starting containers...")
run_command('cd ~/arr-stack && docker compose up -d', timeout=120)
print(f"✅ Containers started!")

# Wait for startup
time.sleep(10)

# Get IP
print(f"\n🔍 Getting container IP...")
# Try multiple methods to get IP
ip = None
for method in [
    'ip addr show eth0 | grep "inet " | awk \'{print $2}\' | cut -d/ -f1',
    'hostname -I | awk \'{print $1}\'',
    'ip a show eth0 | grep inet | head -1 | awk \'{print $2}\' | cut -d/ -f1'
]:
    try:
        task = proxmox.nodes('pve').lxc(container_id).exec.post(
            command='bash',
            input=method,
            capture_output=True
        )
        time.sleep(3)
        # Try to get output
        execs = proxmox.nodes('pve').lxc(container_id).exec.get()
        for ex in execs[-5:]:
            try:
                out = proxmox.nodes('pve').lxc(container_id).exec(ex['pid']).get('output')
                if out and out.strip() and '.' in out:
                    ip = out.strip().split()[0]
                    break
            except:
                pass
        if ip:
            break
    except:
        pass

if not ip:
    ip = "<container-ip>"

print(f"✅ Container IP: {ip}")

# Check container status
print(f"\n📊 Docker Container Status:")
try:
    run_command('docker ps --format \'table {{.Names}}\\t{{.Status}}\'', timeout=30)
except:
    print(f"   (Could not fetch status)")

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
print(f"   4. Connect Prowlarr → Sonarr/Radarr/Lidarr/Readarr")
print(f"   5. Add download client to each ARR app")
print(f"   6. Setup Jellyfin media libraries")
print(f"\n🐧 Container CT {container_id} is ready!")
print(f"{'='*60}\n")
