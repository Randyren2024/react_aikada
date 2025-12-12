import os
import json
import urllib.request
import urllib.parse
import urllib.error

PROVIDER = os.getenv('GEOCODING_PROVIDER', 'nominatim').lower()
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN', '')

def _nominatim_reverse(lat, lng):
    params = {
        'format': 'json',
        'lat': str(lat),
        'lon': str(lng),
        'zoom': '16',
        'addressdetails': '1'
    }
    url = 'https://nominatim.openstreetmap.org/reverse?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'aikada/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read()
            data = json.loads(body.decode('utf-8'))
            return data.get('display_name') or ''
    except Exception:
        return ''

def _mapbox_reverse(lat, lng):
    if not MAPBOX_TOKEN:
        return ''
    coords = f"{lng},{lat}"
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{urllib.parse.quote(coords)}.json?access_token={MAPBOX_TOKEN}&limit=1&language=zh"
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            body = resp.read()
            data = json.loads(body.decode('utf-8'))
            features = data.get('features') or []
            if features:
                return features[0].get('place_name') or ''
            return ''
    except Exception:
        return ''

def reverse_geocode(lat, lng):
    if PROVIDER == 'mapbox':
        return _mapbox_reverse(lat, lng)
    return _nominatim_reverse(lat, lng)

def clamp_location(loc):
    try:
        lat = float(loc.get('latitude'))
        lng = float(loc.get('longitude'))
        acc = loc.get('accuracy')
        acc = float(acc) if acc is not None else None
    except Exception:
        return None
    if not (-90.0 <= lat <= 90.0 and -180.0 <= lng <= 180.0):
        return None
    if acc is not None and (acc < 0 or acc > 10000):
        acc = None
    address = loc.get('address')
    return {
        'latitude': round(lat, 6),
        'longitude': round(lng, 6),
        'accuracy': acc,
        'address': address if isinstance(address, str) else None
    }
