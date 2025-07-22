// Weather data types
export interface WeatherData {
  main: {
    temp: number; // Kelvin
    humidity: number; // Percentage
    pressure: number; // hPa
  };
  wind: {
    speed: number; // m/s
    deg: number; // degrees
  };
  clouds: {
    all: number; // percentage
  };
  rain?: {
    '1h': number; // mm
  };
  sys: {
    sunrise: number;
    sunset: number;
  };
  weather: Array<{
    id: number;
    main: string;
    description: string;
    icon: string;
  }>;
  visibility: number; // meters
  coord: {
    lat: number;
    lon: number;
  };
  mock_data?: boolean;
}

// Prediction model types
export type PredictionModel = 'quantum' | 'lstm' | 'rf' | 'xgb' | 'svm' | 'mlp';

export type DisasterType = 'tornado' | 'earthquake' | 'wildfire' | 'flood';

// Forecast data types
export interface ForecastDay {
  date: string; // YYYY-MM-DD
  probability: number; // 0-1
  weather: WeatherData;
  key_factors: string[];
}

// Factor impact analysis
export interface FactorImpacts {
  temperature?: number; // percentage
  humidity?: number; // percentage
  pressure?: number; // percentage
  wind_speed?: number; // percentage
}

// Prediction request
export interface PredictionRequest {
  location: string;
  model: PredictionModel;
  disaster_type: DisasterType;
}

// Prediction response
export interface PredictionResponse {
  probability: number; // 0-1
  forecast: ForecastDay[];
  factors: FactorImpacts;
  metadata: {
    location: string;
    model: PredictionModel;
    disaster_type: DisasterType;
    timestamp: string;
    weather_data: WeatherData;
  };
}

// API response wrapper
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  error?: string;
}

// Geocoding response
export interface GeocodingResponse {
  lat: number;
  lon: number;
  display_name: string;
}

// Global statistics
export interface GlobalStats {
  count: number;
  deaths: number;
  injuries: number;
  damage: number; // billions USD
}

export interface GlobalStatsData {
  tornado: GlobalStats;
  earthquake: GlobalStats;
  fire: GlobalStats;
  flood: GlobalStats;
}

// Chart data types
export interface GaugeData {
  value: number; // 0-100
  label: string;
  color: string;
}

export interface ChartDataPoint {
  x: string | number;
  y: number;
  label?: string;
}

// UI State types
export interface PredictionState {
  loading: boolean;
  error: string | null;
  data: PredictionResponse | null;
}

export interface AppState {
  location: string;
  selectedModel: PredictionModel;
  selectedDisaster: DisasterType;
  predictions: Record<DisasterType, PredictionState>;
} 