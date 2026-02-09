# CT107: OVH DynHost IP Update - Dokumentacja

## Cel
Kontener CT107 odpowiada za automatyczne aktualizowanie adresów IP dla domen hostowanych na OVH poprzez DynHost API.

## Mechanizm

### Cron Job (root)
```bash
5 * * * * sh /root/<nazwa_skryptu>.sh >> /root/<nazwa_skryptu>.log 2>&1
```
- Uruchamia się co godzinę, na 5 min każdej godziny
- Logi zapisywane są do plików `.log`

### Skrypty
W `/root/` znajdują się osobne skrypty dla każdej domeny/grupy:
- `emitype_de.sh` - emitype.de
- `emitype_com_pl.sh` - emitype.com.pl
- `patryk_it.sh` - patryk.it
- `mikoy_eu.sh` - mikoy.eu
- `kajtek_it.sh` - kajtek.it

Każdy skrypt zawiera:
```bash
DYNHOST_USER="<login-OVH>"
DYNHOST_PASSWD="<hasło-OVH>"
DYNHOST_DOMAIN="<domena>"
OVH_URL="https://www.ovh.com/nic/update?system=dyndns"
```

Skrypt wywołuje:
```bash
curl --user "$DYNHOST_USER:$DYNHOST_PASSWD" "${OVH_URL}&hostname=${DYNHOST_DOMAIN}"
```

### Dodanie nowej domeny
1. Skopiuj istniejący skrypt (np. `cp patryk_it.sh nowa_domena.sh`)
2. Edytuj zmienne: `DYNHOST_USER`, `DYNHOST_PASSWD`, `DYNHOST_DOMAIN`
3. Dodaj wpis w crontab: `5 * * * * sh /root/nowa_domena.sh >> /root/nowa_domena.log 2>&1`
4. Sprawdź logi: `tail -f /root/nowa_domena.log`

### Status i testy
- **Sprawdzenie crontab:** `cat /var/spool/cron/crontabs/root`
- **Test skryptu:** `sh /root/patryk_it.sh`
- **Logi:** `tail -f /root/patryk_it.log`
- **Processy:** `ps aux | grep curl` (podczas wykonywania)

### ddclient
Pakiet `ddclient` jest zainstalowany, ale **NIEUŻYWANY**. Konfiguracja w `/etc/ddclient.conf` jest niekompletna. Można go usunąć, aby zwolnić zasoby:
```bash
apk del ddclient
```

### Ważne uwagi
- OVH DynHost wymaga, aby domena była wcześniej skonfigurowana w panelu OVH ( Management → Zone DNS → DynHost )
- Każda domena ma osobne kredencje (login/hostname + hasło)
- Aktualizacja IP następuje co godzinę (można zmienić w crontab)
- Skrypty nie sprawdzają, czy zmiana IP się powiodła - patrz logi

## Troubleshooting
- **Brak aktualizacji:** sprawdź logi `.sh.log` pod kątem błędów curl
- **Authentication failed:** sprawdź login/hasło w skrypcie
- **Host not found:** upewnij się, że domena istnieje w DynHost i jest poprawnie wpisana

---

**Utworzono:** 2026-02-04
**Autor:** Alek (OpenClaw agent)
**CT VMID:** 107
