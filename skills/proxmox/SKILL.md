# Proxmox Skill - Zarządzanie Proxmox VE

Manage Proxmox VE virtualization platform - create VMs, LXC containers, deploy services.

## Installation

```bash
# Install Proxmoxer (Python API library)
pip install proxmoxer requests
```

## Configuration

Create `.env` file in workspace root:

```bash
# Proxmox API Credentials
PROXMOX_HOST=192.168.1.100  # Proxmox host IP
PROXMOX_USER=root@pam       # Username
PROXMOX_TOKEN_NAME=api_token # API token name
PROXMOX_TOKEN_VALUE=xxx     # API token secret
PROXMOX_VERIFY_SSL=false     # Skip SSL verification (for self-signed certs)
```

## Usage

### Create LXC Container
```python
from proxmox import ProxmoxAPI

proxmox = ProxmoxAPI(
    os.getenv('PROXMOX_HOST'),
    user=os.getenv('PROXMOX_USER'),
    token_name=os.getenv('PROXMOX_TOKEN_NAME'),
    token_value=os.getenv('PROXMOX_TOKEN_VALUE'),
    verify_ssl=False
)

# Create LXC container
proxmox.nodes('pve').lxc.create(
    vmid=100,
    ostemplate='local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst',
    hostname='arr-stack',
    cores=4,
    memory=8192,
    swap=2048,
    storage='local-lvm',
    password='root_password',
    net0='name=eth0,bridge=vmbr0,ip=dhcp'
)
```

### Create VM
```python
# Create VM
proxmox.nodes('pve').qemu.create(
    vmid=200,
    name='jellyfin-server',
    cores=4,
    memory=8192,
    sockets=1,
    cpu='host',
    scsihw='virtio-scsi-pci',
    virtio0='local-lvm:32,format=raw'
)
```

## ARR Stack Deployment

### Docker Compose for ARR Stack

```yaml
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
      - /srv/prowlarr/config:/config
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
      - /srv/sonarr/config:/config
      - /srv/media/tv:/tv
      - /srv/media/downloads:/downloads
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
      - /srv/radarr/config:/config
      - /srv/media/movies:/movies
      - /srv/media/downloads:/downloads
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
      - /srv/lidarr/config:/config
      - /srv/media/music:/music
      - /srv/media/downloads:/downloads
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
      - /srv/readarr/config:/config
      - /srv/media/books:/books
      - /srv/media/downloads:/downloads
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
      - /srv/jellyfin/config:/config
      - /srv/media:/media
    ports:
      - 8096:8096
    restart: unless-stopped
```

## Setup Steps

1. **Create LXC Container**
2. **Install Docker**
3. **Deploy Docker Compose**
4. **Configure Reverse Proxy (optional)**
5. **Setup ARR Apps**
6. **Test Connections**

## Notes

- Default ARR ports: Prowlarr 9696, Sonarr 8989, Radarr 7878, Lidarr 8686, Readarr 8787, Jellyfin 8096
- All services use PUID=1000, PGID=1000 (default user)
- Timezone: Europe/Warsaw
- Media path: /srv/media/{tv,movies,music,books,downloads}
