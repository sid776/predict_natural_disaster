# 🐳 Docker Setup for Natural Disaster Prediction

Simple Docker setup for the React + FastAPI Natural Disaster Prediction application.

## 🚀 Quick Start

```bash
# Build and start both services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

## 📍 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs

## 🏗️ Architecture

### Services

1. **Backend (FastAPI)**

   - Port: 8001
   - Framework: FastAPI + Python 3.10
   - Features: Quantum AI, REST API, Health checks

2. **Frontend (React)**
   - Port: 5173
   - Framework: React 18 + TypeScript + Vite
   - Features: Modern UI, Real-time predictions

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend Configuration
DEBUG=False
OPENWEATHERMAP_API_KEY=your_api_key_here
USGS_API_KEY=your_api_key_here
NASA_POWER_API_KEY=your_api_key_here

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8001
```

## 🛠️ Development

### Hot Reloading

The setup includes volume mounts for hot reloading:

- Backend changes in `backend/` directory auto-reload
- Frontend changes in `frontend/` directory auto-reload
- Quantum model changes auto-reload

### Testing

```bash
# Test backend
docker-compose exec backend python test_backend.py

# View logs
docker-compose logs -f
```

## 🚀 Production

For production deployment, comment out the volume mounts in `docker-compose.yml`:

```yaml
volumes:
  # - ./backend:/app/backend
  # - ./quantum_model.py:/app/quantum_model.py
  # - ./frontend:/app
  # - /app/node_modules
```

## 🔍 Troubleshooting

### Common Commands

```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# Stop and remove
docker-compose down
```

### Health Checks

```bash
# Check backend health
curl http://localhost:8001/api/health

# Check frontend health
curl http://localhost:5173
```

## 🧹 Cleanup

```bash
# Remove containers and networks
docker-compose down

# Remove images
docker-compose down --rmi all

# Full cleanup
docker system prune -a
```

---

**Simple and Clean Docker Setup! 🐳**
