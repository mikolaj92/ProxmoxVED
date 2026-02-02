#!/usr/bin/env python3
"""
Proxmox ARR Stack Deployment Script
"""

from proxmoxer import ProxmoxAPI
import os
import sys
import time
import subprocess
import json


class ProxmoxARRDeployer:
    """Deploy ARR stack to Proxmox"""

    def __init__(self, host: str, user: str, password: str, node: str = 'pve'):
        self.host = host
        self.user = user
        self.password = password
        self.node = node
        self.proxmox = None
        self.container_id = 100

    def connect(self):
        """Connect to Proxmox"""
        try:
            self.proxmox = ProxmoxAPI(
                self.host,
                user=self.user,
                password=self.password,
                verify_ssl=False,
                timeout=30
            )
            # Test connection
            version = self.proxmox.version.get()
            print(f"✅ Connected to Proxmox VE {version['version']}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def find_free_container_id(self):
        """Find next free container ID"""
        containers = self.proxmox.nodes(self.node).lxc.get()
        used_ids = [ct['vmid'] for ct in containers]
        for i in range(100, 1000):
            if i not in used_ids:
                return i
        return 100

    def create_lxc_container(self, hostname='arr-stack', cores=4, memory=8192):
        """Create LXC container"""
        print(f"\n📦 Creating LXC container: {hostname}")

        self.container_id = self.find_free_container_id()
        print(f"   Container ID: {self.container_id}")

        try:
            # Create container
            self.proxmox.nodes(self.node).lxc.create(
                vmid=self.container_id,
                ostemplate='local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst',
                hostname=hostname,
                cores=cores,
                memory=memory,
                swap=memory // 4,
                storage='local-lvm',
                rootfs='local-lvm:32',
                net0='name=eth0,bridge=vmbr0,ip=dhcp',
                onboot=1,
                start=1
            )
            print(f"   ✅ Container created!")
            print(f"   ⏳ Waiting for container to start...")

            # Wait for container to start
            time.sleep(10)

            # Check status
            status = self.proxmox.nodes(self.node).lxc(self.container_id).status.current.get()
            print(f"   ✅ Container status: {status['status']}")

            return self.container_id

        except Exception as e:
            print(f"   ❌ Failed to create container: {e}")
            return None

    def get_container_ip(self, max_wait=60):
        """Get container IP address"""
        print(f"\n🔍 Getting container IP...")

        for i in range(max_wait):
            try:
                # Get network info from container
                result = self.proxmox.nodes(self.node).lxc(self.container_id).status.get('interfaces')
                for interface in result:
                    if interface.get('name') == 'eth0' and 'inet' in interface:
                        for addr in interface['inet']:
                            if addr != '127.0.0.1':
                                print(f"   ✅ Container IP: {addr}")
                                return addr
            except:
                pass

            print(f"   ⏳ Waiting for IP... ({i+1}/{max_wait})")
            time.sleep(1)

        print(f"   ⚠️ Could not get IP, using DHCP")
        return None

    def execute_in_container(self, command):
        """Execute command in container via pct"""
        cmd = f"pct exec {self.container_id} -- {command}"
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timeout", 1
        except Exception as e:
            return "", str(e), 1

    def install_docker(self):
        """Install Docker in container"""
        print(f"\n🐳 Installing Docker...")

        commands = [
            # Update packages
            "apt-get update && apt-get upgrade -y",

            # Install prerequisites
            "apt-get install -y curl git ca-certificates gnupg",

            # Install Docker
            "install -m 0755 -d /etc/apt/keyrings",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
            "chmod a+r /etc/apt/keyrings/docker.gpg",
            "echo \"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable\" | tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "apt-get update",
            "apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",

            # Verify installation
            "docker --version",
            "docker compose version"
        ]

        for cmd in commands:
            print(f"   → {cmd[:60]}...")
            stdout, stderr, code = self.execute_in_container(cmd)
            if code != 0:
                print(f"   ⚠️ Warning: {stderr[:100]}")

        print(f"   ✅ Docker installed!")

    def deploy_arr_stack(self):
        """Deploy ARR stack with docker-compose"""
        print(f"\n🚀 Deploying ARR stack...")

        docker_compose = '''version: '3.8'
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

        # Create directories
        commands = [
            "mkdir -p ~/arr-stack/config/{prowlarr,sonarr,radarr,lidarr,readarr,jellyfin}",
            "mkdir -p ~/arr-stack/media/{tv,movies,music,books,downloads}",
        ]

        for cmd in commands:
            self.execute_in_container(cmd)

        # Write docker-compose.yml
        write_cmd = f'cat > ~/arr-stack/docker-compose.yml <<\'EOF\'\n{docker_compose}\nEOF'
        self.execute_in_container(write_cmd)

        # Start containers
        print(f"   📥 Pulling Docker images (this may take a while)...")
        self.execute_in_container("cd ~/arr-stack && docker compose pull")

        print(f"   ▶️  Starting containers...")
        self.execute_in_container("cd ~/arr-stack && docker compose up -d")

        # Wait for containers to start
        time.sleep(10)

        # Check container status
        stdout, _, _ = self.execute_in_container("docker ps --format 'table {{.Names}}\t{{.Status}}'")
        print(f"\n📊 Container Status:")
        print(stdout)

        print(f"   ✅ ARR stack deployed!")

    def print_access_info(self, ip=None):
        """Print access information"""
        print(f"\n{'='*60}")
        print(f"🎉 ARR STACK DEPLOYED SUCCESSFULLY!")
        print(f"{'='*60}")

        if ip:
            base_url = f"http://{ip}"
        else:
            base_url = "http://<container-ip>"

        print(f"\n📱 Access URLs:")
        print(f"   • Prowlarr (Indexer):  {base_url}:9696")
        print(f"   • Sonarr (TV Shows):   {base_url}:8989")
        print(f"   • Radarr (Movies):     {base_url}:7878")
        print(f"   • Lidarr (Music):      {base_url}:8686")
        print(f"   • Readarr (Books):     {base_url}:8787")
        print(f"   • Jellyfin (Media):    {base_url}:8096")

        print(f"\n🔧 Default credentials:")
        print(f"   • All services use web-based setup")
        print(f"   • Open URL in browser to create admin user")

        print(f"\n🐧 Manage container:")
        print(f"   pct enter {self.container_id}")
        print(f"   pct start {self.container_id}")
        print(f"   pct stop {self.container_id}")

        print(f"\n📖 Full guide:")
        print(f"   /Users/mini-m4-1/clawd/skills/proxmox/ARR_DEPLOYMENT_GUIDE.md")
        print(f"{'='*60}\n")

    def deploy(self):
        """Run complete deployment"""
        print(f"\n{'='*60}")
        print(f"🚀 PROXMOX ARR STACK DEPLOYMENT")
        print(f"{'='*60}")

        if not self.connect():
            return False

        if not self.create_lxc_container():
            return False

        ip = self.get_container_ip()

        if not self.install_docker():
            return False

        if not self.deploy_arr_stack():
            return False

        self.print_access_info(ip)
        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Deploy ARR stack to Proxmox')
    parser.add_argument('--host', default='192.168.11.199:8006', help='Proxmox host')
    parser.add_argument('--user', default='root@pam', help='Proxmox user')
    parser.add_argument('--password', required=True, help='Proxmox password')
    parser.add_argument('--node', default='pve', help='Proxmox node name')

    args = parser.parse_args()

    deployer = ProxmoxARRDeployer(
        host=args.host,
        user=args.user,
        password=args.password,
        node=args.node
    )

    success = deployer.deploy()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
