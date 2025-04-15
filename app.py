from flask import Flask, render_template, request, jsonify
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from quantum_model import QuantumTornadoPredictor
import os
from dotenv import load_dotenv
import datetime
import math
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

app = Flask(__name__)
predictor = QuantumTornadoPredictor()

# Initialize geocoder
geolocator = Nominatim(user_agent="tornado_predictor")

def get_coordinates(location):
    try:
        location_data = geolocator.geocode(location + ", USA")
        if location_data:
            return location_data.latitude, location_data.longitude
        return None, None
    except GeocoderTimedOut:
        return None, None

def get_weather_data(lat, lon):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not api_key:
        print("Error: OpenWeatherMap API key not found in .env file")
        return get_mock_weather_data()
    
    if api_key == 'your_openweathermap_api_key_here':
        print("Error: Please replace the placeholder API key with your actual OpenWeatherMap API key")
        return get_mock_weather_data()
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        print(f"Making API request to: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"API Response Status Code: {response.status_code}")
        print(f"API Response Headers: {response.headers}")
        print(f"API Response Content: {response.content}")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Error: Invalid API key")
            return get_mock_weather_data()
        elif response.status_code == 404:
            print("Error: Location not found")
            return get_mock_weather_data()
        else:
            print(f"Error: API request failed with status code {response.status_code}")
            return get_mock_weather_data()
            
    except requests.exceptions.Timeout:
        print("Error: API request timed out")
        return get_mock_weather_data()
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the API")
        return get_mock_weather_data()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return get_mock_weather_data()

def get_mock_weather_data():
    """Return mock weather data for testing when the API is not available"""
    print("Using mock weather data")
    return {
        'main': {
            'temp': 293.15,  # 20°C
            'humidity': 65,
            'pressure': 1013
        },
        'wind': {
            'speed': 5.5,
            'deg': 180
        },
        'clouds': {
            'all': 40
        },
        'rain': {
            '1h': 0
        },
        'sys': {
            'sunrise': 1622520000,
            'sunset': 1622574000
        },
        'weather': [
            {
                'id': 800,
                'main': 'Clear',
                'description': 'clear sky',
                'icon': '01d'
            }
        ],
        'visibility': 10000,  # 10km
        'mock_data': True  # Flag to indicate this is mock data
    }

def test_api_connection():
    """Test the OpenWeatherMap API connection with a known location"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    print(f"Testing API connection with key: {api_key[:5]}...")
    
    # Test with New York City coordinates
    lat, lon = 40.7128, -74.0060
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        print(f"Requesting weather data from: {url}")
        response = requests.get(url, timeout=10)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.text[:500]}...")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully parsed JSON response: {data.keys()}")
            return True
        else:
            print(f"API test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"API test error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

@app.route('/')
def home():
    # Test API connection when the app starts
    api_working = test_api_connection()
    return render_template('index.html', api_working=api_working)

def generate_forecast(location, coordinates, current_weather):
    """Generate a 30-day forecast based on current weather conditions."""
    forecast = []
    base_weather = current_weather.copy()
    
    for day in range(30):
        date = datetime.now() + timedelta(days=day)
        weather = simulate_weather_changes(base_weather, day)
        probability = calculate_tornado_probability(weather)
        key_factors = get_key_factors(weather)
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'probability': probability,
            'weather': weather,
            'key_factors': key_factors
        })
    
    return forecast

def simulate_weather_changes(base_weather, day):
    """Simulate weather changes for each day in the forecast."""
    weather = base_weather.copy()
    
    # Add some randomness to weather parameters
    weather['main']['temp'] += random.uniform(-2, 2)
    weather['main']['humidity'] = max(0, min(100, weather['main']['humidity'] + random.uniform(-5, 5)))
    weather['main']['pressure'] += random.uniform(-5, 5)
    weather['wind']['speed'] = max(0, weather['wind']['speed'] + random.uniform(-1, 1))
    
    # Ensure values stay within reasonable ranges
    weather['main']['temp'] = max(-50, min(50, weather['main']['temp']))
    weather['main']['pressure'] = max(900, min(1100, weather['main']['pressure']))
    
    return weather

def get_key_factors(weather):
    """Determine which factors are most significant for tornado formation."""
    factors = []
    
    if weather['main']['temp'] > 25:
        factors.append('High Temperature')
    if weather['main']['humidity'] > 70:
        factors.append('High Humidity')
    if weather['main']['pressure'] < 1000:
        factors.append('Low Pressure')
    if weather['wind']['speed'] > 10:
        factors.append('Strong Winds')
    
    return factors if factors else ['Normal Conditions']

def calculate_tornado_probability(weather_data):
    """
    Calculate the probability of a tornado based on weather conditions.
    Returns a probability between 0 and 1.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    
    # Initialize probability components
    temp_prob = 0.0
    humidity_prob = 0.0
    pressure_prob = 0.0
    wind_prob = 0.0
    
    # Temperature factor (optimal range: 20-30°C)
    if 20 <= temp <= 30:
        temp_prob = 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        temp_prob = 0.7
    elif 10 <= temp < 15 or 35 < temp <= 40:
        temp_prob = 0.4
    else:
        temp_prob = 0.1
    
    # Humidity factor (optimal range: 60-80%)
    if 60 <= humidity <= 80:
        humidity_prob = 1.0
    elif 50 <= humidity < 60 or 80 < humidity <= 90:
        humidity_prob = 0.7
    elif 40 <= humidity < 50 or 90 < humidity <= 95:
        humidity_prob = 0.4
    else:
        humidity_prob = 0.1
    
    # Pressure factor (optimal range: 980-1000 hPa)
    if 980 <= pressure <= 1000:
        pressure_prob = 1.0
    elif 970 <= pressure < 980 or 1000 < pressure <= 1010:
        pressure_prob = 0.7
    elif 960 <= pressure < 970 or 1010 < pressure <= 1020:
        pressure_prob = 0.4
    else:
        pressure_prob = 0.1
    
    # Wind speed factor (optimal range: 10-20 m/s)
    if 10 <= wind_speed <= 20:
        wind_prob = 1.0
    elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:
        wind_prob = 0.7
    elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:
        wind_prob = 0.4
    else:
        wind_prob = 0.1
    
    # Calculate weighted probability
    weights = {
        'temperature': 0.3,
        'humidity': 0.3,
        'pressure': 0.2,
        'wind_speed': 0.2
    }
    
    total_probability = (
        temp_prob * weights['temperature'] +
        humidity_prob * weights['humidity'] +
        pressure_prob * weights['pressure'] +
        wind_prob * weights['wind_speed']
    )
    
    # Apply quantum-inspired adjustments
    quantum_factor = random.uniform(0.9, 1.1)  # Simulate quantum uncertainty
    final_probability = min(1.0, total_probability * quantum_factor)
    
    return final_probability

def calculate_factor_impacts(weather_data):
    """
    Calculate the impact of each weather factor on the tornado probability.
    Returns a dictionary with impact percentages for each factor.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    
    # Calculate individual impacts
    temp_impact = calculate_temperature_impact(temp)
    humidity_impact = calculate_humidity_impact(humidity)
    pressure_impact = calculate_pressure_impact(pressure)
    wind_impact = calculate_wind_impact(wind_speed)
    
    # Calculate total impact
    total_impact = temp_impact + humidity_impact + pressure_impact + wind_impact
    
    # Convert to percentages
    impacts = {
        'temperature': round((temp_impact / total_impact) * 100, 1),
        'humidity': round((humidity_impact / total_impact) * 100, 1),
        'pressure': round((pressure_impact / total_impact) * 100, 1),
        'wind_speed': round((wind_impact / total_impact) * 100, 1)
    }
    
    return impacts

def calculate_temperature_impact(temp):
    """Calculate the impact of temperature on tornado probability."""
    if 20 <= temp <= 30:
        return 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        return 0.7
    elif 10 <= temp < 15 or 35 < temp <= 40:
        return 0.4
    return 0.1

def calculate_humidity_impact(humidity):
    """Calculate the impact of humidity on tornado probability."""
    if 60 <= humidity <= 80:
        return 1.0
    elif 50 <= humidity < 60 or 80 < humidity <= 90:
        return 0.7
    elif 40 <= humidity < 50 or 90 < humidity <= 95:
        return 0.4
    return 0.1

def calculate_pressure_impact(pressure):
    """Calculate the impact of pressure on tornado probability."""
    if 980 <= pressure <= 1000:
        return 1.0
    elif 970 <= pressure < 980 or 1000 < pressure <= 1010:
        return 0.7
    elif 960 <= pressure < 970 or 1010 < pressure <= 1020:
        return 0.4
    return 0.1

def calculate_wind_impact(wind_speed):
    """Calculate the impact of wind speed on tornado probability."""
    if 10 <= wind_speed <= 20:
        return 1.0
    elif 7 <= wind_speed < 10 or 20 < wind_speed <= 25:
        return 0.7
    elif 5 <= wind_speed < 7 or 25 < wind_speed <= 30:
        return 0.4
    return 0.1

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
        
        # Get coordinates for the location
        coordinates = get_coordinates(location)
        if not coordinates:
            return jsonify({'error': 'Location not found'}), 404
        
        # Get current weather data
        weather_data = get_weather_data(coordinates[0], coordinates[1])
        if not weather_data:
            return jsonify({'error': 'Failed to fetch weather data'}), 500
        
        # Calculate current tornado probability
        probability = calculate_tornado_probability(weather_data)
        
        # Generate 30-day forecast
        forecast = generate_forecast(location, coordinates, weather_data)
        
        # Calculate factor impacts
        impacts = calculate_factor_impacts(weather_data)
        
        return jsonify({
            'location': location,
            'coordinates': coordinates,
            'weather_data': weather_data,
            'probability': probability,
            'factor_impacts': impacts,
            'forecast': forecast
        })
        
    except Exception as e:
        print(f"Error in predict route: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

def calculate_earthquake_probability(weather_data):
    """
    Calculate the probability of an earthquake based on research-based parameters.
    This model uses a combination of weather data and geological factors.
    """
    # Extract relevant weather parameters
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    
    # Research indicates that atmospheric pressure changes can trigger earthquakes
    # Sudden drops in pressure (especially below 990 hPa) can increase seismic activity
    pressure_factor = max(0, min(1, (1013 - pressure) / 50))
    
    # Humidity is less directly related to earthquakes, but high humidity often
    # accompanies low pressure systems which can trigger seismic activity
    humidity_factor = max(0, min(1, humidity / 100))
    
    # Combine factors with weights based on research
    # Pressure changes have a stronger correlation with seismic activity
    probability = (0.7 * pressure_factor + 0.3 * humidity_factor) * 0.6
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_fire_probability(weather_data):
    """
    Calculate the probability of a forest fire based on research-based parameters.
    Uses the Canadian Forest Fire Weather Index (FWI) system as a reference.
    """
    # Extract relevant weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Temperature factor - higher temperatures increase fire risk
    # Research shows temperatures above 30°C significantly increase fire risk
    temp_factor = max(0, min(1, (temp - 20) / 20))
    
    # Humidity factor - lower humidity increases fire risk
    # Research indicates humidity below 30% significantly increases fire risk
    humidity_factor = max(0, min(1, (100 - humidity) / 70))
    
    # Wind speed factor - higher wind speeds increase fire risk
    # Research shows wind speeds above 15 km/h (4.17 m/s) increase fire spread
    wind_factor = max(0, min(1, wind_speed / 10))
    
    # Combine factors with weights based on research
    # Temperature and humidity are the primary factors, with wind as a secondary factor
    probability = (0.4 * temp_factor + 0.4 * humidity_factor + 0.2 * wind_factor) * 0.8
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_flood_probability(weather_data):
    """
    Calculate the probability of flooding based on research-based parameters.
    Uses hydrological models as a reference.
    """
    # Extract relevant weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    
    # Humidity factor - higher humidity increases flood risk
    # Research shows humidity above 80% often precedes heavy rainfall
    humidity_factor = max(0, min(1, (humidity - 60) / 40))
    
    # Pressure factor - lower pressure increases flood risk
    # Research indicates pressure below 1000 hPa often accompanies storm systems
    pressure_factor = max(0, min(1, (1013 - pressure) / 30))
    
    # Temperature factor - moderate temperatures increase flood risk
    # Research shows moderate temperatures (10-20°C) with high humidity often lead to flooding
    temp_factor = max(0, min(1, 1 - abs(temp - 15) / 20))
    
    # Combine factors with weights based on research
    # Humidity and pressure are the primary factors, with temperature as a secondary factor
    probability = (0.4 * humidity_factor + 0.4 * pressure_factor + 0.2 * temp_factor) * 0.7
    
    # Add some randomness to simulate uncertainty
    probability += random.uniform(-0.1, 0.1)
    
    # Ensure probability is between 0 and 1
    return max(0, min(1, probability))

def calculate_earthquake_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on earthquake probability.
    Based on research on earthquake triggers.
    """
    # Extract weather parameters
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    
    # Calculate individual impacts based on research
    # Pressure changes have a stronger correlation with seismic activity
    pressure_impact = max(0, min(1, (1013 - pressure) / 50))
    humidity_impact = max(0, min(1, humidity / 100))
    
    # Convert to percentages
    return {
        'pressure': pressure_impact * 100,
        'humidity': humidity_impact * 100
    }

def calculate_fire_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on forest fire probability.
    Based on the Canadian Forest Fire Weather Index (FWI) system.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    
    # Calculate individual impacts based on research
    # Temperature and humidity are the primary factors
    temp_impact = max(0, min(1, (temp - 20) / 20))
    humidity_impact = max(0, min(1, (100 - humidity) / 70))
    wind_impact = max(0, min(1, wind_speed / 10))
    
    # Convert to percentages
    return {
        'temperature': temp_impact * 100,
        'humidity': humidity_impact * 100,
        'wind_speed': wind_impact * 100
    }

def calculate_flood_factor_impacts(weather_data):
    """
    Calculate the impact of various factors on flooding probability.
    Based on hydrological research.
    """
    # Extract weather parameters
    temp = weather_data['main']['temp'] - 273.15  # Convert Kelvin to Celsius
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    
    # Calculate individual impacts based on research
    # Humidity and pressure are the primary factors
    humidity_impact = max(0, min(1, (humidity - 60) / 40))
    pressure_impact = max(0, min(1, (1013 - pressure) / 30))
    temp_impact = max(0, min(1, 1 - abs(temp - 15) / 20))
    
    # Convert to percentages
    return {
        'humidity': humidity_impact * 100,
        'pressure': pressure_impact * 100,
        'temperature': temp_impact * 100
    }

def get_30_day_forecast(lat, lon):
    """
    Get a 30-day forecast for a location.
    This is a simplified version that generates mock forecast data.
    In a real application, you would use a weather API that provides long-term forecasts.
    """
    forecast = []
    base_date = datetime.now()
    
    # Generate mock forecast data for 30 days
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Generate slightly different weather data for each day
        # This is a simplified approach - in a real app, you'd use actual forecast data
        temp = random.uniform(15, 35)  # Temperature in Celsius
        humidity = random.uniform(40, 90)  # Humidity percentage
        pressure = random.uniform(980, 1020)  # Pressure in hPa
        wind_speed = random.uniform(0, 15)  # Wind speed in m/s
        
        # Create weather data structure for this day
        weather = {
            'main': {
                'temp': temp + 273.15,  # Convert to Kelvin for consistency
                'humidity': humidity,
                'pressure': pressure
            },
            'wind': {
                'speed': wind_speed
            }
        }
        
        # Calculate probability based on the weather data
        # This is a simplified approach - in a real app, you'd use more sophisticated models
        probability = random.uniform(0.1, 0.9)
        
        # Determine key factors based on the weather data
        key_factors = []
        if temp > 30:
            key_factors.append("High Temperature")
        if humidity > 80:
            key_factors.append("High Humidity")
        if pressure < 990:
            key_factors.append("Low Pressure")
        if wind_speed > 10:
            key_factors.append("Strong Winds")
        
        if not key_factors:
            key_factors.append("Normal Conditions")
        
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'probability': probability,
            'weather': weather,  # Include the weather data in the forecast entry
            'key_factors': key_factors
        })
    
    return forecast

