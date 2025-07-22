from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from datetime import datetime

from app.models.schemas import (
    PredictionRequest, PredictionResponse, ApiResponse,
    WeatherData, GeocodingResponse, PredictionModel, GlobalStatsData
)
from app.services.prediction_service import prediction_service
from app.services.weather_service import weather_service
from app.services.geocoding_service import geocoding_service
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

@router.get("/health", response_model=ApiResponse)
async def health_check() -> ApiResponse:
    """
    Health check endpoint
    """
    try:
        # Test external services
        weather_ok = weather_service.test_api_connection()
        geocoding_ok = geocoding_service.test_service()
        
        services_status = {
            "weather_api": "healthy" if weather_ok else "unhealthy",
            "geocoding_service": "healthy" if geocoding_ok else "unhealthy",
            "prediction_service": "healthy"
        }
        
        overall_health = weather_ok and geocoding_ok
        
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
                    "prediction_service": "unknown"
                }
            },
            success=False,
            error=f"Health check failed: {str(e)}"
        ) 