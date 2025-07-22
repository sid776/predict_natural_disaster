# Natural Disaster Prediction API

A FastAPI-based backend for the Quantum-Inspired Natural Disaster Prediction application.

## 🚀 Features

- **RESTful API**: Clean, documented REST endpoints
- **Quantum AI Integration**: Powered by Qiskit and PennyLane
- **Multiple Prediction Models**: Quantum, LSTM, Random Forest, XGBoost, SVM, MLP
- **Real-time Weather Data**: OpenWeatherMap integration
- **Geocoding Service**: Nominatim integration for location lookup
- **Comprehensive Error Handling**: Proper HTTP status codes and error messages
- **API Documentation**: Auto-generated Swagger/OpenAPI docs
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Health Monitoring**: Service health checks and monitoring

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI applications
- **Qiskit**: Quantum computing framework
- **PennyLane**: Quantum machine learning library
- **Geopy**: Geocoding library
- **Requests**: HTTP library for external API calls

## 📦 Installation

1. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   OPENWEATHERMAP_API_KEY=your_openweathermap_api_key_here
   USGS_API_KEY=your_usgs_api_key_here
   NASA_POWER_API_KEY=your_nasa_power_api_key_here
   DEBUG=False
   ```

## 🚀 Running the Application

### Development Mode

```bash
python run.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
docker build -t disaster-prediction-api .
docker run -p 8000:8000 disaster-prediction-api
```

## 📖 API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint      | Description                     |
| ------ | ------------- | ------------------------------- |
| `GET`  | `/`           | API information                 |
| `GET`  | `/health`     | Simple health check             |
| `GET`  | `/api/health` | Detailed health check           |
| `GET`  | `/api/models` | Get available prediction models |
| `GET`  | `/api/stats`  | Get global disaster statistics  |

### Prediction Endpoints

| Method | Endpoint                   | Description              |
| ------ | -------------------------- | ------------------------ |
| `POST` | `/api/predict`             | Make disaster prediction |
| `GET`  | `/api/weather/{lat}/{lon}` | Get weather data         |
| `GET`  | `/api/geocode/{location}`  | Geocode location         |

### Example Usage

#### Make a Prediction

```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York, NY",
    "model": "quantum",
    "disaster_type": "tornado"
  }'
```

#### Get Weather Data

```bash
curl "http://localhost:8000/api/weather/40.7128/-74.0060"
```

#### Geocode Location

```bash
curl "http://localhost:8000/api/geocode/New%20York,%20NY"
```

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── predictions.py          # API routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather_service.py      # Weather API integration
│   │   ├── geocoding_service.py    # Geocoding service
│   │   └── prediction_service.py   # Prediction logic
│   ├── utils/
│   │   ├── __init__.py
│   │   └── config.py               # Configuration settings
│   ├── __init__.py
│   └── main.py                     # FastAPI application
├── requirements.txt                # Python dependencies
├── run.py                          # Startup script
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables

| Variable                 | Description            | Default |
| ------------------------ | ---------------------- | ------- |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap API key | None    |
| `USGS_API_KEY`           | USGS API key           | None    |
| `NASA_POWER_API_KEY`     | NASA POWER API key     | None    |
| `DEBUG`                  | Debug mode             | False   |
| `HOST`                   | Server host            | 0.0.0.0 |
| `PORT`                   | Server port            | 8000    |

### CORS Configuration

The API is configured to allow requests from:

- http://localhost:3000 (React dev server)
- http://localhost:5173 (Vite dev server)
- All origins in development mode

## 🧪 Testing

### Manual Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test prediction endpoint
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"location": "New York, NY", "model": "quantum", "disaster_type": "tornado"}'
```

### Automated Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 🔍 Monitoring and Logging

The API includes comprehensive logging:

- **Request Logging**: All HTTP requests and responses
- **Performance Monitoring**: Request processing times
- **Error Tracking**: Detailed error logs with stack traces
- **Service Health**: External service status monitoring

### Log Levels

- `INFO`: General application logs
- `WARNING`: Non-critical issues
- `ERROR`: Errors and exceptions
- `DEBUG`: Detailed debugging information

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.10.15-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations

1. **Environment Variables**: Set all required API keys
2. **CORS**: Configure allowed origins for production
3. **Logging**: Set appropriate log levels
4. **Security**: Use HTTPS in production
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Monitoring**: Set up application monitoring and alerting

## 🤝 Integration with Frontend

The API is designed to work seamlessly with the React frontend:

1. **CORS**: Configured to allow frontend requests
2. **Response Format**: Consistent JSON response structure
3. **Error Handling**: Proper HTTP status codes
4. **Documentation**: Auto-generated API docs for frontend developers

## 🐛 Troubleshooting

### Common Issues

1. **Import Error for quantum_model**:

   - Ensure `quantum_model.py` exists in the parent directory
   - Check Python path configuration

2. **Weather API Errors**:

   - Verify OpenWeatherMap API key
   - Check network connectivity
   - API will fall back to mock data

3. **Geocoding Errors**:

   - Check Nominatim service availability
   - Verify location format

4. **Port Already in Use**:
   - Change port in configuration
   - Kill existing process using the port

### Debug Mode

Enable debug mode for detailed error information:

```env
DEBUG=True
```

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:

1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Open an issue in the repository
