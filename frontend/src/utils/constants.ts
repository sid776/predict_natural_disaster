export const COLORS = {
  // Deep Navy Background (Professional Foundation)
  main_bg: "#0f172a", // Deep navy
  card_bg: "rgba(255, 255, 255, 0.08)", // Glass effect
  sidebar_bg: "rgba(255, 255, 255, 0.12)",
  sidebar_border: "rgba(255, 255, 255, 0.15)",
  
  // Professional Text Colors
  text: "#f8fafc",
  text_secondary: "#cbd5e1",
  text_muted: "#94a3b8",
  
  // Vibrant Accent Colors for Critical Data
  // Orange/Amber → Alerts & Warnings
  tornado: "#ff6b35", // Vibrant orange
  wildfire: "#ff8c42", // Amber
  
  // Teal/Turquoise → Safe/Low Risk
  earthquake: "#00d4aa", // Bright teal
  flood: "#06b6d4", // Cyan
  
  // Neon Green → Current conditions / real-time updates
  current_status: "#00ff88", // Neon green
  
  // Magenta/Purple → Forecast trends
  forecast_trend: "#ec4899", // Magenta
  trend_secondary: "#a855f7", // Purple
  
  // IBM/Palantir-style Brand Colors
  primary: "#1A237E", // Deep blue
  secondary: "#7c3aed",
  accent: "#6366f1",
  
  // Enhanced Status Colors with Vibrancy
  success: "#00d4aa", // Bright teal
  warning: "#ff6b35", // Vibrant orange
  error: "#ff4757", // Bright red
  info: "#06b6d4", // Cyan
  
  // Glassmorphism Colors
  glass_bg: "rgba(255, 255, 255, 0.1)",
  glass_border: "rgba(255, 255, 255, 0.2)",
  glass_shadow: "0 8px 32px 0 rgba(31, 38, 135, 0.37)",
  
  // Additional colors
  highlight: "#fbbf24",
  muted: "#64748b",
  border: "rgba(255, 255, 255, 0.1)",
  
  // Vibrant Gradients for Dynamic Feel
  gradient_primary: "linear-gradient(135deg, #1A237E 0%, #3949ab 100%)",
  gradient_secondary: "linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)",
  gradient_glass: "linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
  gradient_success: "linear-gradient(135deg, #00d4aa 0%, #00ff88 100%)", // Teal to neon green
  gradient_warning: "linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%)", // Orange to amber
  gradient_error: "linear-gradient(135deg, #ff4757 0%, #ff6b6b 100%)", // Bright red gradient
  gradient_info: "linear-gradient(135deg, #06b6d4 0%, #00d4aa 100%)", // Cyan to teal
  
  // Risk Level Gradients
  gradient_low_risk: "linear-gradient(135deg, #00d4aa 0%, #00ff88 100%)",
  gradient_medium_risk: "linear-gradient(135deg, #ff8c42 0%, #ff6b35 100%)",
  gradient_high_risk: "linear-gradient(135deg, #ff4757 0%, #ff6b6b 100%)",
  
  // Weather Icons Colors
  weather_humidity: "#06b6d4", // Cyan for humidity
  weather_temperature: "#ff8c42", // Amber for temperature
  weather_wind: "#a855f7", // Purple for wind
  weather_pressure: "#ec4899", // Magenta for pressure
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

export const DATA_SOURCES = {
  openweathermap: {
    label: "OpenWeatherMap",
    description: "Real-time weather data including temperature, humidity, pressure, and wind",
    icon: "🌤️",
    color: COLORS.info,
    features: ["temperature", "humidity", "pressure", "wind_speed", "wind_direction"],
    disaster_types: ["tornado", "wildfire", "flood"],
    api_required: true,
  },
  usgs: {
    label: "USGS Earthquake",
    description: "United States Geological Survey earthquake data and historical records",
    icon: "🌋",
    color: COLORS.warning,
    features: ["magnitude", "depth", "time", "historical_data"],
    disaster_types: ["earthquake"],
    api_required: false,
  },
  nasa_power: {
    label: "NASA POWER",
    description: "NASA Prediction of Worldwide Energy Resources climate data",
    icon: "🛰️",
    color: COLORS.primary,
    features: ["temperature", "wind_speed", "precipitation", "solar_radiation"],
    disaster_types: ["tornado", "wildfire", "flood"],
    api_required: false,
  },
  data_fusion: {
    label: "Data Fusion",
    description: "Combined data from multiple sources for comprehensive analysis",
    icon: "🔗",
    color: COLORS.success,
    features: ["all_features", "cross_validation", "enhanced_accuracy"],
    disaster_types: ["tornado", "earthquake", "wildfire", "flood"],
    api_required: true,
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