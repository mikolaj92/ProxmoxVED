# ARR Stack Deployment Guide on Proxmox

Complete guide to deploy full ARR stack on Proxmox LXC container.

## Prerequisites

- Proxmox VE installed
- At least 8GB RAM available
- 50GB+ storage
- Ubuntu 22.04 LXC template downloaded

## Step 1: Create LXC Container

### Option A: Using CLI (recommended)

```bash
# Clone Proxmox skill and navigate
cd /path/to/proxmox/skill

# Create container
python proxmox_cli.py create-lxc 100 arr-stack --cores 4 --memory 8192

# Copy output commands to Proxmox shell
```

### Option B: Manual Proxmox Web UI

1. Open Proxmox Web UI
2. Click "Create CT"
3. Configure:
   - **General:**
     - Hostname: `arr-stack`
     - Password: (set secure password)
     - SSH Public Key: (optional)

   - **Template:**
     - Storage: `local`
     - Template: `ubuntu-22.04-standard_22.04-1_amd64.tar.zst`

   - **Cores/Memory:**
     - Cores: 4
     - Memory: 8192 MB
     - Swap: 2048 MB

   - **Network:**
     - Bridge: `vmbr0`
     - IPv4: DHCP (or static IP)

   - **DNS:**
     - Domain: (your domain, e.g., `local`)
     - DNS Server 1: `1.1.1.1`
     - DNS Server 2: `8.8.8.8`

   - **Confirm:**
     - Start after created: ✅

4. Click "Create"

## Step 2: Install Docker

### SSH into container

```bash
# From Proxmox host
pct enter 100

# Or via SSH
ssh root@<container-ip>
```

### Install Docker

```bash
# Update packages
apt update && apt upgrade -y

# Install prerequisites
apt install -y curl git ca-certificates gnupg

# Install Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo \\
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \\
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \\
  tee /etc/apt/sources.list.d/docker.list > /dev/null

apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

## Step 3: Deploy ARR Stack

### Create project directory

```bash
mkdir -p ~/arr-stack
cd ~/arr-stack
```

### Create docker-compose.yml

```bash
cat > docker-compose.yml <<'EOF'
version: '3.8'
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
EOF
```

### Create media directories

```bash
mkdir -p config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}
mkdir -p media/{tv,movies,music,books,downloads}
```

### Start containers

```bash
docker compose up -d
```

### Verify deployment

```bash
# Check containers status
docker ps

# Check logs
docker logs prowlarr
docker logs sonarr
docker logs radarr
docker logs lidarr
docker logs readarr
docker logs jellyfin
```

## Step 4: Access Web UIs

Find your container IP:

```bash
ip addr show eth0
```

Access services:

- **Prowlarr:** http://<container-ip>:9696
- **Sonarr:** http://<container-ip>:8989
- **Radarr:** http://<container-ip>:7878
- **Lidarr:** http://<container-ip>:8686
- **Readarr:** http://<container-ip>:8787
- **Jellyfin:** http://<container-ip>:8096

## Step 5: Configure ARR Stack

### 5.1 Prowlarr (Indexer Manager)

1. Open Prowlarr: http://<container-ip>:9696
2. Create admin user
3. Add indexers:
   - Settings → Indexers → Add → Torznab/Newznab
   - Add your favorite indexers
4. Configure apps:
   - Settings → Apps → Sonarr → Add
   - Settings → Apps → Radarr → Add
   - Settings → Apps → Lidarr → Add
   - Settings → Apps → Readarr → Add

### 5.2 Sonarr (TV Series)

1. Open Sonarr: http://<container-ip>:8989
2. Create admin user
3. Configure Media Management:
   - Settings → Media Management
   - Root Folders: `/tv`
   - Delete empty folders: ✅
4. Configure Download Client:
   - Settings → Download Clients
   - Add your download client (Transmission, qBittorrent, etc.)
5. Connect to Prowlarr:
   - Settings → Indexers → Prowlarr → Add
   - Sync indexers from Prowlarr

### 5.3 Radarr (Movies)

1. Open Radarr: http://<container-ip>:7878
2. Create admin user
3. Configure Media Management:
   - Settings → Media Management
   - Root Folders: `/movies`
4. Configure Download Client
5. Connect to Prowlarr

### 5.4 Lidarr (Music)

1. Open Lidarr: http://<container-ip>:8686
2. Create admin user
3. Configure Media Management:
   - Settings → Media Management
   - Root Folders: `/music`
4. Configure Download Client
5. Connect to Prowlarr

### 5.5 Readarr (Books)

1. Open Readarr: http://<container-ip>:8787
2. Create admin user
3. Configure Media Management:
   - Settings → Media Management
   - Root Folders: `/books`
4. Configure Download Client
5. Connect to Prowlarr

### 5.6 Jellyfin (Media Server)

1. Open Jellyfin: http://<container-ip>:8096
2. Create admin user
3. Add media libraries:
   - Menu → Dashboard → Media Library → Add Media Library
   - TV Shows: `/media/tv`
   - Movies: `/media/movies`
   - Music: `/media/music`
   - Books: `/media/books`
4. Scan libraries:
   - Dashboard → Media Library → Scan Library

## Step 6: Setup Reverse Proxy (Optional)

### Install Nginx

```bash
apt install -y nginx
```

### Configure Nginx

```bash
cat > /etc/nginx/sites-available/arr <<'EOF'
server {
    listen 80;
    server_name arr.local;

    location /prowlarr/ {
        proxy_pass http://127.0.0.1:9696;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /sonarr/ {
        proxy_pass http://127.0.0.1:8989;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /radarr/ {
        proxy_pass http://127.0.0.1:7878;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /lidarr/ {
        proxy_pass http://127.0.0.1:8686;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /readarr/ {
        proxy_pass http://127.0.0.1:8787;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /jellyfin/ {
        proxy_pass http://127.0.0.1:8096;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -s /etc/nginx/sites-available/arr /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

Add to `/etc/hosts` on your computer:

```
<container-ip> arr.local
```

Access via reverse proxy:
- Prowlarr: http://arr.local/prowlarr
- Sonarr: http://arr.local/sonarr
- Radarr: http://arr.local/radarr
- Lidarr: http://arr.local/lidarr
- Readarr: http://arr.local/readarr
- Jellyfin: http://arr.local/jellyfin

## Troubleshooting

### Container won't start

```bash
# Check container status
pct status 100

# View container logs
pct log 100

# Start container
pct start 100
```

### Docker containers not starting

```bash
# Check Docker logs
docker logs <container_name>

# Restart Docker
systemctl restart docker

# Re-create containers
docker compose down
docker compose up -d
```

### Can't access web UIs

```bash
# Check if ports are listening
netstat -tlnp | grep -E '9696|8989|7878|8686|8787|8096'

# Check firewall
ufw status

# Allow ports
ufw allow 8096/tcp
ufw allow 8989/tcp
ufw allow 7878/tcp
ufw allow 8686/tcp
ufw allow 8787/tcp
ufw allow 9696/tcp
```

## Next Steps

1. Add download client (Transmission/qBittorrent)
2. Configure indexers in Prowlarr
3. Add media to Jellyfin
4. Setup auto-import in Sonarr/Radarr/Lidarr/Readarr
5. Enjoy your automated media center! 🎉
