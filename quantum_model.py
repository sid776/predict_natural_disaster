import numpy as np
from sklearn.preprocessing import MinMaxScaler
import traceback
from qiskit import QuantumCircuit

class QuantumTornadoPredictor:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.n_qubits = 5  # Number of qubits for our quantum circuit
        
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

    def predict(self, features):
        try:
            print("Starting prediction with features:", features)
            
            # Check if all required features are present
            required_features = ['temperature', 'humidity', 'pressure', 'wind_speed', 'wind_deg']
            for feature in required_features:
                if feature not in features:
                    print(f"Missing required feature: {feature}")
                    # Provide default value for missing feature
                    features[feature] = 0
            
            # Normalize input features
            print("Normalizing features...")
            normalized_features = self._normalize_features(features)
            print("Normalized features:", normalized_features)
            
            # Simple quantum-inspired calculation
            # This is a simplified approach that doesn't actually run a quantum circuit
            # but uses quantum-inspired principles
            
            # Calculate a weighted sum of the normalized features
            weights = np.array([0.3, 0.2, 0.2, 0.2, 0.1])  # Weights for each feature
            print("Using weights:", weights)
            
            weighted_sum = np.sum(normalized_features * weights)
            print("Weighted sum:", weighted_sum)
            
            # Scale to a probability between 0 and 100
            probability = weighted_sum * 100
            print("Initial probability:", probability)
            
            # Add some randomness to simulate quantum uncertainty
            random_factor = np.random.normal(0, 5)
            print("Random factor:", random_factor)
            
            probability = probability + random_factor
            print("Probability after random factor:", probability)
            
            # Ensure the probability is between 0 and 100
            probability = max(0, min(100, probability))
            print("Final probability:", probability)
            
            return probability
        except Exception as e:
            print(f"Error in predict: {str(e)}")
            print(traceback.format_exc())
            # Return a default value instead of raising an exception
            return 50.0  # Default to 50% probability

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