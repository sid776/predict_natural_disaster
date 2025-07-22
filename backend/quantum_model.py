import pennylane as qml
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import traceback
# Qiskit imports are not used in this implementation - using PennyLane instead
# from qiskit import QuantumCircuit

class QuantumTornadoPredictor:
    def __init__(self):
        self.dev = qml.device("default.qubit", wires=4)
        self.circuit = qml.QNode(self.quantum_circuit, self.dev)
        self.scaler = MinMaxScaler()
        self.n_qubits = 5  # Number of qubits for our quantum circuit
        
    def quantum_circuit(self, features):
        # Encode the weather features into quantum states
        for i, feature in enumerate(features):
            qml.RY(feature, wires=i)
            
        # Create entanglement
        for i in range(3):
            qml.CNOT(wires=[i, i+1])
            
        # Measure in computational basis
        return [qml.expval(qml.PauliZ(i)) for i in range(4)]
    
    def predict(self, weather_data):
        try:
            # Extract and normalize weather features
            temp = weather_data['main']['temp'] - 273.15  # Convert to Celsius
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            wind_speed = weather_data['wind']['speed']
            
            # More realistic normalization ranges for tornado prediction
            features = [
                (temp - 15) / 30 * 2 * np.pi,  # Temperature range: 15 to 45 C (typical tornado conditions)
                (humidity - 40) / 40 * 2 * np.pi,  # Humidity range: 40 to 80% (typical tornado conditions)
                (pressure - 980) / 40 * 2 * np.pi,  # Pressure range: 980 to 1020 hPa (typical tornado conditions)
                wind_speed / 20 * 2 * np.pi  # Wind speed range: 0 to 20 m/s (typical tornado conditions)
            ]
            
            # Get quantum predictions
            predictions = self.circuit(np.array(features))
            
            # Convert predictions to probability [0, 1] with more conservative scaling
            raw_probability = (np.mean(predictions) + 1) / 2
            
            # Apply more conservative probability scaling
            # This ensures probabilities are lower and more realistic
            scaled_probability = raw_probability * 0.6  # Scale down by 40%
            
            # Add location-specific adjustments
            # Lower probabilities for regions with historically low tornado activity
            if self._is_low_tornado_region(weather_data):
                scaled_probability *= 0.3  # Reduce probability by 70% for low-risk regions
            
            return min(0.65, scaled_probability)  # Cap maximum probability at 65%
            
        except Exception as e:
            print(f"Error in predict: {str(e)}")
            return 0.1  # Return low default probability on error
    
    def _is_low_tornado_region(self, weather_data):
        """
        Check if the location is in a region with historically low tornado activity
        """
        try:
            # Get location coordinates
            lat = weather_data['coord']['lat']
            lon = weather_data['coord']['lon']
            
            # Regions with historically low tornado activity
            low_risk_regions = [
                # Northeast US (including New Jersey)
                {'min_lat': 38.0, 'max_lat': 45.0, 'min_lon': -75.0, 'max_lon': -70.0},
                # West Coast
                {'min_lat': 32.0, 'max_lat': 49.0, 'min_lon': -125.0, 'max_lon': -120.0},
                # Northern states (excluding tornado alley)
                {'min_lat': 45.0, 'max_lat': 49.0, 'min_lon': -125.0, 'max_lon': -90.0},
                # Alaska
                {'min_lat': 50.0, 'max_lat': 72.0, 'min_lon': -180.0, 'max_lon': -130.0},
                # Hawaii
                {'min_lat': 18.0, 'max_lat': 23.0, 'min_lon': -160.0, 'max_lon': -154.0}
            ]
            
            # Check if location is in any low-risk region
            for region in low_risk_regions:
                if (region['min_lat'] <= lat <= region['max_lat'] and 
                    region['min_lon'] <= lon <= region['max_lon']):
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error in _is_low_tornado_region: {str(e)}")
            return False  # Default to not low-risk on error

    def _normalize_features(self, features):
        try:
            print("Starting feature normalization...")
            # Ensure all required features are present
            required_features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_deg']
            feature_values = []
            
            for feature in required_features:
                if feature in features:
                    feature_values.append(features[feature])
                    print(f"Feature {feature}: {features[feature]}")
                else:
                    print(f"Warning: Missing feature {feature}, using default value 0")
                    feature_values.append(0)
            
            # Convert features to numpy array and normalize
            feature_array = np.array(feature_values).reshape(1, -1)
            print("Feature array before normalization:", feature_array)
            
            # Normalize to [0, 1] range
            normalized = self.scaler.fit_transform(feature_array)
            print("Normalized features:", normalized[0])
            
            return normalized[0]
        except Exception as e:
            print(f"Error in _normalize_features: {str(e)}")
            print(traceback.format_exc())
            # Return default values if normalization fails
            return np.array([0.5, 0.5, 0.5, 0.5, 0.5])

    def _create_quantum_circuit(self, normalized_features):
        try:
            # Create quantum circuit
            qc = QuantumCircuit(self.n_qubits)
            
            # Encode classical data into quantum state
            for i, feature in enumerate(normalized_features):
                # Apply rotation based on feature value
                qc.ry(feature * np.pi, i)
                
            # Add entangling layers
            for i in range(self.n_qubits - 1):
                qc.cx(i, i + 1)
                
            # Add measurement
            qc.measure_all()
            
            return qc
        except Exception as e:
            print(f"Error in _create_quantum_circuit: {str(e)}")
            print(traceback.format_exc())
            raise

    def _quantum_feature_map(self, features):
        """
        Maps classical features to quantum state using quantum feature map
        """
        try:
            qc = QuantumCircuit(self.n_qubits)
            
            # Apply feature map
            for i, feature in enumerate(features):
                # Encode each feature using rotation gates
                qc.ry(feature * np.pi, i)
                qc.rz(feature * np.pi, i)
                
            return qc
        except Exception as e:
            print(f"Error in _quantum_feature_map: {str(e)}")
            print(traceback.format_exc())
            raise 