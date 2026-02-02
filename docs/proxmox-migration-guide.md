# Proxmox Migration Guide & Documentation

**Data:** 2026-02-02  
**Cel:** Migracja danych z Proxmox hosta na NAS + dokumentacja konfiguracji LXC

---

## 1. Obecna struktura (Stan na 2026-02-02)

### Proxmox Host
- **Host:** `192.168.11.199` (pve)
- **SSH:** `ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199`
- **Storage:** `/dev/mapper/pve-root` (94G, 82G used = 92%)

### Host Volumes (Przygotowane do migracji na NAS)
```
/srv/
├── appdata/
│   ├── vaultwarden/     # CT106 - dane Vaultwarden
│   ├── immich/          # CT108 - cache Immich
│   ├── jellyfin/        # CT230 - dane Jellyfin
│   ├── nextcloud/       # (przygotowane, nieaktywne)
│   └── paperless/       # (przygotowane, nieaktywne)
└── media-immich/        # CT108 - upload zdjęć/filmów
```

### Kontenery LXC z Mount Points

#### CT106 (alpine-vaultwarden) - 192.168.11.173:8000
```bash
# Konfiguracja
pct config 106 | grep mp
# mp0: /srv/appdata/vaultwarden,mp=/var/lib/vaultwarden

# Service
rc-service vaultwarden status

# Dane w kontenerze
/var/lib/vaultwarden/          # → /srv/appdata/vaultwarden (host)
  ├── db.sqlite3               # baza danych
  ├── db.sqlite3-shm
  ├── db.sqlite3-wal
  ├── rsa_key.pem
  ├── tmp/
  └── .env
```

#### CT108 (immich) - 192.168.11.225:2283
```bash
# Konfiguracja
pct config 108 | grep mp
# mp0: /srv/media-immich,mp=/opt/immich/upload
# mp1: /srv/appdata/immich,mp=/opt/immich/cache

# Services
systemctl status immich-web          # active
systemctl status immich-machine-learning  # inactive (OK)

# Dane w kontenerze
/opt/immich/upload/           # → /srv/media-immich (host) = zdjęcia/filmy
/opt/immich/cache/            # → /srv/appdata/immich (host) = cache/thumbs
```

#### CT220 (arr-stack) - 192.168.11.66
```bash
# Mount
mp0: /srv/media,mp=/root/arr-stack/media
```

#### CT230 (jellyfin) - 192.168.11.70:8096
```bash
# Mount
mp0: /srv/media,mp=/media
```

---

## 2. Migracja na NAS - Plan

### Krok 1: Przygotowanie NAS
1. **Utwórz foldery na NAS:**
   ```bash
   ssh user@nas
   mkdir -p /volume1/proxmox-migration/{appdata,media-immich,media}
   ```

2. **Skonfiguruj NFS/SMB:**
   - NFS: `/etc/exports` na NAS
   - SMB: udostępnij foldery

### Krok 2: Test NAS (opcjonalnie)
```bash
# Na Proxmox host
mount -t nfs nas-ip:/volume1/proxmox-migration /mnt/test-nas
rsync -av --dry-run /srv/appdata/ /mnt/test-nas/appdata/
umount /mnt/test-nas
```

### Krok 3: Migracja danych (Rsync)
```bash
# Z Proxmox hosta - UTWÓRZ SNAPSHOT PIERWSZY!
ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199

# Migracja appdata (Vaultwarden, Immich cache, etc.)
rsync -av --progress /srv/appdata/ nas-user@nas-ip:/volume1/proxmox-migration/appdata/

# Migracja Immich upload (zdjęcia/filmy)
rsync -av --progress /srv/media-immich/ nas-user@nas-ip:/volume1/proxmox-migration/media-immich/

# Migracja media (ARR stack + Jellyfin)
rsync -av --progress /srv/media/ nas-user@nas-ip:/volume1/proxmox-migration/media/
```

**Czas migracji (szacunkowy):**
- `/srv/appdata/` - kilka minut (~100MB)
- `/srv/media-immich/` - zależy od ilości zdjęć
- `/srv/media/` - zależy od biblioteki filmów/seriali

### Krok 4: Update LXC configurations (POST-MIGRACJA)

**PRZED ZMIANAMI:** Stop wszystkie kontenery używające mount points!
```bash
pct shutdown 106 108 220 230
```

**Zmień mount points na NFS:**
```bash
# CT106 (Vaultwarden)
pct set 106 -mp0 nas-ip:/volume1/proxmox-migration/appdata/vaultwarden,mp=/var/lib/vaultwarden

# CT108 (Immich)
pct set 108 -mp0 nas-ip:/volume1/proxmox-migration/media-immich,mp=/opt/immich/upload
pct set 108 -mp1 nas-ip:/volume1/proxmox-migration/appdata/immich,mp=/opt/immich/cache

# CT220 (arr-stack)
pct set 220 -mp0 nas-ip:/volume1/proxmox-migration/media,mp=/root/arr-stack/media

# CT230 (Jellyfin)
pct set 230 -mp0 nas-ip:/volume1/proxmox-migration/media,mp=/media
```

