# MEMORY.md - Kluczowe informacje i projekty

---

## Projekt: Self-hosted services na Proxmox LXC (2026-02-02)

### Cel
Uruchomienie usług self-hosted w LXC kontenerach z danymi na oddzielnych volumes (dla łatwej migracji na NAS).

### Infrastruktura
- **Proxmox Host:** `192.168.11.199` (pve)
- **SSH Access:** `ssh -i ~/.ssh/proxmox_auto_arr root@192.168.11.199`
- **Storage Strategy:** Per-app volumes w `/srv/appdata/` + `/srv/media-immich/`

### Zainstalowane usługi

#### CT106 (alpine-vaultwarden) - 192.168.11.173:8000
- **Co:** Password manager (Bitwarden-compatible)
- **Mount:** `/srv/appdata/vaultwarden` → `/var/lib/vaultwarden`
- **Status:** ✅ Działa, dane przeniesione z local-lvm
- **Admin Token:** `2Hw77m4wSN/37Xus0lelFaCkOsDk7lS21aD56txCTyQ=` (w `/etc/conf.d/vaultwarden`)

#### CT108 (immich) - 192.168.11.225:2283
- **Co:** Zdjęcia/filmy (Google Photos alternative)
- **Mounts:**
  - `/srv/media-immich` → `/opt/immich/upload` (zdjęcia/filmy)
  - `/srv/appdata/immich` → `/opt/immich/cache` (cache/thumbs)
- **Status:** ✅ Działa, dane przeniesione z local-lvm
- **Components:** PostgreSQL 16, Redis, Immich Web (port 2283), Immich ML (port 3003)

#### CT220 (arr-stack) - 192.168.11.66
- **Co:** Media automation (Prowlarr, Sonarr, Radarr, Bazarr, Readarr, Lidarr, Transmission, Jellyseerr, Sportarr, Tunarr, xTeVe)
- **Mount:** `/srv/media` → `/root/arr-stack/media`
- **Status:** ✅ Działa, stabilny

#### CT230 (jellyfin) - 192.168.11.70:8096
- **Co:** Media server
- **Mount:** `/srv/media` → `/media`
- **Status:** ✅ Działa

### Kluczowe decyzje
1. **Per-app volumes** zamiast jednego dużego mounta = łatwiejsza migracja
2. **Bind mounts (mp0/mp1)** zamiast local-lvm = dane nie urosną w nieskończoność na local-lvm
3. **Unprivileged LXC** = lepsze security, ale UID mapping (100000 range)
4. **SSH `pct` commands** >> browser automation dla Proxmox (bardziej stabilne)

### Migracja na NAS - Plan
1. **RSYNC:** `rsync -av /srv/appdata/ /srv/media-immich/ /srv/media/ → NAS`
2. **Update mount points** na NFS/SMB
3. **Test** i rollback w razie problemów
4. **Dokumentacja:** `docs/proxmox-migration-guide.md` (szczegółowy przewodnik)

### Problemy rozwiązane
- ✅ **Mount points dodane** do CT106/CT108 (przed brakowało)
- ✅ **Dane przeniesione** z local-lvm do host volumes
- ✅ **Permissions poprawione** (unprivileged UID mapping)
- ✅ **Browser automation timeouty** → przejście na SSH `pct` commands

### API Keys (przechowywać bezpiecznie!)
- **Prowlarr:** `8c6dca6adf3644ba9a7981b736ef636f`
- **Bazarr:** `b081e213d5c6f981f2954277044e8454`
- **Readarr:** `2d3e8dae98f644b992dc5327ebf2d992`
- **Jellyfin:** `a3dd99094b9e4b38b5afd2e2cb4af390`
- **Transmission:** User `transmission`, Pass `Test123`

### ToDo (Future)
- [ ] Paperless-ngx (CT260) - zniszczony, do odtworzenia
- [ ] Nextcloud (CT270) - nigdy nie stworzony
- [ ] Setup backup automatyczny (vzdump schedule)
- [ ] Monitoring przestrzeni dyskowej na NAS

---

## Mini-m4-0 ("Lepszy Brat") - 192.168.1.52

### Dostęp
- **SSH:** `ssh mini-m4-0@192.168.1.52`, password: `domowycluster`
- **Telegram Bot:** `@mini_m4_0_bot`
- **OpenClaw:** Gateway + Node zainstalowane

### Status
- ✅ Gateway działa (PID 73456)
- ✅ Telegram skonfigurowany (dmPolicy: "open", allowFrom: ["*"])
- ✅ Model: "zai/glm-4.7" (zamiast broken "openai-codex:default")
- ⚠️ Czasami zgłasza "Unknown model: anthropic/openai-codex:default" (cache issue?)

### Cron Jobs
- **Nightly auto-update:** Codziennie 4:00 AM (Europe/Warsaw)
  - brew update/upgrade/cleanup
  - clawdhub update --all
  - qmd update
  - Telegram raport do user ID 8142555246

---

## inne

- **Browser automation** w Proxmox UI ma timeouty (nawet z 60s) - używać SSH
- **UV** > pip dla Python packages (10-100x szybszy)
- **Nightly cron** skopiowany z mini-m4-0 do lokalnego systemu

---

**Data utworzenia:** 2026-02-02  
**Ostatnia aktualizacja:** 2026-02-02
