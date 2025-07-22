export const COLORS = {
  main_bg: "#f5f5f5",
  card_bg: "#ffffff",
  sidebar_bg: "#ffffff",
  sidebar_border: "#e0e0e0",
  text: "#333333",
  text_secondary: "#666666",
  tornado: "#ff6b6b",
  earthquake: "#4ecdc4",
  wildfire: "#ffa726",
  flood: "#42a5f5",
  guide: "#9c27b0",
  success: "#4caf50",
  warning: "#ff9800",
  error: "#f44336",
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
    description: "Advanced quantum computing model",
    color: COLORS.guide,
  },
  ml: {
    label: "Machine Learning",
    description: "Traditional ML algorithms",
    color: COLORS.success,
  },
  statistical: {
    label: "Statistical",
    description: "Statistical analysis model",
    color: COLORS.warning,
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