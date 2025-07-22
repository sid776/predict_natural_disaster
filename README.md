# 🌪️ Quantum-Inspired Natural Disaster Prediction

A modern web application that uses quantum-inspired machine learning algorithms to predict natural disasters including tornadoes, earthquakes, wildfires, and floods.

## 🏗️ Architecture

This project has been migrated from a monolithic Dash application to a modern **React + FastAPI** architecture:

- **Frontend**: React 18 + TypeScript + Vite + Material-UI
- **Backend**: FastAPI + Python 3.10 + Qiskit + PennyLane
- **Data Sources**: OpenWeatherMap API, USGS, NASA POWER
- **Quantum Computing**: Qiskit 0.45.1 + PennyLane 0.34.0

## 🚀 Quick Start

### Option 1: Start Both Services (Recommended)

```bash
./start_services.sh
```

### Option 2: Start Services Manually

#### Backend (FastAPI)

```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

#### Frontend (React)

```bash
cd frontend
npm run dev
```

## 📍 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/api/health

## 🛠️ Features

### Frontend (React)

- **Modern UI**: Material-UI components with responsive design
- **Real-time Predictions**: Live disaster probability calculations
- **Interactive Charts**: Probability gauges, forecast charts, factor analysis
- **Multiple Disaster Types**: Tornado, Earthquake, Wildfire, Flood
- **Model Selection**: Choose from 6 different prediction models
- **Location Search**: Geocoding with autocomplete
- **30-Day Forecasts**: Extended prediction timelines

### Backend (FastAPI)

- **RESTful API**: Clean, documented endpoints
- **Quantum AI**: Powered by Qiskit and PennyLane
- **Multiple Models**: Quantum, LSTM, Random Forest, XGBoost, SVM, MLP
- **Real-time Weather**: OpenWeatherMap integration
- **Geocoding**: Nominatim integration
- **Comprehensive Error Handling**: Proper HTTP status codes
- **Auto-generated Docs**: Swagger/OpenAPI documentation

## 📁 Project Structure

```
predict_natural_disaster/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Utility functions
│   │   └── types/           # TypeScript types
│   ├── package.json
│   └── README.md
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   ├── models/          # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── utils/           # Configuration
│   ├── requirements.txt
│   └── README.md
├── data_sources/            # Data source adapters
├── quantum_model.py         # Quantum prediction model
├── app.py                   # Legacy Dash app (deprecated)
├── start_services.sh        # Service startup script
└── README.md               # This file
```

## 🔧 API Endpoints

### Core Endpoints

- `GET /api/health` - Health check
- `GET /api/models` - Available prediction models
- `GET /api/stats` - Global disaster statistics

### Prediction Endpoints

- `POST /api/predict` - Make disaster prediction
- `GET /api/weather/{lat}/{lon}` - Get weather data
- `GET /api/geocode/{location}` - Geocode location

### Example API Usage

```bash
# Make a prediction
curl -X POST "http://localhost:8001/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York, NY",
    "model": "quantum",
    "disaster_type": "tornado"
  }'

# Get weather data
curl "http://localhost:8001/api/weather/40.7128/-74.0060"

# Geocode location
curl "http://localhost:8001/api/geocode/New%20York,%20NY"
```

## 🧪 Testing

### Backend Testing

```bash
cd backend
python test_backend.py
```

### Frontend Testing

```bash
cd frontend
npm test
```

## 🔑 Environment Variables

### Backend (.env in backend directory)

```env
OPENWEATHERMAP_API_KEY=your_api_key_here
USGS_API_KEY=your_api_key_here
NASA_POWER_API_KEY=your_api_key_here
DEBUG=False
```

### Frontend (.env in frontend directory)

```env
VITE_API_BASE_URL=http://localhost:8001
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build
```

### Production Considerations

1. Set up proper environment variables
2. Configure CORS for production domains
3. Use HTTPS in production
4. Set up monitoring and logging
5. Implement rate limiting
6. Configure proper database (if needed)

## 🔬 Quantum Computing Integration

The application uses quantum-inspired algorithms:

- **Qiskit**: IBM's quantum computing framework
- **PennyLane**: Quantum machine learning library
- **Quantum Circuits**: 4-qubit circuits for feature encoding
- **Quantum Feature Maps**: Weather data to quantum states
- **Quantum Measurements**: Expectation values for predictions

## 📊 Prediction Models

1. **Quantum AI**: Quantum-inspired machine learning
2. **LSTM**: Long Short-Term Memory neural networks
3. **Random Forest**: Ensemble learning method
4. **XGBoost**: Gradient boosting framework
5. **SVM**: Support Vector Machine
6. **MLP/ANN**: Multi-layer Perceptron

## 🌍 Supported Disaster Types

- **Tornado**: Wind-based predictions using temperature, humidity, pressure, wind speed
- **Earthquake**: Seismic predictions using atmospheric pressure and humidity
- **Wildfire**: Fire risk using temperature, humidity, and wind speed
- **Flood**: Flooding predictions using humidity, pressure, and temperature

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- **API Documentation**: http://localhost:8001/docs
- **Frontend Issues**: Check browser console
- **Backend Issues**: Check server logs
- **Quantum Model Issues**: Check quantum_model.py

## 🔄 Migration Notes

This project was migrated from a monolithic Dash application to a modern React + FastAPI architecture:

- **Before**: Single Dash app with embedded Flask server
- **After**: Separated frontend (React) and backend (FastAPI)
- **Benefits**: Better scalability, maintainability, and developer experience
- **Legacy**: Original `app.py` is preserved for reference

---

**Built with ❤️ using Quantum Computing and Modern Web Technologies**
