#!/usr/bin/env python3
"""
Test script to check if API endpoints are working through FastAPI server
"""

import sys
import os
import requests
import json
from datetime import datetime

# Add the parent directory to the path so we can import the app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_endpoints():
    """Test the API endpoints"""
    print("🚀 Testing API Endpoints")
    print("=" * 50)
    
    # Base URL for the API
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working!")
            print(f"   Status: {data.get('data', {}).get('status', 'unknown')}")
            print(f"   Services: {data.get('data', {}).get('services', {})}")
        else:
            print(f"❌ Health endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {str(e)}")
    
    # Test weather alerts endpoint
    print("\n🔍 Testing Weather Alerts Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/weather-alerts/Miami%2C%20FL", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Weather alerts endpoint working!")
            alerts = data.get('data', {}).get('alerts', [])
            print(f"   Found {len(alerts)} alerts for Miami, FL")
            for i, alert in enumerate(alerts[:2]):
                print(f"   Alert {i+1}: {alert.get('event', 'Unknown')}")
        else:
            print(f"❌ Weather alerts endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Weather alerts endpoint error: {str(e)}")
    
    # Test weather alerts by coordinates endpoint
    print("\n🔍 Testing Weather Alerts by Coordinates Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/weather-alerts/coordinates/25.7617/-80.1918", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Weather alerts by coordinates endpoint working!")
            alerts = data.get('data', {}).get('alerts', [])
            print(f"   Found {len(alerts)} alerts for coordinates (25.7617, -80.1918)")
        else:
            print(f"❌ Weather alerts by coordinates endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Weather alerts by coordinates endpoint error: {str(e)}")
    
    # Test geocoding endpoint
    print("\n🔍 Testing Geocoding Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/geocode/New%20York%2C%20NY", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Geocoding endpoint working!")
            location_data = data.get('data', {})
            print(f"   Location: {location_data.get('display_name', 'Unknown')}")
            print(f"   Coordinates: ({location_data.get('lat', 'N/A')}, {location_data.get('lon', 'N/A')})")
        else:
            print(f"❌ Geocoding endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Geocoding endpoint error: {str(e)}")
    
    # Test weather endpoint
    print("\n🔍 Testing Weather Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/weather/40.7128/-74.0060", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Weather endpoint working!")
            weather_data = data.get('data', {})
            if weather_data:
                print(f"   Temperature: {weather_data.get('main', {}).get('temp', 'N/A')}°C")
                print(f"   Humidity: {weather_data.get('main', {}).get('humidity', 'N/A')}%")
        else:
            print(f"❌ Weather endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Weather endpoint error: {str(e)}")
    
    # Test models endpoint
    print("\n🔍 Testing Models Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/models", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Models endpoint working!")
            models = data.get('data', [])
            print(f"   Available models: {', '.join(models)}")
        else:
            print(f"❌ Models endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Models endpoint error: {str(e)}")
    
    # Test data sources endpoint
    print("\n🔍 Testing Data Sources Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/data-sources", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Data sources endpoint working!")
            sources = data.get('data', [])
            print(f"   Available data sources: {len(sources)}")
            for source in sources:
                print(f"     - {source.get('name', 'Unknown')}: {source.get('description', 'No description')}")
        else:
            print(f"❌ Data sources endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Data sources endpoint error: {str(e)}")
    
    # Test stats endpoint
    print("\n🔍 Testing Stats Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Stats endpoint working!")
            stats = data.get('data', {})
            if stats:
                print("   Global disaster statistics available")
        else:
            print(f"❌ Stats endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {str(e)}")

def test_prediction_endpoint():
    """Test the prediction endpoint"""
    print("\n🔍 Testing Prediction Endpoint...")
    
    base_url = "http://localhost:8000"
    
    # Test prediction request
    prediction_data = {
        "location": "Miami, FL",
        "model": "quantum",
        "disaster_type": "tornado",
        "data_source": "data_fusion"
    }
    
    try:
        response = requests.post(
            f"{base_url}/api/predict",
            json=prediction_data,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Prediction endpoint working!")
            prediction = data.get('data', {})
            if prediction:
                probability = prediction.get('probability', 0)
                print(f"   Prediction probability: {probability:.2%}")
                print(f"   Disaster type: {prediction.get('metadata', {}).get('disaster_type', 'Unknown')}")
        else:
            print(f"❌ Prediction endpoint returned status {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Prediction endpoint error: {str(e)}")

def main():
    """Run all API endpoint tests"""
    print("🚀 Testing API Endpoints")
    print("=" * 50)
    
    # Test basic endpoints
    test_api_endpoints()
    
    # Test prediction endpoint
    test_prediction_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 API ENDPOINT TESTING COMPLETE")
    print("=" * 50)
    print("💡 Note: Make sure the FastAPI server is running on localhost:8000")
    print("   Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 