import requests
from .base import DataSourceBase

class NASAPowerSource(DataSourceBase):
    def fetch(self, location, disaster_type):
        lat, lon = location
        url = (
            f"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,WS2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"
            f"&community=RE&longitude={lon}&latitude={lat}&format=JSON&start=20230101&end=20230102"
        )
        resp = requests.get(url)
        if resp.status_code != 200:
            return {}
        data = resp.json()
        # Get the most recent day
        try:
            daily = list(data['properties']['parameter']['T2M'].items())[0]
            temp = daily[1]
            wind = list(data['properties']['parameter']['WS2M'].values())[0]
            precip = list(data['properties']['parameter']['PRECTOTCORR'].values())[0]
            solar = list(data['properties']['parameter']['ALLSKY_SFC_SW_DWN'].values())[0]
        except Exception:
            return {}
        return {
            'nasa_temperature': temp,
            'nasa_wind_speed': wind,
            'nasa_precipitation': precip,
            'nasa_solar_radiation': solar
        } 