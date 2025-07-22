import type { DisasterType, PredictionModel } from '../types';

// Color palette matching the original app
export const COLORS = {
  // Disaster type colors
  tornado: '#FFA726',      // Orange
  earthquake: '#AB47BC',   // Purple
  wildfire: '#FFE066',     // Yellow
  flood: '#2ECC71',        // Green
  guide: '#42A5F5',        // Blue
  
  // UI colors
  sidebar_bg: '#F3E8FF',       // Light lavender
  sidebar_border: '#B39DDB',   // Purple border
  sidebar_button: '#8E24AA',   // Purple button
  sidebar_button_text: '#FFFFFF',
  main_bg: '#F8F9FA',          // Very light gray
  card_bg: '#FFF9FB',          // Soft pastel
  card_border: '#FFA726',      // Orange border for tornado
  text: '#333A4D',             // Dark gray
  white: '#FFFFFF',
  
  // Chart colors
  success: '#4CAF50',
  warning: '#FF9800',
  danger: '#F44336',
  info: '#2196F3',
} as const;

// Disaster type configuration
export const DISASTER_TYPES: Record<DisasterType, {
  label: string;
  color: string;
  description: string;
  icon: string;
}> = {
  tornado: {
    label: 'Tornado',
    color: COLORS.tornado,
    description: 'Violent rotating column of air',
    icon: '🌪️',
  },
  earthquake: {
    label: 'Earthquake',
    color: COLORS.earthquake,
    description: 'Sudden shaking of the ground',
    icon: '🌋',
  },
  wildfire: {
    label: 'Wildfire',
    color: COLORS.wildfire,
    description: 'Uncontrolled fire in vegetation',
    icon: '🔥',
  },
  flood: {
    label: 'Flood',
    color: COLORS.flood,
    description: 'Overflow of water onto land',
    icon: '🌊',
  },
};

// Prediction model configuration
export const PREDICTION_MODELS: Record<PredictionModel, {
  label: string;
  description: string;
  icon: string;
}> = {
  quantum: {
    label: 'Quantum AI',
    description: 'Quantum-inspired machine learning',
    icon: '⚛️',
  },
  lstm: {
    label: 'LSTM (Deep Learning)',
    description: 'Long Short-Term Memory neural networks',
    icon: '🧠',
  },
  rf: {
    label: 'Random Forest',
    description: 'Ensemble learning method',
    icon: '🌲',
  },
  xgb: {
    label: 'XGBoost',
    description: 'Gradient boosting framework',
    icon: '📈',
  },
  svm: {
    label: 'SVM',
    description: 'Support Vector Machine',
    icon: '🔧',
  },
  mlp: {
    label: 'MLP/ANN',
    description: 'Multi-layer Perceptron',
    icon: '🕸️',
  },
};

// Global statistics data
export const GLOBAL_STATS = {
  tornado: {
    count: 1250,  // Average annual tornadoes in the US
    deaths: 60,   // Average annual deaths
    injuries: 1500,
    damage: 1.5   // Billions USD
  },
  earthquake: {
    count: 20000,  // Annual earthquakes worldwide
    deaths: 2000,  // Average annual deaths
    injuries: 5000,
    damage: 5.0    // Billions USD
  },
  wildfire: {
    count: 50000,  // Annual wildfires in the US
    deaths: 100,   // Average annual deaths
    injuries: 2000,
    damage: 2.0    // Billions USD
  },
  flood: {
    count: 1000,   // Annual significant floods worldwide
    deaths: 5000,  // Average annual deaths
    injuries: 10000,
    damage: 10.0   // Billions USD
  }
} as const;

// Chart configuration
export const CHART_CONFIG = {
  gauge: {
    height: 300,
    width: 400,
  },
  line: {
    height: 300,
    width: 600,
  },
  bar: {
    height: 300,
    width: 500,
  },
} as const;

// API configuration
export const API_CONFIG = {
  timeout: 30000, // 30 seconds
  retryAttempts: 3,
  retryDelay: 1000, // 1 second
} as const;

// Weather thresholds for risk assessment
export const WEATHER_THRESHOLDS = {
  tornado: {
    temp: { min: 20, max: 30 }, // Celsius
    humidity: { min: 60, max: 80 }, // Percentage
    pressure: { min: 980, max: 1000 }, // hPa
    wind_speed: { min: 10, max: 20 }, // m/s
  },
  earthquake: {
    pressure: { min: 990, max: 1013 }, // hPa
    humidity: { min: 50, max: 90 }, // Percentage
  },
  wildfire: {
    temp: { min: 25, max: 40 }, // Celsius
    humidity: { min: 20, max: 50 }, // Percentage
    wind_speed: { min: 5, max: 25 }, // m/s
  },
  flood: {
    temp: { min: 10, max: 25 }, // Celsius
    humidity: { min: 70, max: 95 }, // Percentage
    pressure: { min: 980, max: 1010 }, // hPa
  },
} as const; 