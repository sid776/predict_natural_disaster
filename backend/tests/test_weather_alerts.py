#!/usr/bin/env python3
"""
Test script to check if weather alerts API is working
"""

import sys
import os
import requests
from datetime import datetime

# Add the parent directory to the path so we can import the services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.weather_alerts_service import weather_alerts_service

def test_weather_alerts_service():
    """Test the weather alerts service directly"""
    print("🔍 Testing Weather Alerts Service...")
    
    # Test coordinates (Miami - hurricane prone area)
    lat, lon = 25.7617, -80.1918
    
    try:
        alerts = weather_alerts_service.get_alerts_for_location(lat, lon)
        
        if alerts:
            print("✅ Weather Alerts Service working!")
            print(f"   Found {len(alerts)} alerts")
            for i, alert in enumerate(alerts[:3]):  # Show first 3 alerts
                print(f"   Alert {i+1}: {alert.event} - {alert.severity}")
            return True
        else:
            print("✅ Weather Alerts Service working (no active alerts in area)")
            return True
            
    except Exception as e:
        print(f"❌ Weather Alerts Service error: {str(e)}")
        return False

def test_weather_alerts_by_region():
    """Test weather alerts by region"""
    print("\n🔍 Testing Weather Alerts by Region...")
    
    try:
        alerts = weather_alerts_service.get_alerts_by_region("conus")
        
        if alerts:
            print("✅ Weather Alerts by Region working!")
            print(f"   Found {len(alerts)} alerts for continental US")
            for i, alert in enumerate(alerts[:3]):  # Show first 3 alerts
                print(f"   Alert {i+1}: {alert.event} - {alert.areas}")
            return True
        else:
            print("✅ Weather Alerts by Region working (no active alerts)")
            return True
            
    except Exception as e:
        print(f"❌ Weather Alerts by Region error: {str(e)}")
        return False

def test_weather_alerts_by_event_type():
    """Test weather alerts by event type"""
    print("\n🔍 Testing Weather Alerts by Event Type...")
    
    try:
        alerts = weather_alerts_service.get_alerts_by_event_type("Severe Thunderstorm Warning")
        
        if alerts:
            print("✅ Weather Alerts by Event Type working!")
            print(f"   Found {len(alerts)} Severe Thunderstorm Warnings")
            for i, alert in enumerate(alerts[:3]):  # Show first 3 alerts
                print(f"   Alert {i+1}: {alert.areas} - {alert.effective}")
            return True
        else:
            print("✅ Weather Alerts by Event Type working (no Severe Thunderstorm Warnings)")
            return True
            
    except Exception as e:
        print(f"❌ Weather Alerts by Event Type error: {str(e)}")
        return False

def test_direct_api_calls():
    """Test direct API calls to verify endpoints are accessible"""
    print("\n🔍 Testing direct API calls...")
    
    # Test National Weather Service API directly
    print("Testing National Weather Service API directly...")
    try:
        url = "https://api.weather.gov/alerts/active"
        params = {"status": "actual"}
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ National Weather Service API endpoint accessible")
            data = response.json()
            if "features" in data:
                print(f"   Found {len(data['features'])} active alerts")
        else:
            print(f"❌ National Weather Service API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ National Weather Service API connection error: {str(e)}")
    
    # Test specific location
    print("Testing National Weather Service API for specific location...")
    try:
        url = "https://api.weather.gov/alerts/active"
        params = {
            "point": "25.7617,-80.1918",
            "status": "actual"
        }
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ National Weather Service API location endpoint accessible")
            data = response.json()
            if "features" in data:
                print(f"   Found {len(data['features'])} alerts for Miami area")
        else:
            print(f"❌ National Weather Service API location endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ National Weather Service API location endpoint connection error: {str(e)}")

def test_api_connection():
    """Test the API connection method"""
    print("\n🔍 Testing API Connection Method...")
    
    try:
        is_connected = weather_alerts_service.test_api_connection()
        if is_connected:
            print("✅ Weather Alerts API connection test passed")
            return True
        else:
            print("❌ Weather Alerts API connection test failed")
            return False
    except Exception as e:
        print(f"❌ Weather Alerts API connection test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Weather Alerts API Connectivity")
    print("=" * 50)
    
    results = {
        'weather_alerts_service': test_weather_alerts_service(),
        'weather_alerts_by_region': test_weather_alerts_by_region(),
        'weather_alerts_by_event_type': test_weather_alerts_by_event_type(),
        'api_connection': test_api_connection()
    }
    
    # Test direct API calls
    test_direct_api_calls()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test.upper():25} {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} weather alerts tests working")
    
    if passed_tests == total_tests:
        print("🎉 All weather alerts tests are working correctly!")
    else:
        print("⚠️  Some weather alerts tests have issues. Check the logs above.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 