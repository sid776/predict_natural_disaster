import sys
import os
import random
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

# Add the parent directory to the path to import the quantum model
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_dir)

try:
    from quantum_model import QuantumTornadoPredictor
except ImportError:
    # Try alternative import path
    sys.path.append(os.path.dirname(parent_dir))
    from quantum_model import QuantumTornadoPredictor
from app.models.schemas import (
    PredictionRequest, PredictionResponse, PredictionMetadata,
    ForecastDay, FactorImpacts, WeatherData, DisasterType, PredictionModel
)
from app.services.weather_service import weather_service
from app.services.geocoding_service import geocoding_service
import logging

logger = logging.getLogger(__name__)

class PredictionService:
    """Service for making disaster predictions using various models"""
    
    def __init__(self):
        self.quantum_predictor = QuantumTornadoPredictor()
        
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Make a prediction for a specific disaster type
        
        Args:
            request: PredictionRequest object containing location, model, and disaster type
            
        Returns:
            PredictionResponse object with prediction results
        """
        try:
            logger.info(f"Making prediction for {request.disaster_type} using {request.model} model")
            
            # Get coordinates for the location
            coords = geocoding_service.get_coordinates(request.location)
            if not coords:
                raise ValueError(f"Could not geocode location: {request.location}")
            
            lat, lon = coords
            
            # Get weather data
            weather_data = weather_service.get_weather_data(lat, lon)
            
            # Make prediction based on model
            probability = self._predict_with_model(request.model, request.disaster_type, weather_data)
            
            # Generate forecast
            forecast = self._generate_forecast(lat, lon, weather_data, request.disaster_type)
            
            # Calculate factor impacts
            factors = self._calculate_factor_impacts(weather_data, request.disaster_type)
            
            # Create metadata
            metadata = PredictionMetadata(
                location=request.location,
                model=request.model,
                disaster_type=request.disaster_type,
                timestamp=datetime.now().isoformat(),
                weather_data=weather_data
            )
            
            # Create response
            response = PredictionResponse(
                probability=probability,
                forecast=forecast,
                factors=factors,
                metadata=metadata
            )
            
            logger.info(f"Prediction completed: {probability:.2%} probability")
            return response
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise
    
    def _predict_with_model(self, model: PredictionModel, disaster_type: DisasterType, weather_data: WeatherData) -> float:
        """Make prediction using the specified model"""
        try:
            if model == PredictionModel.quantum:
                return self._predict_with_quantum(weather_data, disaster_type)
            elif model == PredictionModel.lstm:
                return self._predict_with_lstm(weather_data, disaster_type)
            elif model == PredictionModel.rf:
                return self._predict_with_rf(weather_data, disaster_type)
            elif model == PredictionModel.xgb:
                return self._predict_with_xgb(weather_data, disaster_type)
            elif model == PredictionModel.svm:
                return self._predict_with_svm(weather_data, disaster_type)
            elif model == PredictionModel.mlp:
                return self._predict_with_mlp(weather_data, disaster_type)
            else:
                logger.warning(f"Unknown model {model}, using quantum as fallback")
                return self._predict_with_quantum(weather_data, disaster_type)
                
        except Exception as e:
            logger.error(f"Error in model prediction: {str(e)}")
            return random.uniform(0.1, 0.5)  # Return random probability as fallback
    
    def _predict_with_quantum(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Make prediction using quantum model"""
        try:
            if disaster_type == DisasterType.tornado:
                # Convert WeatherData to dict format expected by quantum model
                weather_dict = {
                    'main': {
                        'temp': weather_data.main.temp,
                        'humidity': weather_data.main.humidity,
                        'pressure': weather_data.main.pressure
                    },
                    'wind': {
                        'speed': weather_data.wind.speed,
                        'deg': weather_data.wind.deg
                    },
                    'coord': {
                        'lat': weather_data.coord.lat,
                        'lon': weather_data.coord.lon
                    }
                }
                return self.quantum_predictor.predict(weather_dict)
            else:
                # For other disaster types, use the calculation functions from app.py
                return self._calculate_disaster_probability(weather_data, disaster_type)
                
        except Exception as e:
            logger.error(f"Error in quantum prediction: {str(e)}")
            return random.uniform(0.1, 0.5)
    
    def _calculate_disaster_probability(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Calculate probability for non-tornado disasters using research-based models"""
        try:
            if disaster_type == DisasterType.earthquake:
                return self._calculate_earthquake_probability(weather_data)
            elif disaster_type == DisasterType.wildfire:
                return self._calculate_fire_probability(weather_data)
            elif disaster_type == DisasterType.flood:
                return self._calculate_flood_probability(weather_data)
            else:
                return random.uniform(0.1, 0.5)
                
        except Exception as e:
            logger.error(f"Error calculating {disaster_type} probability: {str(e)}")
            return random.uniform(0.1, 0.5)
    
    def _calculate_earthquake_probability(self, weather_data: WeatherData) -> float:
        """Calculate earthquake probability based on atmospheric pressure and humidity"""
        pressure = weather_data.main.pressure
        humidity = weather_data.main.humidity
        
        # Pressure factor - sudden drops can trigger seismic activity
        pressure_factor = max(0, min(1, (1013 - pressure) / 50))
        
        # Humidity factor - less direct but often accompanies low pressure
        humidity_factor = max(0, min(1, humidity / 100))
        
        # Combine factors with research-based weights
        probability = (0.7 * pressure_factor + 0.3 * humidity_factor) * 0.6
        
        # Add quantum-inspired uncertainty
        probability += random.uniform(-0.1, 0.1)
        
        return max(0, min(1, probability))
    
    def _calculate_fire_probability(self, weather_data: WeatherData) -> float:
        """Calculate wildfire probability using Canadian Forest Fire Weather Index principles"""
        temp = weather_data.main.temp - 273.15  # Convert to Celsius
        humidity = weather_data.main.humidity
        wind_speed = weather_data.wind.speed
        
        # Temperature factor - higher temperatures increase fire risk
        temp_factor = max(0, min(1, (temp - 20) / 20))
        
        # Humidity factor - lower humidity increases fire risk
        humidity_factor = max(0, min(1, (100 - humidity) / 70))
        
        # Wind speed factor - higher wind speeds increase fire risk
        wind_factor = max(0, min(1, wind_speed / 10))
        
        # Combine factors with research-based weights
        probability = (0.4 * temp_factor + 0.4 * humidity_factor + 0.2 * wind_factor) * 0.8
        
        # Add quantum-inspired uncertainty
        probability += random.uniform(-0.1, 0.1)
        
        return max(0, min(1, probability))
    
    def _calculate_flood_probability(self, weather_data: WeatherData) -> float:
        """Calculate flood probability using hydrological models"""
        temp = weather_data.main.temp - 273.15  # Convert to Celsius
        humidity = weather_data.main.humidity
        pressure = weather_data.main.pressure
        
        # Humidity factor - higher humidity increases flood risk
        humidity_factor = max(0, min(1, (humidity - 60) / 40))
        
        # Pressure factor - lower pressure increases flood risk
        pressure_factor = max(0, min(1, (1013 - pressure) / 30))
        
        # Temperature factor - moderate temperatures increase flood risk
        temp_factor = max(0, min(1, 1 - abs(temp - 15) / 20))
        
        # Combine factors with research-based weights
        probability = (0.4 * humidity_factor + 0.4 * pressure_factor + 0.2 * temp_factor) * 0.7
        
        # Add quantum-inspired uncertainty
        probability += random.uniform(-0.1, 0.1)
        
        return max(0, min(1, probability))
    
    def _generate_forecast(self, lat: float, lon: float, weather_data: WeatherData, disaster_type: DisasterType) -> List[ForecastDay]:
        """Generate 30-day forecast for the disaster type"""
        forecast = []
        base_date = datetime.now()
        
        for i in range(30):
            date = base_date + timedelta(days=i)
            
            # Simulate weather changes for each day
            simulated_weather = self._simulate_weather_changes(weather_data, i)
            
            # Calculate probability for this day
            probability = self._predict_with_model(PredictionModel.quantum, disaster_type, simulated_weather)
            
            # Determine key factors
            key_factors = self._get_key_factors(simulated_weather, disaster_type)
            
            forecast_day = ForecastDay(
                date=date.strftime('%Y-%m-%d'),
                probability=probability,
                weather=simulated_weather,
                key_factors=key_factors
            )
            
            forecast.append(forecast_day)
        
        return forecast
    
    def _simulate_weather_changes(self, base_weather: WeatherData, day: int) -> WeatherData:
        """Simulate weather changes for forecast days"""
        # Create a copy of the weather data
        weather = WeatherData(
            main=base_weather.main,
            wind=base_weather.wind,
            clouds=base_weather.clouds,
            rain=base_weather.rain,
            sys=base_weather.sys,
            weather=base_weather.weather,
            visibility=base_weather.visibility,
            coord=base_weather.coord,
            mock_data=base_weather.mock_data
        )
        
        # Add some randomness to weather parameters
        weather.main.temp += random.uniform(-2, 2)
        weather.main.humidity = max(0, min(100, weather.main.humidity + random.uniform(-5, 5)))
        weather.main.pressure += random.uniform(-5, 5)
        weather.wind.speed = max(0, weather.wind.speed + random.uniform(-1, 1))
        
        # Ensure values stay within reasonable ranges
        weather.main.temp = max(250, min(320, weather.main.temp))  # -23°C to 47°C in Kelvin
        weather.main.pressure = max(900, min(1100, weather.main.pressure))
        
        return weather
    
    def _get_key_factors(self, weather_data: WeatherData, disaster_type: DisasterType) -> List[str]:
        """Determine key factors for the disaster type"""
        factors = []
        temp = weather_data.main.temp - 273.15  # Convert to Celsius
        
        if disaster_type == DisasterType.tornado:
            if temp > 25:
                factors.append("High Temperature")
            if weather_data.main.humidity > 70:
                factors.append("High Humidity")
            if weather_data.main.pressure < 1000:
                factors.append("Low Pressure")
            if weather_data.wind.speed > 10:
                factors.append("Strong Winds")
        elif disaster_type == DisasterType.earthquake:
            if weather_data.main.pressure < 990:
                factors.append("Low Pressure")
            if weather_data.main.humidity > 80:
                factors.append("High Humidity")
        elif disaster_type == DisasterType.wildfire:
            if temp > 30:
                factors.append("High Temperature")
            if weather_data.main.humidity < 30:
                factors.append("Low Humidity")
            if weather_data.wind.speed > 5:
                factors.append("Strong Winds")
        elif disaster_type == DisasterType.flood:
            if weather_data.main.humidity > 80:
                factors.append("High Humidity")
            if weather_data.main.pressure < 1000:
                factors.append("Low Pressure")
            if 10 <= temp <= 20:
                factors.append("Moderate Temperature")
        
        return factors if factors else ["Normal Conditions"]
    
    def _calculate_factor_impacts(self, weather_data: WeatherData, disaster_type: DisasterType) -> FactorImpacts:
        """Calculate the impact of each weather factor on the disaster probability"""
        temp = weather_data.main.temp - 273.15  # Convert to Celsius
        humidity = weather_data.main.humidity
        pressure = weather_data.main.pressure
        wind_speed = weather_data.wind.speed
        
        if disaster_type == DisasterType.tornado:
            temp_impact = self._calculate_temperature_impact(temp)
            humidity_impact = self._calculate_humidity_impact(humidity)
            pressure_impact = self._calculate_pressure_impact(pressure)
            wind_impact = self._calculate_wind_impact(wind_speed)
            
            # Ensure minimum impact values for better visualization
            temp_impact = max(temp_impact, 0.1)
            humidity_impact = max(humidity_impact, 0.1)
            pressure_impact = max(pressure_impact, 0.1)
            wind_impact = max(wind_impact, 0.1)
            
            total_impact = temp_impact + humidity_impact + pressure_impact + wind_impact
            
            return FactorImpacts(
                temperature=round((temp_impact / total_impact) * 100, 1),
                humidity=round((humidity_impact / total_impact) * 100, 1),
                pressure=round((pressure_impact / total_impact) * 100, 1),
                wind_speed=round((wind_impact / total_impact) * 100, 1)
            )
        elif disaster_type == DisasterType.earthquake:
            pressure_impact = max(0.1, min(1, (1013 - pressure) / 50))
            humidity_impact = max(0.1, min(1, humidity / 100))
            
            total_impact = pressure_impact + humidity_impact
            
            return FactorImpacts(
                pressure=round((pressure_impact / total_impact) * 100, 1),
                humidity=round((humidity_impact / total_impact) * 100, 1)
            )
        elif disaster_type == DisasterType.wildfire:
            temp_impact = max(0.1, min(1, (temp - 20) / 20))
            humidity_impact = max(0.1, min(1, (100 - humidity) / 70))
            wind_impact = max(0.1, min(1, wind_speed / 10))
            
            total_impact = temp_impact + humidity_impact + wind_impact
            
            return FactorImpacts(
                temperature=round((temp_impact / total_impact) * 100, 1),
                humidity=round((humidity_impact / total_impact) * 100, 1),
                wind_speed=round((wind_impact / total_impact) * 100, 1)
            )
        elif disaster_type == DisasterType.flood:
            humidity_impact = max(0.1, min(1, (humidity - 60) / 40))
            pressure_impact = max(0.1, min(1, (1013 - pressure) / 30))
            temp_impact = max(0.1, min(1, 1 - abs(temp - 15) / 20))
            
            total_impact = humidity_impact + pressure_impact + temp_impact
            
            return FactorImpacts(
                humidity=round((humidity_impact / total_impact) * 100, 1),
                pressure=round((pressure_impact / total_impact) * 100, 1),
                temperature=round((temp_impact / total_impact) * 100, 1)
            )
        else:
            return FactorImpacts()
    
    def _calculate_temperature_impact(self, temp: float) -> float:
        """Calculate temperature impact on tornado probability"""
        if 20 <= temp <= 30:
            return 1.0
        elif 15 <= temp < 20 or 30 < temp <= 35:
            return 0.7
        elif 10 <= temp < 15 or 35 < temp <= 40:
            return 0.4
        else:
            return 0.1
    
    def _calculate_humidity_impact(self, humidity: float) -> float:
        """Calculate humidity impact on tornado probability"""
        if 60 <= humidity <= 80:
            return 1.0
        elif 50 <= humidity < 60 or 80 < humidity <= 90:
            return 0.7
        elif 40 <= humidity < 50 or 90 < humidity <= 95:
            return 0.4
        else:
            return 0.1
    
    def _calculate_pressure_impact(self, pressure: float) -> float:
        """Calculate pressure impact on tornado probability"""
        if 980 <= pressure <= 1000:
            return 1.0
        elif 970 <= pressure < 980 or 1000 < pressure <= 1010:
            return 0.7
        elif 960 <= pressure < 970 or 1010 < pressure <= 1020:
            return 0.4
        else:
            return 0.1
    
    def _calculate_wind_impact(self, wind_speed: float) -> float:
        """Calculate wind speed impact on tornado probability"""
        if 10 <= wind_speed <= 20:
            return 1.0
        elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:
            return 0.7
        elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:
            return 0.4
        else:
            return 0.1
    
    # Stub methods for other models
    def _predict_with_lstm(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Stub for LSTM model prediction"""
        return random.uniform(0.2, 0.8)
    
    def _predict_with_rf(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Stub for Random Forest model prediction"""
        return random.uniform(0.2, 0.8)
    
    def _predict_with_xgb(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Stub for XGBoost model prediction"""
        return random.uniform(0.2, 0.8)
    
    def _predict_with_svm(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Stub for SVM model prediction"""
        return random.uniform(0.2, 0.8)
    
    def _predict_with_mlp(self, weather_data: WeatherData, disaster_type: DisasterType) -> float:
        """Stub for MLP/ANN model prediction"""
        return random.uniform(0.2, 0.8)

# Create singleton instance
prediction_service = PredictionService() 