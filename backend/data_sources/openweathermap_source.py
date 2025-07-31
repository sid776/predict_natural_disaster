import requests
from .base import DataSourceBase

class OpenWeatherMapSource(DataSourceBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch(self, location, disaster_type):
        # For simplicity, location is a tuple (lat, lon)
        lat, lon = location
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}&units=metric"
        resp = requests.get(url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        return {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind'].get('deg', 0)
        } 