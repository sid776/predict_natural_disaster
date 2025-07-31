import requests
from .base import DataSourceBase

class USGSEarthquakeSource(DataSourceBase):
    def fetch(self, location, disaster_type):
        # Only fetch if disaster_type is earthquake
        if disaster_type != 'earthquake':
            return {}
        lat, lon = location
        url = (
            f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson"
            f"&latitude={lat}&longitude={lon}&maxradiuskm=100&limit=1&orderby=time"
        )
        resp = requests.get(url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        if not data['features']:
            return {}
        quake = data['features'][0]['properties']
        return {
            'magnitude': quake.get('mag', 0),
            'depth': quake.get('depth', 0),
            'time': quake.get('time', 0)
        } 