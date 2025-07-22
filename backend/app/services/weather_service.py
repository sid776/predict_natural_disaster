import requests
import os
from typing import Optional, Dict, Any
from app.models.schemas import WeatherData, WeatherMain, WeatherWind, WeatherClouds, WeatherSys, WeatherCondition, WeatherCoord
from app.utils.config import settings
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API"""
    
    def __init__(self):
        self.api_key = settings.openweathermap_api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_weather_data(self, lat: float, lon: float) -> WeatherData:
        """
        Get current weather data for given coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            WeatherData object with current weather information
        """
        if not self.api_key or self.api_key == "your_openweathermap_api_key_here":
            logger.warning("OpenWeatherMap API key not configured, using mock data")
            return self._get_mock_weather_data(lat, lon)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            logger.info(f"Fetching weather data for coordinates: {lat}, {lon}")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_weather_data(data)
            elif response.status_code == 401:
                logger.error("Invalid OpenWeatherMap API key")
                return self._get_mock_weather_data(lat, lon)
            elif response.status_code == 404:
                logger.error("Location not found")
                return self._get_mock_weather_data(lat, lon)
            else:
                logger.error(f"Weather API request failed with status code {response.status_code}")
                return self._get_mock_weather_data(lat, lon)
                
        except requests.exceptions.Timeout:
            logger.error("Weather API request timed out")
            return self._get_mock_weather_data(lat, lon)
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to weather API")
            return self._get_mock_weather_data(lat, lon)
        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return self._get_mock_weather_data(lat, lon)
    
    def _parse_weather_data(self, data: Dict[str, Any]) -> WeatherData:
        """Parse raw weather API response into WeatherData model"""
        try:
            # Handle rain data (might not be present)
            rain_data = None
            if "rain" in data:
                rain_data = {"h1": data["rain"].get("1h", 0)}
            
            weather_data = WeatherData(
                main=WeatherMain(
                    temp=data["main"]["temp"] + 273.15,  # Convert to Kelvin
                    humidity=data["main"]["humidity"],
                    pressure=data["main"]["pressure"]
                ),
                wind=WeatherWind(
                    speed=data["wind"]["speed"],
                    deg=data["wind"]["deg"]
                ),
                clouds=WeatherClouds(
                    all=data["clouds"]["all"]
                ),
                rain=rain_data,
                sys=WeatherSys(
                    sunrise=data["sys"]["sunrise"],
                    sunset=data["sys"]["sunset"]
                ),
                weather=[
                    WeatherCondition(
                        id=w["id"],
                        main=w["main"],
                        description=w["description"],
                        icon=w["icon"]
                    ) for w in data["weather"]
                ],
                visibility=data.get("visibility", 10000),
                coord=WeatherCoord(
                    lat=data["coord"]["lat"],
                    lon=data["coord"]["lon"]
                ),
                mock_data=False
            )
            return weather_data
            
        except KeyError as e:
            logger.error(f"Missing key in weather data: {e}")
            return self._get_mock_weather_data(
                data.get("coord", {}).get("lat", 40.7128),
                data.get("coord", {}).get("lon", -74.0060)
            )
    
    def _get_mock_weather_data(self, lat: float, lon: float) -> WeatherData:
        """Return mock weather data for testing when API is not available"""
        logger.info("Using mock weather data")
        
        return WeatherData(
            main=WeatherMain(
                temp=293.15,  # 20°C in Kelvin
                humidity=65,
                pressure=1013
            ),
            wind=WeatherWind(
                speed=5.5,
                deg=180
            ),
            clouds=WeatherClouds(
                all=40
            ),
            rain=None,
            sys=WeatherSys(
                sunrise=1622520000,
                sunset=1622574000
            ),
            weather=[
                WeatherCondition(
                    id=800,
                    main="Clear",
                    description="clear sky",
                    icon="01d"
                )
            ],
            visibility=10000,
            coord=WeatherCoord(lat=lat, lon=lon),
            mock_data=True
        )
    
    def test_api_connection(self) -> bool:
        """Test the OpenWeatherMap API connection"""
        if not self.api_key or self.api_key == "your_openweathermap_api_key_here":
            logger.warning("OpenWeatherMap API key not configured")
            return False
        
        try:
            # Test with New York City coordinates
            test_lat, test_lon = 40.7128, -74.0060
            url = f"{self.base_url}/weather"
            params = {
                "lat": test_lat,
                "lon": test_lon,
                "appid": self.api_key,
                "units": "metric"
            }
            
            logger.info("Testing OpenWeatherMap API connection")
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                logger.info("OpenWeatherMap API connection successful")
                return True
            else:
                logger.error(f"OpenWeatherMap API test failed with status code: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"OpenWeatherMap API test error: {str(e)}")
            return False

# Create singleton instance
weather_service = WeatherService() 