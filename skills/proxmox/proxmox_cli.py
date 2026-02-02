#!/usr/bin/env python3
"""
Proxmox CLI - Easy Proxmox management from command line
"""

import os
import sys
import argparse
from pathlib import Path


def create_lxc_template(
    container_id: int,
    hostname: str,
    cores: int = 4,
    memory: int = 8192,
    storage: str = 'local-lvm',
    template: str = 'local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst',
    bridge: str = 'vmbr0'
) -> str:
    """Generate pct command to create LXC container"""

    return f"""# Create LXC Container: {hostname}
pct create {container_id} {template} \\
  --hostname {hostname} \\
  --cores {cores} \\
  --memory {memory} \\
  --swap {memory // 4} \\
  --storage {storage} \\
  --net0 name=eth0,bridge={bridge},ip=dhcp \\
  --rootfs {storage}:32 \\
  --onboot 1

# Start container
pct start {container_id}

# Enter container
pct enter {container_id}
"""


def create_vm_template(
    vm_id: int,
    name: str,
    cores: int = 4,
    memory: int = 8192,
    storage: str = 'local-lvm',
    disk_size: int = 32
) -> str:
    """Generate qm command to create VM"""

    return f"""# Create VM: {name}
qm create {vm_id} \\
  --name {name} \\
  --cores {cores} \\
  --memory {memory} \\
  --net0 virtio,bridge=vmbr0 \\
  --scsihw virtio-scsi-pci \\
  --scsi0 {storage}:{disk_size},format=raw \\
  --ide2 {storage}:cloudinit \\
  --boot order=scsi0 \\
  --agent enabled=1

# Import Ubuntu Cloud Image (optional)
# qm importdisk {vm_id} /path/to/ubuntu-22.04-server-cloudimg-amd64.img {storage}
# qm set {vm_id} --scsi0 {storage}:vm-{vm_id}-disk-0,format=raw

# Start VM
qm start {vm_id}

# Open console
qm terminal {vm_id}
"""


def install_docker_in_lxc(container_id: int) -> str:
    """Generate commands to install Docker in LXC container"""

    return f"""# Install Docker in LXC Container {container_id}
pct exec {container_id} -- bash -c '
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

# Enable Docker service
systemctl enable docker
systemctl start docker

# Verify installation
docker --version
docker compose version
'
"""


def list_containers():
    """List all LXC containers"""
    return "# List LXC Containers\npct list\n"


def list_vms():
    """List all VMs"""
    return "# List VMs\nqm list\n"


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Proxmox CLI - Easy Proxmox management')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create LXC container
    lxc_parser = subparsers.add_parser('create-lxc', help='Create LXC container')
    lxc_parser.add_argument('id', type=int, help='Container ID')
    lxc_parser.add_argument('hostname', help='Container hostname')
    lxc_parser.add_argument('--cores', type=int, default=4, help='CPU cores')
    lxc_parser.add_argument('--memory', type=int, default=8192, help='Memory in MB')
    lxc_parser.add_argument('--storage', default='local-lvm', help='Storage ID')
    lxc_parser.add_argument('--template', default='local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst', help='LXC template')
    lxc_parser.add_argument('--bridge', default='vmbr0', help='Network bridge')

    # Create VM
    vm_parser = subparsers.add_parser('create-vm', help='Create VM')
    vm_parser.add_argument('id', type=int, help='VM ID')
    vm_parser.add_argument('name', help='VM name')
    vm_parser.add_argument('--cores', type=int, default=4, help='CPU cores')
    vm_parser.add_argument('--memory', type=int, default=8192, help='Memory in MB')
    vm_parser.add_argument('--storage', default='local-lvm', help='Storage ID')
    vm_parser.add_argument('--disk', type=int, default=32, help='Disk size in GB')

    # Install Docker
    docker_parser = subparsers.add_parser('install-docker', help='Install Docker in LXC')
    docker_parser.add_argument('id', type=int, help='Container ID')

    # List
    subparsers.add_parser('list-lxc', help='List LXC containers')
    subparsers.add_parser('list-vm', help='List VMs')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'create-lxc':
        output = create_lxc_template(
            args.id, args.hostname, args.cores, args.memory,
            args.storage, args.template, args.bridge
        )
    elif args.command == 'create-vm':
        output = create_vm_template(
            args.id, args.name, args.cores, args.memory, args.storage, args.disk
        )
    elif args.command == 'install-docker':
        output = install_docker_in_lxc(args.id)
    elif args.command == 'list-lxc':
        output = list_containers()
    elif args.command == 'list-vm':
        output = list_vms()
    else:
        parser.print_help()
        sys.exit(1)

    print(output)


if __name__ == '__main__':
    main()
