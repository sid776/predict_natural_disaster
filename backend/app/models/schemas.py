from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
from datetime import datetime
from enum import Enum

# Enums
class PredictionModel(str, Enum):
    quantum = "quantum"
    lstm = "lstm"
    rf = "rf"
    xgb = "xgb"
    svm = "svm"
    mlp = "mlp"

class DisasterType(str, Enum):
    tornado = "tornado"
    earthquake = "earthquake"
    wildfire = "wildfire"
    flood = "flood"

# Weather data models
class WeatherMain(BaseModel):
    temp: float  # Kelvin
    humidity: int  # Percentage
    pressure: float  # hPa

class WeatherWind(BaseModel):
    speed: float  # m/s
    deg: float  # degrees

class WeatherClouds(BaseModel):
    all: int  # percentage

class WeatherRain(BaseModel):
    h1: Optional[float] = None  # mm

class WeatherSys(BaseModel):
    sunrise: int
    sunset: int

class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class WeatherCoord(BaseModel):
    lat: float
    lon: float

class WeatherData(BaseModel):
    main: WeatherMain
    wind: WeatherWind
    clouds: WeatherClouds
    rain: Optional[WeatherRain] = None
    sys: WeatherSys
    weather: List[WeatherCondition]
    visibility: int  # meters
    coord: WeatherCoord
    mock_data: Optional[bool] = False

# Forecast models
class ForecastDay(BaseModel):
    date: str  # YYYY-MM-DD
    probability: float  # 0-1
    weather: WeatherData
    key_factors: List[str]

# Factor impacts
class FactorImpacts(BaseModel):
    temperature: Optional[float] = None  # percentage
    humidity: Optional[float] = None  # percentage
    pressure: Optional[float] = None  # percentage
    wind_speed: Optional[float] = None  # percentage

# Prediction request
class PredictionRequest(BaseModel):
    location: str = Field(..., min_length=3, description="City and state (e.g., 'New York, NY')")
    model: PredictionModel = Field(default=PredictionModel.quantum, description="Prediction model to use")
    disaster_type: DisasterType = Field(..., description="Type of disaster to predict")

# Prediction metadata
class PredictionMetadata(BaseModel):
    location: str
    model: PredictionModel
    disaster_type: DisasterType
    timestamp: str
    weather_data: WeatherData

# Prediction response
class PredictionResponse(BaseModel):
    probability: float = Field(..., ge=0, le=1, description="Probability between 0 and 1")
    forecast: List[ForecastDay]
    factors: FactorImpacts
    metadata: PredictionMetadata

# API response wrapper
class ApiResponse(BaseModel):
    data: Union[PredictionResponse, List[PredictionModel], WeatherData, Dict]
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None

# Geocoding response
class GeocodingResponse(BaseModel):
    lat: float
    lon: float
    display_name: str

# Global statistics
class GlobalStats(BaseModel):
    count: int
    deaths: int
    injuries: int
    damage: float  # billions USD

class GlobalStatsData(BaseModel):
    tornado: GlobalStats
    earthquake: GlobalStats
    wildfire: GlobalStats
    flood: GlobalStats

# Health check response
class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"
    services: Dict[str, str]

# Error response
class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now) 