# Quantum Tornado Prediction System

This application uses quantum computing and AI to predict tornado probabilities for locations in the United States. It combines weather data with quantum algorithms to provide predictions.

## Features
- Location-based tornado prediction
- Quantum-enhanced machine learning
- Real-time weather data integration
- Web interface for easy interaction

## How It Works

### Quantum Computing Approach
The system uses a quantum-enhanced machine learning approach to predict tornado probabilities:

1. **Feature Encoding**: Weather data (temperature, humidity, pressure, wind speed, wind direction) is encoded into quantum states using rotation gates (RY and RZ).

2. **Quantum Circuit**: A 5-qubit quantum circuit processes these encoded features:
   - Each weather feature is encoded into a qubit using rotation gates
   - Entangling layers (CNOT gates) create correlations between features
   - The quantum state's properties are measured to determine tornado probability

3. **Prediction**: The magnitude of specific basis states in the final quantum state is used to calculate the tornado probability.

### Weather Data Integration
- Uses OpenWeatherMap API to fetch real-time weather data
- Geocoding converts location names to coordinates
- Weather features are normalized before quantum processing

## Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file based on `.env.example` and add your OpenWeatherMap API key:
```
OPENWEATHER_API_KEY=your_api_key_here
```

## Usage
1. Run the application:
```bash
python app.py
```
2. Open your browser and navigate to `http://localhost:5000`
3. Enter your location in the US (e.g., "Oklahoma City, OK")
4. View the tornado prediction results

## Technical Details
- **Quantum Framework**: Uses Qiskit for quantum circuit creation and simulation
- **Weather API**: Integrates with OpenWeatherMap for real-time data
- **Web Framework**: Flask for backend, Bootstrap for frontend
- **Geocoding**: Uses geopy for location-to-coordinates conversion

## Project Structure
- `app.py`: Main Flask application with routes and API integration
- `quantum_model.py`: Quantum computing model for tornado prediction
- `templates/index.html`: Web interface
- `requirements.txt`: Project dependencies
- `.env`: Configuration for API keys

## Quantum Algorithm Explanation
The quantum algorithm used in this project is based on quantum feature maps and variational quantum circuits:

1. **Quantum Feature Map**: Maps classical weather data to quantum states using rotation gates
2. **Entanglement**: Creates correlations between weather features using CNOT gates
3. **Measurement**: Extracts probability information from the quantum state

This approach leverages quantum superposition and entanglement to potentially capture complex weather patterns that classical algorithms might miss.

## Limitations and Future Improvements
- Current implementation uses a simplified quantum model
- Could be enhanced with:
  - More sophisticated quantum circuits
  - Integration with real quantum hardware
  - Historical tornado data for model calibration
  - Additional weather features

## Note
This is a research project and should not be used as the sole source for tornado predictions. Always follow official weather service warnings and alerts. 