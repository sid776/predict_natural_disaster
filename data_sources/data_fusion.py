from .openweathermap_source import OpenWeatherMapSource
from .usgs_source import USGSEarthquakeSource
from .nasa_power_source import NASAPowerSource

class DataFusion:
    def __init__(self, owm_api_key):
        self.owm = OpenWeatherMapSource(owm_api_key)
        self.usgs = USGSEarthquakeSource()
        self.nasa = NASAPowerSource()

    def fetch_all(self, location, disaster_type):
        data = {}
        data.update(self.owm.fetch(location, disaster_type))
        data.update(self.usgs.fetch(location, disaster_type))
        data.update(self.nasa.fetch(location, disaster_type))
        return data 