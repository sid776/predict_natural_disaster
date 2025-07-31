#!/usr/bin/env python3
"""
Test script to check if all data sources are working via API calls
"""

import sys
import os
import requests
from datetime import datetime

# Add the parent directory to the path so we can import the data sources
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_sources.openweathermap_source import OpenWeatherMapSource
from data_sources.usgs_source import USGSEarthquakeSource
from data_sources.nasa_power_source import NASAPowerSource
from data_sources.data_fusion import DataFusion

def test_openweathermap():
    """Test OpenWeatherMap API"""
    print("🔍 Testing OpenWeatherMap API...")
    
    # Test coordinates (New York City)
    lat, lon = 40.7128, -74.0060
    
    # You'll need to set your API key here or get it from environment
    api_key = os.getenv('OPENWEATHERMAP_API_KEY', 'your_api_key_here')
    
    if api_key == 'your_api_key_here':
        print("❌ OpenWeatherMap API key not set. Set OPENWEATHERMAP_API_KEY environment variable.")
        return False
    
    try:
        source = OpenWeatherMapSource(api_key)
        data = source.fetch((lat, lon), 'tornado')
        
        if data:
            print("✅ OpenWeatherMap API working!")
            print(f"   Temperature: {data.get('temperature', 'N/A')}°C")
            print(f"   Humidity: {data.get('humidity', 'N/A')}%")
            print(f"   Pressure: {data.get('pressure', 'N/A')} hPa")
            print(f"   Wind Speed: {data.get('wind_speed', 'N/A')} m/s")
            return True
        else:
            print("❌ OpenWeatherMap API returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ OpenWeatherMap API error: {str(e)}")
        return False

def test_usgs():
    """Test USGS Earthquake API"""
    print("\n🔍 Testing USGS Earthquake API...")
    
    # Test coordinates (San Francisco - earthquake prone area)
    lat, lon = 37.7749, -122.4194
    
    try:
        source = USGSEarthquakeSource()
        data = source.fetch((lat, lon), 'earthquake')
        
        if data:
            print("✅ USGS Earthquake API working!")
            print(f"   Magnitude: {data.get('magnitude', 'N/A')}")
            print(f"   Depth: {data.get('depth', 'N/A')} km")
            print(f"   Time: {data.get('time', 'N/A')}")
            return True
        else:
            print("✅ USGS Earthquake API working (no recent earthquakes in area)")
            return True
            
    except Exception as e:
        print(f"❌ USGS Earthquake API error: {str(e)}")
        return False

def test_nasa_power():
    """Test NASA POWER API"""
    print("\n🔍 Testing NASA POWER API...")
    
    # Test coordinates (Miami)
    lat, lon = 25.7617, -80.1918
    
    try:
        source = NASAPowerSource()
        data = source.fetch((lat, lon), 'tornado')
        
        if data:
            print("✅ NASA POWER API working!")
            print(f"   Temperature: {data.get('nasa_temperature', 'N/A')}°C")
            print(f"   Wind Speed: {data.get('nasa_wind_speed', 'N/A')} m/s")
            print(f"   Precipitation: {data.get('nasa_precipitation', 'N/A')} mm")
            print(f"   Solar Radiation: {data.get('nasa_solar_radiation', 'N/A')} W/m²")
            return True
        else:
            print("❌ NASA POWER API returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ NASA POWER API error: {str(e)}")
        return False

def test_data_fusion():
    """Test Data Fusion (combining all sources)"""
    print("\n🔍 Testing Data Fusion...")
    
    # Test coordinates (Chicago)
    lat, lon = 41.8781, -87.6298
    
    # You'll need to set your API key here or get it from environment
    api_key = os.getenv('OPENWEATHERMAP_API_KEY', 'your_api_key_here')
    
    if api_key == 'your_api_key_here':
        print("❌ OpenWeatherMap API key not set. Skipping Data Fusion test.")
        return False
    
    try:
        fusion = DataFusion(api_key)
        data = fusion.fetch_all((lat, lon), 'tornado')
        
        if data:
            print("✅ Data Fusion working!")
            print(f"   Total features: {len(data)}")
            print("   Features found:")
            for key, value in data.items():
                print(f"     {key}: {value}")
            return True
        else:
            print("❌ Data Fusion returned empty data")
            return False
            
    except Exception as e:
        print(f"❌ Data Fusion error: {str(e)}")
        return False

def test_direct_api_calls():
    """Test direct API calls to verify endpoints are accessible"""
    print("\n🔍 Testing direct API calls...")
    
    # Test OpenWeatherMap API directly
    print("Testing OpenWeatherMap API directly...")
    api_key = os.getenv('OPENWEATHERMAP_API_KEY', 'your_api_key_here')
    if api_key != 'your_api_key_here':
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat=40.7128&lon=-74.0060&appid={api_key}&units=metric"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ OpenWeatherMap API endpoint accessible")
            else:
                print(f"❌ OpenWeatherMap API returned status {response.status_code}")
        except Exception as e:
            print(f"❌ OpenWeatherMap API connection error: {str(e)}")
    else:
        print("⚠️  Skipping OpenWeatherMap direct test (no API key)")
    
    # Test USGS API directly
    print("Testing USGS Earthquake API directly...")
    try:
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=37.7749&longitude=-122.4194&maxradiuskm=100&limit=1&orderby=time"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ USGS Earthquake API endpoint accessible")
        else:
            print(f"❌ USGS Earthquake API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ USGS Earthquake API connection error: {str(e)}")
    
    # Test NASA POWER API directly
    print("Testing NASA POWER API directly...")
    try:
        url = "https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,WS2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN&community=RE&longitude=-80.1918&latitude=25.7617&format=JSON&start=20230101&end=20230102"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print("✅ NASA POWER API endpoint accessible")
        else:
            print(f"❌ NASA POWER API returned status {response.status_code}")
    except Exception as e:
        print(f"❌ NASA POWER API connection error: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Testing Data Sources API Connectivity")
    print("=" * 50)
    
    results = {
        'openweathermap': test_openweathermap(),
        'usgs': test_usgs(),
        'nasa_power': test_nasa_power(),
        'data_fusion': test_data_fusion()
    }
    
    # Test direct API calls
    test_direct_api_calls()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    for source, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{source.upper():15} {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} data sources working")
    
    if passed_tests == total_tests:
        print("🎉 All data sources are working correctly!")
    else:
        print("⚠️  Some data sources have issues. Check the logs above.")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    if not results['openweathermap']:
        print("- Set OPENWEATHERMAP_API_KEY environment variable for weather data")
    if not results['usgs']:
        print("- Check internet connectivity for USGS API")
    if not results['nasa_power']:
        print("- Check internet connectivity for NASA POWER API")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 