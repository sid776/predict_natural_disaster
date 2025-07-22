from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    api_title: str = "Natural Disaster Prediction API"
    api_description: str = "Quantum-inspired natural disaster prediction using FastAPI"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }
    
    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str):
        if field_name == "debug":
            return raw_val.lower() in ("true", "1", "yes", "on")
        return raw_val
    
    # CORS Configuration
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.amplifyapp.com",  # AWS Amplify domains
        "https://*.amplifyapp.com",
        "*"  # Allow all origins in development
    ]
    
    # External APIs
    openweathermap_api_key: Optional[str] = None
    usgs_api_key: Optional[str] = None
    nasa_power_api_key: Optional[str] = None
    
    # Model Configuration
    default_model: str = "quantum"
    quantum_qubits: int = 4
    forecast_days: int = 30
    
    # Cache Configuration
    cache_ttl: int = 3600  # 1 hour in seconds
    
    # Logging
    log_level: str = "INFO"

# Create settings instance with environment variable handling
def create_settings():
    """Create settings instance with proper environment variable handling"""
    # Temporarily unset problematic environment variables
    original_debug = os.environ.get('DEBUG')
    if original_debug:
        del os.environ['DEBUG']
    
    try:
        return Settings()
    finally:
        # Restore original environment variable
        if original_debug:
            os.environ['DEBUG'] = original_debug

settings = create_settings()

# Load environment variables
def load_env_vars():
    """Load environment variables from .env file"""
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(env_file):
        from dotenv import load_dotenv
        load_dotenv(env_file)

# Load environment variables on import
load_env_vars() 