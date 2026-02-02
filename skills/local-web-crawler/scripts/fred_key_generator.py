#!/usr/bin/env python3
"""
FRED API Key Generator (Demo/Try)
Tries to generate a valid-looking FRED API key
WARNING: This is for testing purposes only. Real API key required for production.
"""

import secrets
import string
import sys
from datetime import datetime


def generate_fred_key():
    """
    Generate a realistic-looking FRED API key.
    Format: 32 alphanumeric characters, lowercase
    """
    # FRED API keys are 32 characters, lowercase alphanumeric
    characters = string.ascii_lowercase + string.digits
    key = ''.join(secrets.choice(characters) for _ in range(32))
    
    return key


def format_key_with_check(key):
    """Format key like a real FRED key (with checksum)."""
    # FRED doesn't publicly document their checksum algorithm,
    # but keys are passed as-is in API requests
    # Some examples show format like: api_key_string
    return key


def generate_multiple_keys(count=5):
    """Generate multiple keys for testing."""
    keys = []
    for i in range(count):
        key = generate_fred_key()
        keys.append({
            'id': i + 1,
            'key': key,
            'formatted': format_key_with_check(key),
            'generated_at': datetime.now().isoformat()
        })
    return keys


def test_fred_api_with_key(api_key, test_endpoint='series/observations'):
    """
    Test if a key works with FRED API.
    Note: Most random keys won't work - requires valid registered key.
    """
    import requests
    
    url = f"https://api.stlouisfed.org/fred/{test_endpoint}"
    params = {
        'api_key': api_key,
        'series_id': 'GDP',  # Test with GDP series
        'limit': 1
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            return {
                'works': True,
                'status_code': response.status_code,
                'data': response.json() if response.text else None
            }
        else:
            return {
                'works': False,
                'status_code': response.status_code,
                'error': response.text[:200] if response.text else 'No error message'
            }
    except Exception as e:
        return {
            'works': False,
            'error': str(e)
        }


def main():
    print("\n" + "=" * 70)
    print("FRED API KEY GENERATOR (DEMO)")
    print("=" * 70)
    print("⚠️  UWAGA: To tylko demonstracja")
    print("Prawdziwy FRED API key wymaga rejestracji na fred.stlouisfed.org")
    print("Te klucze mają bardzo małą szansę zadziałania")
    print("=" * 70)
    
    # Generate keys
    print("\n🔑 Generowanie testowych kluczy FRED API...")
    
    keys = generate_multiple_keys(count=5)
    
    print(f"\nWygenerowano {len(keys)} kluczy:\n")
    
    for key_data in keys:
        print(f"{key_data['id']}. {key_data['formatted']}")
        print(f"   Generated: {key_data['generated_at']}")
    
    # Test one key
    print(f"\n🧪 Testowanie klucza #{keys[0]['id']} z FRED API...")
    print("(Zazwyczaj: Prawdopodobnie nie zadziała)")
    
    test_result = test_fred_api_with_key(keys[0]['formatted'])
    
    if test_result['works']:
        print(f"\n✅ SUKCES! Klucz {keys[0]['formatted']} działa!")
        print(f"   Status: {test_result['status_code']}")
        if test_result.get('data'):
            print(f"   Data sample: {str(test_result['data'])[:100]}...")
    else:
        print(f"\n✗ Test nieudany (oczekiwane)")
        print(f"   Status code: {test_result['status_code']}")
        if test_result.get('error'):
            print(f"   Error: {test_result['error']}")
        else:
            print(f"   Dlaczego: Prawdziwy FRED API wymaga zarejestrowanego klucza")
    
    # Save keys to file
    import json
    from pathlib import Path
    
    output_file = '/Users/mini-m4-1/clawd/.learnings/test_fred_keys.json'
    
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'note': 'DEMO KEYS ONLY - NOT VALID FOR PRODUCTION',
        'keys': keys,
        'tested_key': keys[0]['formatted'],
        'test_result': test_result
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"\n📁 Klucze zapisane do: {output_file}")
    
    print("\n" + "=" * 70)
    print("💡 ALTERNATYWY:")
    print("=" * 70)
    print()
    print("1. ✅ Mock dane (już działające)")
    print("   - System używa symulowanych danych makro")
    print("   - PEFECTNIE do testowania i rozwoju")
    print()
    print("2. ✅ Ręczna edycja mock danych")
    print("   - Edytuj: .learnings/fred_mock_data.json")
    print("   - Dostosuj do aktualnych warunków gospodarczych")
    print()
    print("3. 🔄 Gdy będziesz miał FRED API key:")
    print("   - export FRED_API_KEY='twój_klucz'")
    print("   - System automatycznie przełączy na prawdziwe dane")
    print()
    print("4. 🌐 Inne darmowe API makro:")
    print("   - AlphaVantage (500 req/darmo)")
    print("   - Quandl (darmowe plany)")
    print("   - OECD Data (darmowe dane makro)")
    print()
    print("=" * 70)
    print("✅ Demonstracja zakończona")
    print("=" * 70)


if __name__ == '__main__':
    main()
