from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import time
from contextlib import asynccontextmanager

from app.utils.config import settings
from app.api.predictions import router as predictions_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Natural Disaster Prediction API...")
    logger.info(f"API Version: {settings.api_version}")
    logger.info(f"Debug Mode: {settings.debug}")
    
    # Test external services
    try:
        from app.services.weather_service import weather_service
        from app.services.geocoding_service import geocoding_service
        
        weather_ok = weather_service.test_api_connection()
        geocoding_ok = geocoding_service.test_service()
        
        logger.info(f"Weather API: {'OK' if weather_ok else 'FAILED'}")
        logger.info(f"Geocoding Service: {'OK' if geocoding_ok else 'FAILED'}")
        
    except Exception as e:
        logger.error(f"Error testing external services: {str(e)}")
    
    logger.info("Natural Disaster Prediction API started successfully!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Natural Disaster Prediction API...")

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    
    return response

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "detail": exc.errors(),
            "message": "Invalid request data"
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": f"HTTP {exc.status_code}",
            "detail": exc.detail,
            "message": "Request failed"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
            "message": "Internal server error"
        }
    )

# Include routers
app.include_router(predictions_router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Natural Disaster Prediction API",
        "version": settings.api_version,
        "description": settings.api_description,
        "docs": "/docs",
        "health": "/api/health"
    }

# Health check endpoint (simple)
@app.get("/health")
async def simple_health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

# API health check endpoint for Railway
@app.get("/api/health")
async def api_health_check():
    """API health check endpoint for Railway"""
    return {"status": "healthy", "timestamp": time.time()}

# API documentation customization
@app.get("/docs", include_in_schema=False)
async def custom_docs():
    """Custom API documentation"""
    return {
        "message": "API Documentation",
        "swagger_ui": "/docs",
        "redoc": "/redoc",
        "openapi_json": "/openapi.json"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    ) 