**Start kontenery:**
```bash
pct start 106 108 220 230
```

### Krok 5: Weryfikacja
```bash
# Sprawdź czy mounty są NFS
pct exec 106 -- df -h | grep var
pct exec 108 -- df -h | grep opt

# Sprawdź czy serwisy działają
pct exec 106 -- rc-service vaultwarden status
pct exec 108 -- systemctl status immich-web
```

---

## 3. Komendy zarządzania Proxmox (Szybki reference)

### Podstawowe operacje LXC
```bash
# Lista kontenerów
pct list

# Status kontenera
pct status <CTID>

# Start/Stop/Shutdown
pct start <CTID>
pct shutdown <CTID>
pct stop <CTID>

# Exec command w kontenerze
pct exec <CTID> -- command

# Config kontenera
pct config <CTID>
```

### Mount Points (Bind mounts)
```bash
# Dodaj mount point
pct set <CTID> -mp0 /host/path,mp=/container/path

# Dodaj NFS mount
pct set <CTID> -mp0 nfs-server:/export/path,mp=/container/path

# Usuń mount point
pct set <CTID> -mp0 del

# Zmień options (opcjonalnie)
pct set <CTID> -mp0 /host/path,mp=/container/path,ro=1  # read-only
```

### Backup (przed migracją!)
```bash
# Backup całego kontenera
vzdump 106 --storage local --mode snapshot
vzdump 108 --storage local --mode snapshot
```

---

## 4. Disaster Recovery

### Jeśli coś pójdzie źle po migracji:
1. **Rollback mount points:**
   ```bash
   pct shutdown <CTID>
   pct set <CTID> -mp0 /srv/...,mp=/...  # powrót na lokalne
   pct start <CTID>
   ```

2. **Przywróć z backupu vzdump:**
   ```bash
   pct restore 106 /var/lib/vz/dump/vzdump-lxc-106-*.tar.zst
   ```

### Kopia bezpieczeństwa danych (RSYNC do innej lokacji)
```bash
# Z Proxmox hosta - rsync do backup location
rsync -av --delete /srv/appdata/ backup-server:/proxmox-backup/appdata/
rsync -av --delete /srv/media-immich/ backup-server:/proxmox-backup/media-immich/
```

---

## 5. Przydatne komendy (Debugging)

### Sprawdzenie przestrzeni dyskowej
```bash
# Na Proxmox host
df -h | grep pve
lvs

# W kontenerze
pct exec 108 -- df -h
pct exec 106 -- du -sh /var/lib/vaultwarden
```

### Sprawdzenie mount points
```bash
# Wszystkie mounty w kontenerze
pct exec 108 -- mount | grep opt

# Konfiguracja mount points
pct config 108 | grep mp
```

### Permissions (Unprivileged containers)
```bash
# UID/GID mapping: 100000 range
# UID 999 w CT = UID 100999 na hoście

# Zmiana ownera na hoście
chown -R 100999:100991 /srv/media-immich
chown -R 100100:100100 /srv/appdata/vaultwarden
```

---

## 6. ToDo (Future improvements)

- [ ] Ograniczyć rozmiar logów Immich (może urosnąć)
- [ ] Setup backup automatyczny (vzdump schedule)
- [ ] Monitoring przestrzeni dyskowej na NAS
- [ ] Consider ZFS instead of ext4 na NAS (dla lepszych snapshots)
- [ ] Test failover (NAS down = co się stanie z CT?)

---

## 7. Historia zmian

**2026-02-02:**
- ✅ Utworzone `/srv/appdata/` i `/srv/media-immich/` na Proxmox host
- ✅ CT106 (Vaultwarden): mp0 `/var/lib/vaultwarden` → `/srv/appdata/vaultwarden`
- ✅ CT108 (Immich): mp0 `/opt/immich/upload` → `/srv/media-immich`
- ✅ CT108 (Immich): mp1 `/opt/immich/cache` → `/srv/appdata/immich`
- ✅ Dane przeniesione z local-lvm do host volumes
- ✅ Dokumentacja utworzona

**Przed migracją (user install):**
- CT106 i CT108 były zainstalowane przez usera z community scripts
- Dane siedziały w local-lvm (rootfs)
- Brak mount points = ryzyko "puchnięcia" local-lvm

---

## 8. Kluczowe lekcje

1. **Per-app volumes** = łatwiejsza migracja niż jeden wielki mount
2. **Unprivileged LXC** → UID mapping (100000 range)
3. **SSH `pct` commands** >> browser automation dla Proxmox
4. **Test migracji na małym CT** (Vaultwarden) zanim duży (Immich)
5. **Backup PRZED zmianami mount points** (vzdump)
6. **Bind mounts > local-lvm** dla danych użytkownika

---

**Autor:** Claude (OpenClaw)  
**Data dokumentacji:** 2026-02-02  
**Wersja:** 1.0
