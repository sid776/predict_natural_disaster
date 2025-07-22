# Natural Disaster Prediction Frontend

A React-based frontend for the Quantum-Inspired Natural Disaster Prediction application.

## 🚀 Features

- **Real-time Predictions**: Get instant disaster probability predictions
- **Multiple Disaster Types**: Tornado, Earthquake, Wildfire, and Flood analysis
- **Quantum AI Models**: Powered by Qiskit and PennyLane
- **Interactive Visualizations**: Charts and gauges for data visualization
- **Responsive Design**: Works on desktop and mobile devices
- **Weather Integration**: Real-time weather data from OpenWeatherMap

## 🛠️ Technology Stack

- **React 18** with TypeScript
- **Material-UI** for UI components
- **Recharts** for data visualization
- **Axios** for API communication
- **Vite** for build tooling

## 📦 Installation

1. **Install dependencies**:

   ```bash
   npm install
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:

   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_NODE_ENV=development
   VITE_ENABLE_DEBUG_MODE=true
   ```

3. **Start development server**:

   ```bash
   npm run dev
   ```

4. **Build for production**:
   ```bash
   npm run build
   ```

## 🏗️ Project Structure

```
src/
├── components/          # React components
│   ├── Layout/         # Layout components (Navbar, Sidebar)
│   └── Charts/         # Chart components (Gauge, Forecast, Factors)
├── hooks/              # Custom React hooks
├── services/           # API services
├── types/              # TypeScript type definitions
├── utils/              # Utility functions and constants
└── pages/              # Page components (if needed)
```

## 🎨 Components

### Layout Components

- **Navbar**: Application header with title and branding
- **Sidebar**: Input controls and forecast display

### Chart Components

- **ProbabilityGauge**: Circular gauge showing disaster probability
- **ForecastChart**: Line chart for 30-day forecast
- **FactorsChart**: Bar chart for weather factor impacts

### Custom Hooks

- **usePrediction**: Single prediction hook
- **useBatchPrediction**: Batch predictions for all disaster types

## 🔧 Configuration

### API Configuration

The frontend communicates with the FastAPI backend through the `ApiService`. Configure the API base URL in your environment variables.

### Theme Configuration

Colors and styling are defined in `src/utils/constants.ts`. The application uses a consistent color palette for different disaster types.

## 📱 Usage

1. **Enter Location**: Type a city and state (e.g., "New York, NY")
2. **Select Model**: Choose from Quantum AI, LSTM, Random Forest, etc.
3. **Click Predict**: Get predictions for all disaster types
4. **View Results**: Switch between tabs to see different disaster analyses
5. **Explore Charts**: Interactive visualizations show probability, forecast, and factors

## 🔌 API Integration

The frontend expects the following API endpoints from the backend:

- `GET /api/health` - Health check
- `GET /api/models` - Available prediction models
- `GET /api/geocode/{location}` - Geocoding service
- `GET /api/weather/{lat}/{lon}` - Weather data
- `POST /api/predict` - Main prediction endpoint
- `GET /api/stats` - Global statistics

## 🐛 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Debugging

Enable debug mode by setting `VITE_ENABLE_DEBUG_MODE=true` in your environment variables.

## 🚀 Deployment

### Docker Deployment

The frontend can be deployed using Docker:

```bash
# Build the image
docker build -t disaster-prediction-frontend .

# Run the container
docker run -p 3000:3000 disaster-prediction-frontend
```

### Static Deployment

Build the application and serve the static files:

```bash
npm run build
# Serve the dist/ directory with your web server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please open an issue in the repository.
