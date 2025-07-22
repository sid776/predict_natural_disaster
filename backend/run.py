#!/usr/bin/env python3
"""
Startup script for the Natural Disaster Prediction API
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import the quantum model
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

def main():
    """Main function to start the FastAPI server"""
    print("🚀 Natural Disaster Prediction API")
    print("===================================")
    
    # Check if quantum model exists
    quantum_model_path = parent_dir / "quantum_model.py"
    if not quantum_model_path.exists():
        print("❌ Error: quantum_model.py not found in parent directory")
        print(f"   Expected location: {quantum_model_path}")
        sys.exit(1)
    
    print("✅ Quantum model found")
    
    # Import and check settings
    try:
        from app.utils.config import settings
        print(f"📋 API Version: {settings.api_version}")
        print(f"🔧 Debug Mode: {settings.debug}")
        print(f"🌐 Host: {settings.host}")
        print(f"🔌 Port: {settings.port}")
        
        # Check API keys
        if not settings.openweathermap_api_key or settings.openweathermap_api_key == "your_openweathermap_api_key_here":
            print("⚠️  Warning: OpenWeatherMap API key not configured")
            print("   Weather data will use mock data")
        else:
            print("✅ OpenWeatherMap API key configured")
            
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")
        sys.exit(1)
    
    print("\n🚀 Starting server...")
    print("📖 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Health check available at: http://localhost:8000/api/health")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.lower(),
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 