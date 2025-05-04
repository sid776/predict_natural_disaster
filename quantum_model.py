import pennylane as qml
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import traceback
from qiskit import QuantumCircuit

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
            
            # Normalize features to [0, 2π]
            features = [
                (temp + 20) / 60 * 2 * np.pi,  # Temperature range: -20 to 40 C
                humidity / 100 * 2 * np.pi,     # Humidity range: 0 to 100%
                (pressure - 950) / 100 * 2 * np.pi,  # Pressure range: 950 to 1050 hPa
                wind_speed / 30 * 2 * np.pi     # Wind speed range: 0 to 30 m/s
            ]
            
            # Get quantum predictions
            predictions = self.circuit(np.array(features))
            
            # Convert predictions to probability [0, 1]
            probability = (np.mean(predictions) + 1) / 2
            
            return probability
        except Exception as e:
            print(f"Error in predict: {str(e)}")
            return 0.5  # Return default probability on error

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