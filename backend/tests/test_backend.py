#!/usr/bin/env python3
"""
Simple test script to check backend functionality
"""

import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def test_imports():
    """Test if all imports work"""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from app.utils.config import settings
        print("✅ Config imported successfully")
        
        from app.models.schemas import PredictionRequest, PredictionModel, DisasterType
        print("✅ Schemas imported successfully")
        
        from app.services.weather_service import weather_service
        print("✅ Weather service imported successfully")
        
        from app.services.geocoding_service import geocoding_service
        print("✅ Geocoding service imported successfully")
        
        from app.services.prediction_service import prediction_service
        print("✅ Prediction service imported successfully")
        
        from app.main import app
        print("✅ FastAPI app imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_quantum_model():
    """Test quantum model import"""
    try:
        print("\nTesting quantum model...")
        from quantum_model import QuantumTornadoPredictor
        predictor = QuantumTornadoPredictor()
        print("✅ Quantum model imported and instantiated successfully")
        return True
    except Exception as e:
        print(f"❌ Quantum model error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Backend Test Suite")
    print("=" * 30)
    
    success = True
    success &= test_imports()
    success &= test_quantum_model()
    
    if success:
        print("\n🎉 All tests passed! Backend should work.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
        sys.exit(1) 