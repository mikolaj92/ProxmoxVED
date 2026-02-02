# ✅ Konfiguracja xTeVe z polskimi kanałami

## Playlisty z Free-TV/IPTV

### Główna playlista (wszystkie kanały):
```
https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8
```

### Tylko polskie kanały (odfiltrowane):
Musimy stworzyć własną playlistę z pliku poland.md

## Lista polskich kanałów z Free-TV:

### DVB-T (nadawane naziemnie):
1. TVP1
2. TVP2
3. TVP3 Warszawa
4. TVP Polonia
5. Alfa TVP
6. TVP Info
7. TVP World
8. TVP ABC 2
9. TVP Historia 2
10. TVP Kultura 2
11. Belsat

### DVB-S (satelita):
1. TV Republika
2. 4fun.tv

## Konfiguracja w xTeVe:

### Krok 1: Dodaj główną playlistę
URL: `https://raw.githubusercontent.com/Free-TV/IPTV/master/playlist.m3u8`

### Krok 2: Filtruj polskie kanały
W Mapping wyszukaj kanały z "pl" lub "Poland"

### Krok 3: Dodaj do Jellyfin
HDHomeRun URL: `http://192.168.11.66:34400`

Gotowe!
