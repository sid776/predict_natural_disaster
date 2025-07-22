from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from typing import Optional, Tuple
from app.models.schemas import GeocodingResponse
import logging
import time

logger = logging.getLogger(__name__)

class GeocodingService:
    """Service for geocoding locations using Nominatim with fallback mechanisms"""
    
    def __init__(self):
        # Increase timeout and add retry mechanism
        self.geolocator = Nominatim(
            user_agent="natural_disaster_predictor",
            timeout=10  # Increased from default 1 second
        )
        
        # Fallback coordinates for common cities
        self.fallback_coordinates = {
            "new york": (40.7128, -74.0060),
            "new york, ny": (40.7128, -74.0060),
            "los angeles": (34.0522, -118.2437),
            "los angeles, ca": (34.0522, -118.2437),
            "chicago": (41.8781, -87.6298),
            "chicago, il": (41.8781, -87.6298),
            "houston": (29.7604, -95.3698),
            "houston, tx": (29.7604, -95.3698),
            "phoenix": (33.4484, -112.0740),
            "phoenix, az": (33.4484, -112.0740),
            "philadelphia": (39.9526, -75.1652),
            "philadelphia, pa": (39.9526, -75.1652),
            "san antonio": (29.4241, -98.4936),
            "san antonio, tx": (29.4241, -98.4936),
            "san diego": (32.7157, -117.1611),
            "san diego, ca": (32.7157, -117.1611),
            "dallas": (32.7767, -96.7970),
            "dallas, tx": (32.7767, -96.7970),
            "san jose": (37.3382, -121.8863),
            "san jose, ca": (37.3382, -121.8863),
            "austin": (30.2672, -97.7431),
            "austin, tx": (30.2672, -97.7431),
            "jacksonville": (30.3322, -81.6557),
            "jacksonville, fl": (30.3322, -81.6557),
            "fort worth": (32.7555, -97.3308),
            "fort worth, tx": (32.7555, -97.3308),
            "columbus": (39.9612, -82.9988),
            "columbus, oh": (39.9612, -82.9988),
            "charlotte": (35.2271, -80.8431),
            "charlotte, nc": (35.2271, -80.8431),
            "san francisco": (37.7749, -122.4194),
            "san francisco, ca": (37.7749, -122.4194),
            "indianapolis": (39.7684, -86.1581),
            "indianapolis, in": (39.7684, -86.1581),
            "seattle": (47.6062, -122.3321),
            "seattle, wa": (47.6062, -122.3321),
            "denver": (39.7392, -104.9903),
            "denver, co": (39.7392, -104.9903),
            "washington": (38.9072, -77.0369),
            "washington, dc": (38.9072, -77.0369),
            "boston": (42.3601, -71.0589),
            "boston, ma": (42.3601, -71.0589),
            "el paso": (31.7619, -106.4850),
            "el paso, tx": (31.7619, -106.4850),
            "nashville": (36.1627, -86.7816),
            "nashville, tn": (36.1627, -86.7816),
            "detroit": (42.3314, -83.0458),
            "detroit, mi": (42.3314, -83.0458),
            "oklahoma city": (35.4676, -97.5164),
            "oklahoma city, ok": (35.4676, -97.5164),
            "portland": (45.5152, -122.6784),
            "portland, or": (45.5152, -122.6784),
            "las vegas": (36.1699, -115.1398),
            "las vegas, nv": (36.1699, -115.1398),
            "memphis": (35.1495, -90.0490),
            "memphis, tn": (35.1495, -90.0490),
            "louisville": (38.2527, -85.7585),
            "louisville, ky": (38.2527, -85.7585),
            "baltimore": (39.2904, -76.6122),
            "baltimore, md": (39.2904, -76.6122),
            "milwaukee": (43.0389, -87.9065),
            "milwaukee, wi": (43.0389, -87.9065),
            "albuquerque": (35.0844, -106.6504),
            "albuquerque, nm": (35.0844, -106.6504),
            "tucson": (32.2226, -110.9747),
            "tucson, az": (32.2226, -110.9747),
            "fresno": (36.7378, -119.7871),
            "fresno, ca": (36.7378, -119.7871),
            "sacramento": (38.5816, -121.4944),
            "sacramento, ca": (38.5816, -121.4944),
            "atlanta": (33.7490, -84.3880),
            "atlanta, ga": (33.7490, -84.3880),
            "kansas city": (39.0997, -94.5786),
            "kansas city, mo": (39.0997, -94.5786),
            "long beach": (33.7701, -118.1937),
            "long beach, ca": (33.7701, -118.1937),
            "colorado springs": (38.8339, -104.8214),
            "colorado springs, co": (38.8339, -104.8214),
            "miami": (25.7617, -80.1918),
            "miami, fl": (25.7617, -80.1918),
            "raleigh": (35.7796, -78.6382),
            "raleigh, nc": (35.7796, -78.6382),
            "omaha": (41.2565, -95.9345),
            "omaha, ne": (41.2565, -95.9345),
            "minneapolis": (44.9778, -93.2650),
            "minneapolis, mn": (44.9778, -93.2650),
            "tulsa": (36.1540, -95.9928),
            "tulsa, ok": (36.1540, -95.9928),
            "cleveland": (41.4993, -81.6944),
            "cleveland, oh": (41.4993, -81.6944),
            "wichita": (37.6872, -97.3301),
            "wichita, ks": (37.6872, -97.3301),
            "arlington": (32.7357, -97.1081),
            "arlington, tx": (32.7357, -97.1081),
            "new orleans": (29.9511, -90.0715),
            "new orleans, la": (29.9511, -90.0715),
            "bakersfield": (35.3733, -119.0187),
            "bakersfield, ca": (35.3733, -119.0187),
            "tampa": (27.9506, -82.4572),
            "tampa, fl": (27.9506, -82.4572),
            "honolulu": (21.3099, -157.8581),
            "honolulu, hi": (21.3099, -157.8581),
            "anaheim": (33.8366, -117.9143),
            "anaheim, ca": (33.8366, -117.9143),
            "aurora": (39.7294, -104.8319),
            "aurora, co": (39.7294, -104.8319),
            "santa ana": (33.7455, -117.8677),
            "santa ana, ca": (33.7455, -117.8677),
            "corpus christi": (27.8006, -97.3964),
            "corpus christi, tx": (27.8006, -97.3964),
            "riverside": (33.9533, -117.3962),
            "riverside, ca": (33.9533, -117.3962),
            "lexington": (38.0406, -84.5037),
            "lexington, ky": (38.0406, -84.5037),
            "stockton": (37.9577, -121.2908),
            "stockton, ca": (37.9577, -121.2908),
            "henderson": (36.0395, -114.9817),
            "henderson, nv": (36.0395, -114.9817),
            "saint paul": (44.9537, -93.0900),
            "saint paul, mn": (44.9537, -93.0900),
            "st. louis": (38.6270, -90.1994),
            "st. louis, mo": (38.6270, -90.1994),
            "cincinnati": (39.1031, -84.5120),
            "cincinnati, oh": (39.1031, -84.5120),
            "pittsburgh": (40.4406, -79.9959),
            "pittsburgh, pa": (40.4406, -79.9959),
            "greensboro": (36.0726, -79.7920),
            "greensboro, nc": (36.0726, -79.7920),
            "anchorage": (61.2181, -149.9003),
            "anchorage, ak": (61.2181, -149.9003),
            "plano": (33.0198, -96.6989),
            "plano, tx": (33.0198, -96.6989),
            "orlando": (28.5383, -81.3792),
            "orlando, fl": (28.5383, -81.3792),
            "newark": (40.7357, -74.1724),
            "newark, nj": (40.7357, -74.1724),
            "durham": (35.9940, -78.8986),
            "durham, nc": (35.9940, -78.8986),
            "chula vista": (32.6401, -117.0842),
            "chula vista, ca": (32.6401, -117.0842),
            "toledo": (41.6528, -83.5379),
            "toledo, oh": (41.6528, -83.5379),
            "fort wayne": (41.0793, -85.1394),
            "fort wayne, in": (41.0793, -85.1394),
            "st. petersburg": (27.7731, -82.6400),
            "st. petersburg, fl": (27.7731, -82.6400),
            "laredo": (27.5064, -99.5075),
            "laredo, tx": (27.5064, -99.5075),
            "jersey city": (40.7178, -74.0431),
            "jersey city, nj": (40.7178, -74.0431),
            "chandler": (33.3062, -111.8413),
            "chandler, az": (33.3062, -111.8413),
            "madison": (43.0731, -89.4012),
            "madison, wi": (43.0731, -89.4012),
            "lubbock": (33.5779, -101.8552),
            "lubbock, tx": (33.5779, -101.8552),
            "scottsdale": (33.4942, -111.9261),
            "scottsdale, az": (33.4942, -111.9261),
            "reno": (39.5296, -119.8138),
            "reno, nv": (39.5296, -119.8138),
            "buffalo": (42.8864, -78.8784),
            "buffalo, ny": (42.8864, -78.8784),
            "gilbert": (33.3528, -111.7890),
            "gilbert, az": (33.3528, -111.7890),
            "glendale": (33.5387, -112.1860),
            "glendale, az": (33.5387, -112.1860),
            "north las vegas": (36.1989, -115.1175),
            "north las vegas, nv": (36.1989, -115.1175),
            "winston-salem": (36.0999, -80.2442),
            "winston-salem, nc": (36.0999, -80.2442),
            "chesapeake": (36.7682, -76.2875),
            "chesapeake, va": (36.7682, -76.2875),
            "norfolk": (36.8508, -76.2859),
            "norfolk, va": (36.8508, -76.2859),
            "fremont": (37.5485, -121.9886),
            "fremont, ca": (37.5485, -121.9886),
            "garland": (32.9126, -96.6389),
            "garland, tx": (32.9126, -96.6389),
            "irvine": (33.6846, -117.8265),
            "irvine, ca": (33.6846, -117.8265),
            "hialeah": (25.8576, -80.2781),
            "hialeah, fl": (25.8576, -80.2781),
            "richmond": (37.5407, -77.4360),
            "richmond, va": (37.5407, -77.4360),
            "boise": (43.6150, -116.2023),
            "boise, id": (43.6150, -116.2023),
            "spokane": (47.6588, -117.4260),
            "spokane, wa": (47.6588, -117.4260),
            "baton rouge": (30.4515, -91.1871),
            "baton rouge, la": (30.4515, -91.1871),
        }
        
    def _try_fallback_coordinates(self, location: str) -> Optional[Tuple[float, float]]:
        """Try to get coordinates from fallback dictionary"""
        location_lower = location.lower().strip()
        
        # Try exact match first
        if location_lower in self.fallback_coordinates:
            logger.info(f"Using fallback coordinates for {location}: {self.fallback_coordinates[location_lower]}")
            return self.fallback_coordinates[location_lower]
        
        # Try partial matches
        for key, coords in self.fallback_coordinates.items():
            if location_lower in key or key in location_lower:
                logger.info(f"Using fallback coordinates for {location} (partial match '{key}'): {coords}")
                return coords
        
        return None
        
    def get_coordinates(self, location: str, max_retries: int = 2) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a given location with retry mechanism and fallback
        
        Args:
            location: Location string (e.g., "New York, NY")
            max_retries: Maximum number of retry attempts
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        if not location or len(location.strip()) < 2:
            logger.warning(f"Invalid location provided: {location}")
            return None
            
        # Try fallback coordinates first for common cities
        fallback_coords = self._try_fallback_coordinates(location)
        if fallback_coords:
            return fallback_coords
        
        # Try Nominatim with retries
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Geocoding location: {location} (attempt {attempt + 1}/{max_retries + 1})")
                
                # Add USA suffix if not present to improve accuracy
                search_location = location
                if not location.lower().endswith(('usa', 'united states', 'us')):
                    search_location = f"{location}, USA"
                
                location_data = self.geolocator.geocode(search_location)
                
                if location_data:
                    coords = (location_data.latitude, location_data.longitude)
                    logger.info(f"Found coordinates for {location}: {coords}")
                    return coords
                else:
                    logger.warning(f"No coordinates found for location: {location}")
                    return None
                    
            except GeocoderTimedOut:
                logger.warning(f"Geocoding timed out for location: {location} (attempt {attempt + 1})")
                if attempt < max_retries:
                    time.sleep(1)  # Wait before retry
                    continue
                else:
                    logger.error(f"Geocoding failed after {max_retries + 1} attempts for location: {location}")
                    return None
            except GeocoderUnavailable:
                logger.error(f"Geocoding service unavailable for location: {location}")
                return None
            except Exception as e:
                logger.error(f"Error geocoding location {location}: {str(e)}")
                return None
        
        return None
    
    def get_location_info(self, location: str, max_retries: int = 2) -> Optional[GeocodingResponse]:
        """
        Get detailed location information including coordinates and display name
        
        Args:
            location: Location string (e.g., "New York, NY")
            max_retries: Maximum number of retry attempts
            
        Returns:
            GeocodingResponse object or None if not found
        """
        if not location or len(location.strip()) < 2:
            logger.warning(f"Invalid location provided: {location}")
            return None
            
        # Try fallback coordinates first
        fallback_coords = self._try_fallback_coordinates(location)
        if fallback_coords:
            response = GeocodingResponse(
                lat=fallback_coords[0],
                lon=fallback_coords[1],
                display_name=f"{location} (fallback coordinates)"
            )
            logger.info(f"Using fallback location info: {response.display_name}")
            return response
        
        # Try Nominatim with retries
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Getting location info for: {location} (attempt {attempt + 1}/{max_retries + 1})")
                
                # Add USA suffix if not present
                search_location = location
                if not location.lower().endswith(('usa', 'united states', 'us')):
                    search_location = f"{location}, USA"
                
                location_data = self.geolocator.geocode(search_location)
                
                if location_data:
                    response = GeocodingResponse(
                        lat=location_data.latitude,
                        lon=location_data.longitude,
                        display_name=location_data.address
                    )
                    logger.info(f"Found location info: {response.display_name}")
                    return response
                else:
                    logger.warning(f"No location info found for: {location}")
                    return None
                    
            except GeocoderTimedOut:
                logger.warning(f"Geocoding timed out for location: {location} (attempt {attempt + 1})")
                if attempt < max_retries:
                    time.sleep(1)  # Wait before retry
                    continue
                else:
                    logger.error(f"Geocoding failed after {max_retries + 1} attempts for location: {location}")
                    return None
            except GeocoderUnavailable:
                logger.error(f"Geocoding service unavailable for location: {location}")
                return None
            except Exception as e:
                logger.error(f"Error getting location info for {location}: {str(e)}")
                return None
        
        return None
    
    def validate_location(self, location: str) -> bool:
        """
        Validate if a location string is valid and can be geocoded
        
        Args:
            location: Location string to validate
            
        Returns:
            True if location is valid, False otherwise
        """
        if not location or len(location.strip()) < 2:
            return False
        
        # Basic validation - should contain letters and possibly commas
        if not any(c.isalpha() for c in location):
            return False
        
        # Check fallback coordinates first
        if self._try_fallback_coordinates(location):
            return True
        
        # Try to get coordinates as a test
        coords = self.get_coordinates(location)
        return coords is not None
    
    def test_service(self) -> bool:
        """Test the geocoding service with a known location"""
        try:
            test_location = "New York, NY"
            coords = self.get_coordinates(test_location)
            
            if coords:
                logger.info("Geocoding service test successful")
                return True
            else:
                logger.error("Geocoding service test failed")
                return False
                
        except Exception as e:
            logger.error(f"Geocoding service test error: {str(e)}")
            return False

# Create singleton instance
geocoding_service = GeocodingService() 