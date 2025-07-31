from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from datetime import datetime

from app.models.schemas import (
    PredictionRequest, PredictionResponse, ApiResponse,
    WeatherData, GeocodingResponse, PredictionModel, GlobalStatsData,
    WeatherAlert, WeatherAlertsResponse, DataSourceInfo
)
from app.services.prediction_service import prediction_service
from app.services.weather_service import weather_service
from app.services.geocoding_service import geocoding_service
from app.services.weather_alerts_service import weather_alerts_service
from app.utils.config import settings

router = APIRouter(prefix="/api", tags=["predictions"])

@router.post("/predict", response_model=ApiResponse)
async def predict_disaster(request: PredictionRequest) -> ApiResponse:
    """
    Make a disaster prediction for a specific location and disaster type
    """
    try:
        # Validate location
        if not geocoding_service.validate_location(request.location):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid location: {request.location}. Please provide a valid city and state."
            )
        
        # Make prediction
        prediction = prediction_service.predict(request)
        
        return ApiResponse(
            data=prediction,
            success=True,
            message=f"Prediction completed successfully for {request.disaster_type.value}"
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.get("/weather/{lat}/{lon}", response_model=ApiResponse)
async def get_weather(lat: float, lon: float) -> ApiResponse:
    """
    Get current weather data for given coordinates
    """
    try:
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400,
                detail="Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            )
        
        weather_data = weather_service.get_weather_data(lat, lon)
        
        return ApiResponse(
            data=weather_data,
            success=True,
            message="Weather data retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get weather data: {str(e)}")

@router.get("/geocode/{location}", response_model=ApiResponse)
async def geocode_location(location: str) -> ApiResponse:
    """
    Get coordinates and location information for a given location string
    """
    try:
        location_info = geocoding_service.get_location_info(location)
        
        if not location_info:
            raise HTTPException(
                status_code=404,
                detail=f"Location not found: {location}"
            )
        
        return ApiResponse(
            data=location_info,
            success=True,
            message="Location geocoded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Geocoding failed: {str(e)}")

@router.get("/models", response_model=ApiResponse)
async def get_models() -> ApiResponse:
    """
    Get list of available prediction models
    """
    try:
        models = [model.value for model in PredictionModel]
        
        return ApiResponse(
            data=models,
            success=True,
            message="Available models retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")

@router.get("/data-sources", response_model=ApiResponse)
async def get_data_sources() -> ApiResponse:
    """
    Get list of available data sources
    """
    try:
        data_sources = [
            DataSourceInfo(
                id="data_fusion",
                name="Data Fusion",
                description="Combined data from multiple sources for comprehensive analysis",
                icon="🔗",
                features=["all_features", "cross_validation", "enhanced_accuracy"],
                disaster_types=["tornado", "earthquake", "wildfire", "flood"],
                api_required=True
            ),
            DataSourceInfo(
                id="openweathermap",
                name="OpenWeatherMap",
                description="Real-time weather data including temperature, humidity, pressure, and wind",
                icon="🌤️",
                features=["temperature", "humidity", "pressure", "wind_speed", "wind_direction"],
                disaster_types=["tornado", "wildfire", "flood"],
                api_required=True
            ),
            DataSourceInfo(
                id="usgs",
                name="USGS Earthquake",
                description="United States Geological Survey earthquake data and historical records",
                icon="🌋",
                features=["magnitude", "depth", "time", "historical_data"],
                disaster_types=["earthquake"],
                api_required=False
            ),
            DataSourceInfo(
                id="nasa_power",
                name="NASA POWER",
                description="NASA Prediction of Worldwide Energy Resources climate data",
                icon="🛰️",
                features=["temperature", "wind_speed", "precipitation", "solar_radiation"],
                disaster_types=["tornado", "wildfire", "flood"],
                api_required=False
            )
        ]
        
        return ApiResponse(
            data=data_sources,
            success=True,
            message="Available data sources retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get data sources: {str(e)}")

@router.get("/stats", response_model=ApiResponse)
async def get_global_stats() -> ApiResponse:
    """
    Get global disaster statistics
    """
    try:
        stats = GlobalStatsData(
            tornado={
                "count": 1250,  # Average annual tornadoes in the US
                "deaths": 60,   # Average annual deaths
                "injuries": 1500,
                "damage": 1.5   # Billions USD
            },
            earthquake={
                "count": 20000,  # Annual earthquakes worldwide
                "deaths": 2000,  # Average annual deaths
                "injuries": 5000,
                "damage": 5.0    # Billions USD
            },
            wildfire={
                "count": 50000,  # Annual wildfires in the US
                "deaths": 100,   # Average annual deaths
                "injuries": 2000,
                "damage": 2.0    # Billions USD
            },
            flood={
                "count": 1000,   # Annual significant floods worldwide
                "deaths": 5000,  # Average annual deaths
                "injuries": 10000,
                "damage": 10.0   # Billions USD
            }
        )
        
        return ApiResponse(
            data=stats,
            success=True,
            message="Global statistics retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.get("/weather-alerts/{location}", response_model=ApiResponse)
async def get_weather_alerts(location: str) -> ApiResponse:
    """
    Get weather alerts for a specific location
    """
    try:
        # First geocode the location to get coordinates
        location_info = geocoding_service.get_location_info(location)
        
        if not location_info:
            raise HTTPException(
                status_code=404,
                detail=f"Location not found: {location}"
            )
        
        # Get weather alerts for the coordinates
        alerts = weather_alerts_service.get_alerts_for_location(
            location_info.lat, 
            location_info.lon
        )
        
        # Convert alerts to Pydantic models
        alert_models = [WeatherAlert(**alert.to_dict()) for alert in alerts]
        
        response_data = WeatherAlertsResponse(
            alerts=alert_models,
            location=location,
            coordinates={"lat": location_info.lat, "lon": location_info.lon},
            timestamp=datetime.now().isoformat()
        )
        
        return ApiResponse(
            data=response_data,
            success=True,
            message=f"Found {len(alerts)} weather alerts for {location}"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get weather alerts: {str(e)}")

@router.get("/weather-alerts/coordinates/{lat}/{lon}", response_model=ApiResponse)
async def get_weather_alerts_by_coordinates(lat: float, lon: float) -> ApiResponse:
    """
    Get weather alerts for specific coordinates
    """
    try:
        # Validate coordinates
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise HTTPException(
                status_code=400,
                detail="Invalid coordinates. Latitude must be between -90 and 90, longitude between -180 and 180."
            )
        
        # Get weather alerts for the coordinates
        alerts = weather_alerts_service.get_alerts_for_location(lat, lon)
        
        # Convert alerts to Pydantic models
        alert_models = [WeatherAlert(**alert.to_dict()) for alert in alerts]
        
        response_data = WeatherAlertsResponse(
            alerts=alert_models,
            location=f"Coordinates ({lat}, {lon})",
            coordinates={"lat": lat, "lon": lon},
            timestamp=datetime.now().isoformat()
        )
        
        return ApiResponse(
            data=response_data,
            success=True,
            message=f"Found {len(alerts)} weather alerts for coordinates ({lat}, {lon})"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get weather alerts: {str(e)}")

@router.get("/health", response_model=ApiResponse)
async def health_check() -> ApiResponse:
    """
    Health check endpoint
    """
    try:
        # Test external services
        weather_ok = weather_service.test_api_connection()
        geocoding_ok = geocoding_service.test_service()
        alerts_ok = weather_alerts_service.test_api_connection()
        
        services_status = {
            "weather_api": "healthy" if weather_ok else "unhealthy",
            "geocoding_service": "healthy" if geocoding_ok else "unhealthy",
            "weather_alerts_api": "healthy" if alerts_ok else "unhealthy",
            "prediction_service": "healthy"
        }
        
        overall_health = weather_ok and geocoding_ok and alerts_ok
        
        return ApiResponse(
            data={
                "status": "healthy" if overall_health else "degraded",
                "timestamp": datetime.now().isoformat(),
                "version": settings.api_version,
                "services": services_status
            },
            success=overall_health,
            message="Health check completed"
        )
        
    except Exception as e:
        return ApiResponse(
            data={
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "version": settings.api_version,
                "services": {
                    "weather_api": "unknown",
                    "geocoding_service": "unknown",
                    "weather_alerts_api": "unknown",
                    "prediction_service": "unknown"
                }
            },
            success=False,
            error=f"Health check failed: {str(e)}"
        ) 