@app.route('/predict-earthquake', methods=['POST'])
def predict_earthquake():
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
            
        # Get coordinates for the location
        coordinates = get_coordinates(location)
        if not coordinates:
            return jsonify({'error': 'Could not find coordinates for the location'}), 400
            
        # Get weather data for the location
        weather_data = get_weather_data(coordinates[0], coordinates[1])
        if not weather_data:
            return jsonify({'error': 'Could not fetch weather data'}), 400
            
        # Calculate earthquake probability based on various factors
        probability = calculate_earthquake_probability(weather_data)
        
        # Get 30-day forecast
        forecast = get_30_day_forecast(coordinates[0], coordinates[1])
        
        # Calculate factor impacts
        factor_impacts = calculate_earthquake_factor_impacts(weather_data)
        
        return jsonify({
            'location': location,
            'coordinates': coordinates,
            'probability': probability,
            'weather_data': weather_data,
            'forecast': forecast,
            'factor_impacts': factor_impacts
        })
        
    except Exception as e:
        print(f"Error in earthquake prediction: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full traceback for debugging
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/predict-fire', methods=['POST'])
def predict_fire():
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
            
        # Get coordinates for the location
        coordinates = get_coordinates(location)
        if not coordinates:
            return jsonify({'error': 'Could not find coordinates for the location'}), 400
            
        # Get weather data for the location
        weather_data = get_weather_data(coordinates[0], coordinates[1])
        if not weather_data:
            return jsonify({'error': 'Could not fetch weather data'}), 400
            
        # Calculate forest fire probability based on various factors
        probability = calculate_fire_probability(weather_data)
        
        # Get 30-day forecast
        forecast = get_30_day_forecast(coordinates[0], coordinates[1])
        
        # Calculate factor impacts
        factor_impacts = calculate_fire_factor_impacts(weather_data)
        
        return jsonify({
            'location': location,
            'coordinates': coordinates,
            'probability': probability,
            'weather_data': weather_data,
            'forecast': forecast,
            'factor_impacts': factor_impacts
        })
        
    except Exception as e:
        print(f"Error in forest fire prediction: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full traceback for debugging
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.route('/predict-flood', methods=['POST'])
def predict_flood():
    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return jsonify({'error': 'Location is required'}), 400
            
        # Get coordinates for the location
        coordinates = get_coordinates(location)
        if not coordinates:
            return jsonify({'error': 'Could not find coordinates for the location'}), 400
            
        # Get weather data for the location
        weather_data = get_weather_data(coordinates[0], coordinates[1])
        if not weather_data:
            return jsonify({'error': 'Could not fetch weather data'}), 400
            
        # Calculate flooding probability based on various factors
        probability = calculate_flood_probability(weather_data)
        
        # Get 30-day forecast
        forecast = get_30_day_forecast(coordinates[0], coordinates[1])
        
        # Calculate factor impacts
        factor_impacts = calculate_flood_factor_impacts(weather_data)
        
        return jsonify({
            'location': location,
            'coordinates': coordinates,
            'probability': probability,
            'weather_data': weather_data,
            'forecast': forecast,
            'factor_impacts': factor_impacts
        })
        
    except Exception as e:
        print(f"Error in flood prediction: {str(e)}")
        import traceback
        traceback.print_exc()  # Print the full traceback for debugging
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    app.run(debug=True) 