import requests
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class WeatherAlert:
    """Weather alert data model"""
    def __init__(self, alert_data: Dict[str, Any]):
        self.id = alert_data.get("id", "")
        self.event = alert_data.get("event", "")
        self.headline = alert_data.get("headline", "")
        self.description = alert_data.get("description", "")
        self.severity = alert_data.get("severity", "")
        self.urgency = alert_data.get("urgency", "")
        self.areas = alert_data.get("areaDesc", "")
        self.effective = alert_data.get("effective", "")
        self.expires = alert_data.get("expires", "")
        self.status = alert_data.get("status", "")
        self.message_type = alert_data.get("messageType", "")
        self.category = alert_data.get("category", "")
        self.certainty = alert_data.get("certainty", "")
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "event": self.event,
            "headline": self.headline,
            "description": self.description,
            "severity": self.severity,
            "urgency": self.urgency,
            "areas": self.areas,
            "effective": self.effective,
            "expires": self.expires,
            "status": self.status,
            "message_type": self.message_type,
            "category": self.category,
            "certainty": self.certainty
        }

class WeatherAlertsService:
    """Service for fetching weather alerts from National Weather Service API"""
    
    def __init__(self):
        self.base_url = "https://api.weather.gov"
        self.timeout = 10
        
    def get_alerts_for_location(self, lat: float, lon: float, radius: int = 50) -> List[WeatherAlert]:
        """
        Get weather alerts for a specific location
        
        Args:
            lat: Latitude
            lon: Longitude
            radius: Search radius in miles (default: 50)
            
        Returns:
            List of WeatherAlert objects
        """
        try:
            # Use the point parameter to get alerts for specific coordinates
            url = f"{self.base_url}/alerts/active"
            params = {
                "point": f"{lat},{lon}",
                "status": "actual"  # Only active alerts
            }
            
            logger.info(f"Fetching weather alerts for coordinates: {lat}, {lon}")
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                alerts = []
                
                if "features" in data:
                    for feature in data["features"]:
                        if "properties" in feature:
                            alert = WeatherAlert(feature["properties"])
                            alerts.append(alert)
                
                logger.info(f"Found {len(alerts)} weather alerts for location")
                return alerts
            else:
                logger.error(f"Weather alerts API request failed with status code {response.status_code}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error("Weather alerts API request timed out")
            return []
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to weather alerts API")
            return []
        except Exception as e:
            logger.error(f"Error fetching weather alerts: {str(e)}")
            return []
    
    def get_alerts_by_region(self, region: str = "conus") -> List[WeatherAlert]:
        """
        Get weather alerts for a specific region
        
        Args:
            region: Region code (e.g., 'conus' for continental US)
            
        Returns:
            List of WeatherAlert objects
        """
        try:
            url = f"{self.base_url}/alerts/active"
            params = {
                "region": region,
                "status": "actual"
            }
            
            logger.info(f"Fetching weather alerts for region: {region}")
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                alerts = []
                
                if "features" in data:
                    for feature in data["features"]:
                        if "properties" in feature:
                            alert = WeatherAlert(feature["properties"])
                            alerts.append(alert)
                
                logger.info(f"Found {len(alerts)} weather alerts for region {region}")
                return alerts
            else:
                logger.error(f"Weather alerts API request failed with status code {response.status_code}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error("Weather alerts API request timed out")
            return []
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to weather alerts API")
            return []
        except Exception as e:
            logger.error(f"Error fetching weather alerts: {str(e)}")
            return []
    
    def get_alerts_by_event_type(self, event_type: str) -> List[WeatherAlert]:
        """
        Get weather alerts for a specific event type
        
        Args:
            event_type: Type of weather event (e.g., 'Severe Thunderstorm Warning')
            
        Returns:
            List of WeatherAlert objects
        """
        try:
            url = f"{self.base_url}/alerts/active"
            params = {
                "event": event_type,
                "status": "actual"
            }
            
            logger.info(f"Fetching weather alerts for event type: {event_type}")
            response = requests.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                alerts = []
                
                if "features" in data:
                    for feature in data["features"]:
                        if "properties" in feature:
                            alert = WeatherAlert(feature["properties"])
                            alerts.append(alert)
                
                logger.info(f"Found {len(alerts)} weather alerts for event type {event_type}")
                return alerts
            else:
                logger.error(f"Weather alerts API request failed with status code {response.status_code}")
                return []
                
        except requests.exceptions.Timeout:
            logger.error("Weather alerts API request timed out")
            return []
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to weather alerts API")
            return []
        except Exception as e:
            logger.error(f"Error fetching weather alerts: {str(e)}")
            return []
    
    def test_api_connection(self) -> bool:
        """
        Test the connection to the weather alerts API
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            url = f"{self.base_url}/alerts/active"
            params = {"status": "actual"}
            
            response = requests.get(url, params=params, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Weather alerts API connection test failed: {str(e)}")
            return False

# Create a global instance
weather_alerts_service = WeatherAlertsService() 