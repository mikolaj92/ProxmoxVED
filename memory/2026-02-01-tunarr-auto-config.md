# Automatyczna Konfiguracja Tunarr

Ten skrypt JavaScript automatycznie skonfiguruje Tunarr:
1. Doda programowanie do kanału "Movies 24/7"
2. Pobierze listę filmów z Jellyfin
3. Wygeneruje XMLTV i M3U

## Instrukcja

### Krok 1: Otwórz Tunarr
W przeglądarce: http://192.168.11.66:8000

### Krok 2: Otwórz Developer Console
- **Chrome/Edge**: F12 → zakładka "Console"
- **Firefox**: F12 → zakładka "Console"

### Krok 3: Wklej i uruchom poniższy kod

```javascript
// Automatyczna konfiguracja Tunarr
(async function() {
    console.log('🚀 Konfiguracja Tunarr...');
    
    try {
        // Pobierz kanały
        const channelsRes = await fetch('/api/channels');
        const channels = await channelsRes.json();
        const moviesChannel = channels.find(c => c.name === 'Movies 24/7');
        
        if (!moviesChannel) {
            console.error('❌ Kanał "Movies 24/7" nie znaleziony!');
            return;
        }
        
        console.log('✅ Kanał znaleziony:', moviesChannel);
        
        // Pobierz biblioteki
        const libsRes = await fetch('/api/libraries');
        const libs = await libsRes.json();
        const moviesLib = libs.find(l => l.type === 'movies' && l.name.includes('Movies'));
        
        if (!moviesLib) {
            console.error('❌ Biblioteka Movies nie znaleziona!');
            return;
        }
        
        console.log('✅ Biblioteka znaleziona:', moviesLib);
        
        // Dodaj programowanie Flex
        const programming = {
            channelId: moviesChannel.uuid,
            libraryId: moviesLib.uuid,
            type: 'flex',
            startTime: 0, // 00:00
            duration: 86400000, // 24h
            fillStyle: 'random',
            enabled: true
        };
        
        const progRes = await fetch('/api/programming', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(programming)
        });
        
        if (progRes.ok) {
            console.log('✅ Programowanie dodane!');
            console.log('🎬 Kanał "Movies 24/7" jest gotowy!');
            console.log('');
            console.log('📺 Sprawdź:');
            console.log('  - XMLTV: http://192.168.11.66:8000/xmltv.xml');
            console.log('  - M3U: http://192.168.11.66:8000/lineups.m3u');
        } else {
            console.error('❌ Błąd dodawania programowania');
        }
        
    } catch (error) {
        console.error('❌ Błąd:', error);
    }
})();
```

### Krok 4: Sprawdź wynik
Po uruchomieniu skryptu:
1. Odśwież stronę Channels
2. Kliknij "Movies 24/7"
3. Zakładka "Programming" - powinno pokazywać programy
4. Sprawdź XMLTV: http://192.168.11.66:8000/xmltv.xml

### Krok 5: Dodaj do Jellyfin
Opcja A - HDHomeRun:
- Jellyfin Dashboard → Live TV → Add HDHomeRun tuner
- Tunarr zostanie wykryty automatycznie

Opcja B - M3U:
- Jellyfin Dashboard → Live TV → Add M3U tuner
- URL: http://192.168.11.66:8000/lineups.m3u
- XMLTV: http://192.168.11.66:8000/xmltv.xml

## Troubleshooting

### "Błąd: /api/channels not found"
- Tunarr używa innej wersji API
- Skonfiguruj ręcznie przez Web UI (patrz kompletny przewodnik)

### "Pusta biblioteka"
- Sprawdź czy Jellyfin ma filmy
- Tunarr → Settings → Media Sources → Refresh

### "XMLTV pusty"
- Dodaj programowanie do kanału
- Włącz kanał (toggle ON)
- Poczekaj na regenerację XMLTV (~1 min)

## Ręczna konfiguracja
Jeśli automatyczny skrypt nie działa:
1. Tunarr → Channels → "Movies 24/7"
2. Zakładka "Programming"
3. "Add Programming"
4. Source: Jellyfin Movies
5. Type: Flex
6. Zapisz
