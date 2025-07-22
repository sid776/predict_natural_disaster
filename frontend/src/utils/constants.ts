export const COLORS = {
  main_bg: "#f8fafc",
  card_bg: "#ffffff",
  sidebar_bg: "#ffffff",
  sidebar_border: "#e2e8f0",
  text: "#1e293b",
  text_secondary: "#64748b",
  tornado: "#ef4444",
  earthquake: "#10b981",
  wildfire: "#f59e0b",
  flood: "#3b82f6",
  primary: "#0f172a",
  secondary: "#64748b",
  success: "#10b981",
  warning: "#f59e0b",
  error: "#ef4444",
  info: "#3b82f6",
};

export const DISASTER_TYPES = {
  tornado: {
    label: "Tornado",
    icon: "🌪️",
    color: COLORS.tornado,
    description: "Violent rotating column of air",
  },
  earthquake: {
    label: "Earthquake",
    icon: "🌋",
    color: COLORS.earthquake,
    description: "Sudden shaking of the ground",
  },
  wildfire: {
    label: "Wildfire",
    icon: "🔥",
    color: COLORS.wildfire,
    description: "Uncontrolled fire in vegetation",
  },
  flood: {
    label: "Flood",
    icon: "🌊",
    color: COLORS.flood,
    description: "Overflow of water onto land",
  },
};

export const PREDICTION_MODELS = {
  quantum: {
    label: "Quantum AI",
    description: "Quantum-inspired machine learning using Qiskit",
    icon: "⚛️",
    color: COLORS.primary,
  },
  lstm: {
    label: "LSTM (Deep Learning)",
    description: "Long Short-Term Memory neural networks",
    icon: "🧠",
    color: COLORS.success,
  },
  rf: {
    label: "Random Forest",
    description: "Ensemble learning method with decision trees",
    icon: "🌲",
    color: COLORS.warning,
  },
  xgb: {
    label: "XGBoost",
    description: "Gradient boosting framework",
    icon: "📈",
    color: COLORS.error,
  },
  svm: {
    label: "SVM",
    description: "Support Vector Machine classifier",
    icon: "🔧",
    color: COLORS.info,
  },
  mlp: {
    label: "MLP/ANN",
    description: "Multi-layer Perceptron neural network",
    icon: "🕸️",
    color: COLORS.secondary,
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