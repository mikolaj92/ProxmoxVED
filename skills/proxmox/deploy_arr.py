#!/usr/bin/env python3
"""
Proxmox ARR Stack Deployment Script
Automates deployment of full ARR stack on Proxmox LXC container
"""

import os
import sys
import time
import subprocess
from pathlib import Path


class ARRStackDeployer:
    """Deploy ARR stack to Proxmox LXC container"""

    def __init__(self, proxmox_host: str, container_id: int):
        self.proxmox_host = proxmox_host
        self.container_id = container_id
        self.arr_ports = {
            'prowlarr': 9696,
            'sonarr': 8989,
            'radarr': 7878,
            'lidarr': 8686,
            'readarr': 8787,
            'jellyfin': 8096
        }

    def generate_docker_compose(self, media_path: str = '/srv/media') -> str:
        """Generate docker-compose.yml for ARR stack"""
        return f"""version: '3.8'
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
      - {media_path}/tv:/tv
      - {media_path}/downloads:/downloads
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
      - {media_path}/movies:/movies
      - {media_path}/downloads:/downloads
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
      - {media_path}/music:/music
      - {media_path}/downloads:/downloads
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
      - {media_path}/books:/books
      - {media_path}/downloads:/downloads
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
      - {media_path}:/media
    ports:
      - 8096:8096
    restart: unless-stopped

volumes:
  config:
"""

    def generate_nginx_config(self, domain: str) -> str:
        """Generate Nginx reverse proxy config"""
        configs = []
        for app, port in self.arr_ports.items():
            config = f"""
server {{
    listen 80;
    server_name {app}.{domain};

    location / {{
        proxy_pass http://127.0.0.1:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
            configs.append(config)
        return '\n'.join(configs)

    def deploy_to_container(self, ssh_host: str, ssh_user: str):
        """Deploy ARR stack to LXC container via SSH"""
        compose_file = self.generate_docker_compose()
        nginx_config = self.generate_nginx_config('arr.local')

        commands = [
            # Create directories
            f"mkdir -p ~/arr-stack/config/{{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}}",
            f"mkdir -p ~/arr-stack/media/{{tv,movies,music,books,downloads}}",

            # Write docker-compose.yml
            f'cat > ~/arr-stack/docker-compose.yml <<\'EOF\'\n{compose_file}\nEOF',

            # Write nginx config
            f'cat > ~/arr-stack/nginx.conf <<\'EOF\'\n{nginx_config}\nEOF',

            # Install Docker if not present
            "curl -fsSL https://get.docker.com | sh",
            "sudo usermod -aG docker $USER",

            # Deploy
            "cd ~/arr-stack",
            "docker compose up -d"
        ]

        for cmd in commands:
            print(f"Executing: {cmd[:50]}...")
            # subprocess.run(['ssh', f'{ssh_user}@{ssh_host}', cmd], check=True)


def main():
    """Main entry point"""
    if len(sys.argv) < 3:
        print("Usage: deploy_arr.py <proxmox_host> <container_id>")
        print("Example: deploy_arr.py 192.168.1.100 100")
        sys.exit(1)

    proxmox_host = sys.argv[1]
    container_id = int(sys.argv[2])

    deployer = ARRStackDeployer(proxmox_host, container_id)

    # Generate files locally first
    print("📝 Generating docker-compose.yml...")
    compose_file = deployer.generate_docker_compose()
    Path('docker-compose.yml').write_text(compose_file)
    print("✅ Generated: docker-compose.yml")

    print("\n📝 Generating nginx reverse proxy config...")
    nginx_config = deployer.generate_nginx_config('arr.local')
    Path('nginx.conf').write_text(nginx_config)
    print("✅ Generated: nginx.conf")

    print("\n🚀 Ready to deploy!")
    print(f"\nNext steps:")
    print(f"1. SSH into container: pct enter {container_id}")
    print(f"2. Copy files: scp docker-compose.yml root@{proxmox_host}:/root/")
    print(f"3. Run: docker compose up -d")
    print(f"\n🎯 Services will be available at:")
    for app, port in deployer.arr_ports.items():
        print(f"   - {app.capitalize()}: http://{proxmox_host}:{port}")


if __name__ == '__main__':
    main()
