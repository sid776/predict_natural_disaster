#!/usr/bin/env python3
"""
End-to-End Test for Multi-County Prediction Feature

This test validates the complete multi-county prediction flow:
1. API endpoint functionality
2. Dynamic county discovery
3. Weather data integration
4. Response validation
5. Error handling
"""

import sys
import os
import asyncio
import pytest
from typing import Dict, Any
import requests
import json
from datetime import datetime

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.models.schemas import (
    MultiCountyPredictionResponse, CountyInfo, CountyPrediction, 
    DisasterProgression, ApiResponse
)


class TestMultiCountyPrediction:
    """End-to-end test suite for multi-county prediction feature"""
    
    def __init__(self):
        self.base_url = "http://localhost:8001"
        self.test_locations = [
            "Miami, FL",
            "Los Angeles, CA", 
            "New York, NY",
            "Austin, TX",
            "Denver, CO"
        ]
        self.disaster_types = ["tornado", "earthquake", "wildfire", "flood"]
        
    def test_api_health(self):
        """Test that the API is running and healthy"""
        print("🔍 Testing API health...")
        
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            
            data = response.json()
            assert data["success"] == True, "Health check should return success=True"
            assert "services" in data["data"], "Health response should include services"
            
            print("✅ API health check passed")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API health check failed: {e}")
            return False
    
    def test_multi_county_endpoint_exists(self):
        """Test that the multi-county endpoint exists and is accessible"""
        print("🔍 Testing multi-county endpoint accessibility...")
        
        try:
            # Test with a simple location
            test_location = "Miami, FL"
            url = f"{self.base_url}/api/multi-county-prediction/{test_location}"
            params = {
                "disaster_type": "tornado",
                "model": "quantum",
                "data_source": "openweathermap"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            # Should either return 200 (success) or 400 (validation error)
            # Both are acceptable as long as the endpoint exists
            assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"
            
            print("✅ Multi-county endpoint is accessible")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Multi-county endpoint test failed: {e}")
            return False
    
    def test_successful_multi_county_prediction(self):
        """Test a successful multi-county prediction"""
        print("🔍 Testing successful multi-county prediction...")
        
        try:
            test_location = "Miami, FL"
            url = f"{self.base_url}/api/multi-county-prediction/{test_location}"
            params = {
                "disaster_type": "tornado",
                "model": "quantum",
                "data_source": "openweathermap"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate API response structure
                assert data["success"] == True, "Response should indicate success"
                assert "data" in data, "Response should contain data field"
                assert "message" in data, "Response should contain message field"
                
                # Validate multi-county response structure
                multi_county_data = data["data"]
                assert "center_location" in multi_county_data, "Missing center_location"
                assert "disaster_type" in multi_county_data, "Missing disaster_type"
                assert "progression" in multi_county_data, "Missing progression"
                assert "evacuation_recommendations" in multi_county_data, "Missing evacuation_recommendations"
                assert "timestamp" in multi_county_data, "Missing timestamp"
                
                # Validate progression structure
                progression = multi_county_data["progression"]
                assert "direction_degrees" in progression, "Missing direction_degrees"
                assert "speed_mph" in progression, "Missing speed_mph"
                assert "estimated_duration_hours" in progression, "Missing estimated_duration_hours"
                assert "affected_counties" in progression, "Missing affected_counties"
                
                # Validate that we have at least one affected county
                affected_counties = progression["affected_counties"]
                assert len(affected_counties) > 0, "Should have at least one affected county"
                
                # Validate first county structure
                first_county = affected_counties[0]
                assert "county" in first_county, "County missing county info"
                assert "predicted_impact_time_hours" in first_county, "Missing impact time"
                assert "risk_level" in first_county, "Missing risk level"
                assert "probability" in first_county, "Missing probability"
                assert "weather_conditions" in first_county, "Missing weather conditions"
                assert "evacuation_priority" in first_county, "Missing evacuation priority"
                
                # Validate county info structure
                county_info = first_county["county"]
                assert "name" in county_info, "Missing county name"
                assert "coordinates" in county_info, "Missing coordinates"
                assert "distance_miles" in county_info, "Missing distance"
                
                # Validate coordinates structure
                coordinates = county_info["coordinates"]
                assert "lat" in coordinates, "Missing latitude"
                assert "lon" in coordinates, "Missing longitude"
                
                # Validate evacuation recommendations
                evacuation_recs = multi_county_data["evacuation_recommendations"]
                assert "immediate_evacuation" in evacuation_recs, "Missing immediate evacuation"
                assert "prepare_to_evacuate" in evacuation_recs, "Missing prepare to evacuate"
                assert "monitor_situation" in evacuation_recs, "Missing monitor situation"
                
                print(f"✅ Successful multi-county prediction for {test_location}")
                print(f"   📍 Found {len(affected_counties)} affected counties")
                print(f"   🌪️ Disaster type: {multi_county_data['disaster_type']}")
                print(f"   ⚡ Speed: {progression['speed_mph']:.1f} mph")
                print(f"   🧭 Direction: {progression['direction_degrees']:.1f}°")
                print(f"   ⏰ Duration: {progression['estimated_duration_hours']:.1f} hours")
                
                return True
                
            else:
                print(f"⚠️ Multi-county prediction returned status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Multi-county prediction test failed: {e}")
            return False
    
    def test_different_disaster_types(self):
        """Test multi-county prediction with different disaster types"""
        print("🔍 Testing different disaster types...")
        
        test_location = "Los Angeles, CA"
        success_count = 0
        
        for disaster_type in self.disaster_types:
            try:
                url = f"{self.base_url}/api/multi-county-prediction/{test_location}"
                params = {
                    "disaster_type": disaster_type,
                    "model": "quantum",
                    "data_source": "openweathermap"
                }
                
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data["success"]:
                        print(f"✅ {disaster_type.capitalize()} prediction successful")
                        success_count += 1
                    else:
                        print(f"⚠️ {disaster_type.capitalize()} prediction failed")
                else:
                    print(f"⚠️ {disaster_type.capitalize()} returned status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {disaster_type.capitalize()} test failed: {e}")
        
        print(f"📊 Disaster type test results: {success_count}/{len(self.disaster_types)} successful")
        return success_count > 0
    
    def test_different_locations(self):
        """Test multi-county prediction with different locations"""
        print("🔍 Testing different locations...")
        
        disaster_type = "tornado"
        success_count = 0
        
        for location in self.test_locations:
            try:
                url = f"{self.base_url}/api/multi-county-prediction/{location}"
                params = {
                    "disaster_type": disaster_type,
                    "model": "quantum",
                    "data_source": "openweathermap"
                }
                
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if data["success"]:
                        counties = data["data"]["progression"]["affected_counties"]
                        print(f"✅ {location}: {len(counties)} counties found")
                        success_count += 1
                    else:
                        print(f"⚠️ {location}: prediction failed")
                else:
                    print(f"⚠️ {location}: status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ {location} test failed: {e}")
        
        print(f"📊 Location test results: {success_count}/{len(self.test_locations)} successful")
        return success_count > 0
    
    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        print("🔍 Testing error handling...")
        
        # Test with invalid location
        try:
            url = f"{self.base_url}/api/multi-county-prediction/InvalidLocation123"
            params = {
                "disaster_type": "tornado",
                "model": "quantum",
                "data_source": "openweathermap"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            # Should return 400 for invalid location
            if response.status_code == 400:
                print("✅ Invalid location properly handled")
                return True
            else:
                print(f"⚠️ Unexpected status for invalid location: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error handling test failed: {e}")
            return False
    
    def test_response_validation(self):
        """Test that responses conform to expected schema"""
        print("🔍 Testing response validation...")
        
        try:
            test_location = "New York, NY"
            url = f"{self.base_url}/api/multi-county-prediction/{test_location}"
            params = {
                "disaster_type": "earthquake",
                "model": "quantum",
                "data_source": "openweathermap"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate that the response can be parsed as our expected schema
                try:
                    # Test that the data structure is valid
                    multi_county_data = data["data"]
                    
                    # Check required fields exist
                    required_fields = [
                        "center_location", "disaster_type", "progression", 
                        "evacuation_recommendations", "timestamp"
                    ]
                    
                    for field in required_fields:
                        assert field in multi_county_data, f"Missing required field: {field}"
                    
                    # Check progression fields
                    progression = multi_county_data["progression"]
                    progression_fields = [
                        "direction_degrees", "speed_mph", 
                        "estimated_duration_hours", "affected_counties"
                    ]
                    
                    for field in progression_fields:
                        assert field in progression, f"Missing progression field: {field}"
                    
                    # Check data types
                    assert isinstance(multi_county_data["center_location"], str)
                    assert isinstance(multi_county_data["disaster_type"], str)
                    assert isinstance(progression["direction_degrees"], (int, float))
                    assert isinstance(progression["speed_mph"], (int, float))
                    assert isinstance(progression["estimated_duration_hours"], (int, float))
                    assert isinstance(progression["affected_counties"], list)
                    
                    print("✅ Response validation passed")
                    return True
                    
                except (KeyError, TypeError, AssertionError) as e:
                    print(f"❌ Response validation failed: {e}")
                    return False
            else:
                print(f"⚠️ Response validation skipped - status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Response validation test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all end-to-end tests"""
        print("🚀 Starting Multi-County Prediction End-to-End Tests")
        print("=" * 60)
        
        tests = [
            ("API Health", self.test_api_health),
            ("Endpoint Accessibility", self.test_multi_county_endpoint_exists),
            ("Successful Prediction", self.test_successful_multi_county_prediction),
            ("Different Disaster Types", self.test_different_disaster_types),
            ("Different Locations", self.test_different_locations),
            ("Error Handling", self.test_error_handling),
            ("Response Validation", self.test_response_validation)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🧪 Running: {test_name}")
            try:
                result = test_func()
                results.append((test_name, result))
                status = "✅ PASSED" if result else "❌ FAILED"
                print(f"   {status}")
            except Exception as e:
                print(f"   ❌ FAILED with exception: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<25} {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Multi-county prediction feature is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the implementation.")
        
        return passed == total


def main():
    """Main function to run the tests"""
    test_suite = TestMultiCountyPrediction()
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎯 Multi-County Prediction Feature: READY FOR PRODUCTION")
        return 0
    else:
        print("\n🔧 Multi-County Prediction Feature: NEEDS ATTENTION")
        return 1


if __name__ == "__main__":
    exit(main()) 