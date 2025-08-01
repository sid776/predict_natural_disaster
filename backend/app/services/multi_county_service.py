import asyncio
import math
import random
from typing import List, Dict, Optional, Tuple
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from ..models.schemas import (
    PredictionResponse, WeatherData, CountyInfo, CountyPrediction, 
    DisasterProgression, MultiCountyPredictionResponse
)
from .prediction_service import PredictionService
from .weather_service import WeatherService
from .geocoding_service import GeocodingService


class MultiCountyService:
    def __init__(self):
        self.prediction_service = PredictionService()
        self.weather_service = WeatherService()
        self.geocoding_service = GeocodingService()
        self.geolocator = Nominatim(user_agent="disaster_prediction_app")

    async def get_nearby_counties(self, location: str, radius_miles: float = 5.0) -> List[CountyInfo]:
        """Get counties within the specified radius of the location using dynamic discovery."""
        try:
            # Get coordinates for the main location
            coords = self.geocoding_service.get_coordinates(location)
            if not coords:
                return []

            main_lat, main_lon = coords
            
            # Use dynamic discovery for all locations
            counties = await self._discover_nearby_locations(main_lat, main_lon, radius_miles)
            
            return counties
            
        except Exception as e:
            print(f"Error getting nearby counties: {e}")
            return []

    async def _discover_nearby_locations(self, lat: float, lon: float, radius_miles: float) -> List[CountyInfo]:
        """Dynamically discover nearby locations using OpenWeatherMap and geocoding."""
        try:
            counties = []
            
            # Generate points in a grid around the main location
            grid_points = self._generate_grid_points(lat, lon, radius_miles)
            
            for point_lat, point_lon in grid_points:
                try:
                    # Get location name for this point
                    location_name = self._get_location_name(point_lat, point_lon)
                    
                    if location_name and location_name != "Unknown":
                        distance = geodesic((lat, lon), (point_lat, point_lon)).miles
                        
                        # Get weather data to determine if it's a populated area
                        weather_data = self._get_weather_for_point(point_lat, point_lon)
                        
                        if weather_data and self._is_populated_area(weather_data):
                            # Estimate population based on area type and weather data
                            estimated_population = self._estimate_population(weather_data, distance)
                            
                            counties.append(CountyInfo(
                                name=location_name,
                                coordinates={"lat": point_lat, "lon": point_lon},
                                distance_miles=distance,
                                population=estimated_population
                            ))
                            
                            # Limit to 5 counties to avoid overwhelming the UI
                            if len(counties) >= 5:
                                break
                                
                except Exception as e:
                    print(f"Error processing point ({point_lat}, {point_lon}): {e}")
                    continue
            
            # If no counties found due to geocoding issues, create fallback counties
            if not counties:
                print("No counties found via geocoding, creating fallback counties...")
                counties = self._create_fallback_counties(lat, lon, radius_miles)
            
            return counties
            
        except Exception as e:
            print(f"Error in dynamic discovery: {e}")
            # Return fallback counties if everything fails
            return self._create_fallback_counties(lat, lon, radius_miles)

    def _create_fallback_counties(self, lat: float, lon: float, radius_miles: float) -> List[CountyInfo]:
        """Create fallback counties when geocoding fails."""
        counties = []
        
        # Create 5 fallback counties at different distances
        distances = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        for i, distance in enumerate(distances):
            # Calculate coordinates at this distance
            angle = (i * 72) * (math.pi / 180)  # Spread counties around in a circle
            dlat = distance / 69.0  # Convert miles to degrees
            dlon = distance / (69.0 * math.cos(math.radians(lat)))
            
            point_lat = lat + dlat * math.cos(angle)
            point_lon = lon + dlon * math.sin(angle)
            
            # Generate fallback name
            location_name = self._generate_fallback_location_name(point_lat, point_lon)
            
            counties.append(CountyInfo(
                name=location_name,
                coordinates={"lat": point_lat, "lon": point_lon},
                distance_miles=distance,
                population=self._estimate_population({}, distance)
            ))
        
        return counties

    def _generate_grid_points(self, lat: float, lon: float, radius_miles: float) -> List[Tuple[float, float]]:
        """Generate grid points around the main location."""
        points = []
        # Convert miles to degrees (approximate)
        lat_degree_range = radius_miles / 69.0  # 1 degree latitude ≈ 69 miles
        lon_degree_range = radius_miles / (69.0 * math.cos(math.radians(lat)))
        
        # Generate a smaller 5x5 grid to reduce API calls
        for i in range(-2, 3):
            for j in range(-2, 3):
                point_lat = lat + (i * lat_degree_range / 2)
                point_lon = lon + (j * lon_degree_range / 2)
                
                # Ensure coordinates are valid
                if -90 <= point_lat <= 90 and -180 <= point_lon <= 180:
                    points.append((point_lat, point_lon))
        
        return points

    def _get_location_name(self, lat: float, lon: float) -> str:
        """Get location name for coordinates using reverse geocoding."""
        try:
            # Add timeout and retry mechanism
            location = self.geolocator.reverse(f"{lat}, {lon}", timeout=5)
            if location:
                # Extract county or city name from address
                address = location.raw.get('address', {})
                county = address.get('county') or address.get('city') or address.get('town') or address.get('municipality')
                
                # If we have a county name, use it
                if county and county != "Unknown":
                    return county
                
                # Fallback to display name
                display_name = location.raw.get('display_name', '')
                if display_name:
                    # Extract the first part of the display name (usually city/town)
                    parts = display_name.split(',')
                    if len(parts) > 0:
                        return parts[0].strip()
                
                return "Unknown"
            return "Unknown"
        except Exception as e:
            # If geocoding fails, generate a fallback name based on coordinates
            print(f"Geocoding failed for ({lat}, {lon}): {e}")
            return self._generate_fallback_location_name(lat, lon)

    def _generate_fallback_location_name(self, lat: float, lon: float) -> str:
        """Generate a fallback location name when geocoding fails."""
        try:
            # Create a simple name based on coordinates
            # Round to 2 decimal places for readability
            lat_rounded = round(lat, 2)
            lon_rounded = round(lon, 2)
            
            # Determine region based on coordinates
            if lat > 40:
                region = "Northern"
            elif lat > 30:
                region = "Central"
            else:
                region = "Southern"
                
            if lon > -100:
                region += " Eastern"
            elif lon > -120:
                region += " Central"
            else:
                region += " Western"
            
            return f"{region} Area ({lat_rounded}, {lon_rounded})"
            
        except Exception:
            return "Unknown Location"

    def _get_weather_for_point(self, lat: float, lon: float) -> Optional[Dict]:
        """Get weather data for a specific point using OpenWeatherMap."""
        try:
            weather_data = self.weather_service.get_weather_data(lat, lon)
            return weather_data.dict() if weather_data else None
        except Exception:
            return None

    def _is_populated_area(self, weather_data: Dict) -> bool:
        """Determine if an area is populated based on weather data."""
        try:
            # Check if we have valid weather data (indicates populated area)
            if not weather_data:
                return False
            
            # Additional checks could be added here based on weather patterns
            # For now, assume any area with weather data is populated
            return True
        except Exception:
            return False

    def _estimate_population(self, weather_data: Dict, distance: float) -> int:
        """Estimate population based on distance and weather data."""
        try:
            # Simple estimation based on distance from center
            # Closer areas likely have higher population density
            base_population = 50000  # Base population for nearby areas
            
            # Adjust based on distance
            if distance <= 2:
                multiplier = 2.0  # High density
            elif distance <= 3:
                multiplier = 1.5  # Medium density
            else:
                multiplier = 1.0  # Lower density
            
            # Add some randomness to make it more realistic
            random_factor = random.uniform(0.8, 1.2)
            
            return int(base_population * multiplier * random_factor)
        except Exception:
            return 50000  # Default fallback

    async def predict_disaster_progression(
        self, 
        location: str, 
        disaster_type: str,
        model: str = "quantum",
        data_source: str = "openweathermap"
    ) -> DisasterProgression:
        """Predict disaster progression for nearby counties."""
        try:
            # Get main location prediction
            main_prediction = await self._get_main_prediction(location, disaster_type, model, data_source)
            
            # Get nearby counties
            counties = await self.get_nearby_counties(location, radius_miles=5.0)
            
            if not counties:
                raise ValueError("No nearby counties found")
            
            # Calculate progression parameters
            progression_params = self._calculate_progression_parameters(disaster_type, main_prediction)
            
            # Predict impact for each county
            county_predictions = []
            for county in counties:
                county_prediction = await self._predict_county_impact(
                    county, disaster_type, progression_params, model, data_source
                )
                county_predictions.append(county_prediction)
            
            # Sort by impact time
            county_predictions.sort(key=lambda x: x.predicted_impact_time_hours)
            
            return DisasterProgression(
                direction_degrees=progression_params["direction"],
                speed_mph=progression_params["speed"],
                estimated_duration_hours=progression_params["duration"],
                affected_counties=county_predictions
            )
            
        except Exception as e:
            raise ValueError(f"Failed to predict disaster progression: {str(e)}")

    async def _get_main_prediction(self, location: str, disaster_type: str, model: str, data_source: str) -> PredictionResponse:
        """Get prediction for the main location."""
        from ..models.schemas import PredictionRequest, DisasterType, PredictionModel, DataSource
        
        request = PredictionRequest(
            location=location,
            disaster_type=DisasterType(disaster_type),
            model=PredictionModel(model),
            data_source=DataSource(data_source) if data_source != "openweathermap" else DataSource.openweathermap
        )
        
        return self.prediction_service.predict(request)

    def _calculate_progression_parameters(self, disaster_type: str, main_prediction: PredictionResponse) -> Dict:
        """Calculate disaster progression parameters."""
        # Base parameters
        base_speed = {
            "tornado": 35.0,  # mph
            "wildfire": 8.0,   # mph
            "flood": 2.0,      # mph
            "earthquake": 0.0   # instantaneous
        }
        
        base_duration = {
            "tornado": 2.0,    # hours
            "wildfire": 24.0,   # hours
            "flood": 48.0,      # hours
            "earthquake": 0.1   # hours
        }
        
        # Adjust based on prediction probability
        probability_factor = main_prediction.probability
        speed = base_speed.get(disaster_type, 20.0) * (0.5 + probability_factor)
        duration = base_duration.get(disaster_type, 12.0) * (0.8 + probability_factor * 0.4)
        
        # Random direction (in practice, this would be based on weather patterns)
        direction = random.uniform(0, 360)
        
        return {
            "speed": speed,
            "direction": direction,
            "duration": duration
        }

    async def _predict_county_impact(
        self, 
        county: CountyInfo, 
        disaster_type: str, 
        progression: Dict,
        model: str,
        data_source: str
    ) -> CountyPrediction:
        """Predict impact for a specific county."""
        try:
            # Get weather data for the county
            weather_data = self._get_weather_for_point(county.coordinates["lat"], county.coordinates["lon"])
            
            # Calculate impact time based on distance and speed
            speed_mph = progression["speed"]
            if speed_mph > 0:
                impact_time = county.distance_miles / speed_mph
            else:
                impact_time = 0.0
            
            # Calculate risk level
            risk_level = self._calculate_risk_level(county.distance_miles, weather_data, disaster_type)
            
            # Calculate probability based on distance and weather
            base_probability = 0.8 - (county.distance_miles * 0.1)  # Decreases with distance
            weather_factor = self._get_weather_risk_factor(weather_data, disaster_type)
            probability = min(0.95, max(0.05, base_probability * weather_factor))
            
            # Determine evacuation priority
            evacuation_priority = self._determine_evacuation_priority(impact_time, risk_level, county.population)
            
            return CountyPrediction(
                county=county,
                predicted_impact_time_hours=impact_time,
                risk_level=risk_level,
                probability=probability,
                weather_conditions=weather_data or {},
                evacuation_priority=evacuation_priority
            )
            
        except Exception as e:
            print(f"Error predicting county impact: {e}")
            # Return a basic prediction
            return CountyPrediction(
                county=county,
                predicted_impact_time_hours=county.distance_miles / 20.0,
                risk_level="Medium",
                probability=0.5,
                weather_conditions={},
                evacuation_priority="Monitor"
            )

    def _calculate_risk_level(self, distance: float, weather_data: Optional[Dict], disaster_type: str) -> str:
        """Calculate risk level based on distance and weather conditions."""
        if distance <= 1.0:
            return "Critical"
        elif distance <= 2.0:
            return "High"
        elif distance <= 3.0:
            return "Medium"
        else:
            return "Low"

    def _get_weather_risk_factor(self, weather_data: Optional[Dict], disaster_type: str) -> float:
        """Get weather-based risk factor."""
        if not weather_data:
            return 1.0
        
        try:
            # Adjust risk based on weather conditions for different disaster types
            if disaster_type == "tornado":
                wind_speed = weather_data.get("wind", {}).get("speed", 0)
                return 1.0 + (wind_speed / 50.0)  # Higher wind = higher risk
            elif disaster_type == "wildfire":
                humidity = weather_data.get("main", {}).get("humidity", 50)
                return 1.0 + ((100 - humidity) / 100.0)  # Lower humidity = higher risk
            elif disaster_type == "flood":
                # Check for rain data
                return 1.2  # Slightly higher risk for flood
            else:
                return 1.0
        except Exception:
            return 1.0

    def _determine_evacuation_priority(self, impact_time: float, risk_level: str, population: Optional[int]) -> str:
        """Determine evacuation priority based on impact time and risk."""
        if impact_time <= 1.0 or risk_level == "Critical":
            return "Immediate"
        elif impact_time <= 3.0 or risk_level == "High":
            return "Prepare"
        else:
            return "Monitor"

    async def get_evacuation_recommendations(self, progression: DisasterProgression) -> Dict:
        """Get evacuation recommendations based on progression data."""
        immediate = []
        prepare = []
        monitor = []
        
        for county_prediction in progression.affected_counties:
            county_info = {
                "county": county_prediction.county.name,
                "time_remaining": f"{county_prediction.predicted_impact_time_hours:.1f}h",
                "risk_level": county_prediction.risk_level,
                "population": county_prediction.county.population
            }
            
            if county_prediction.evacuation_priority == "Immediate":
                immediate.append(county_info)
            elif county_prediction.evacuation_priority == "Prepare":
                prepare.append(county_info)
            else:
                monitor.append(county_info)
        
        return {
            "immediate_evacuation": immediate,
            "prepare_to_evacuate": prepare,
            "monitor_situation": monitor
        } 