export type DisasterType = "tornado" | "earthquake" | "wildfire" | "flood";
export type PredictionModel = "quantum" | "lstm" | "rf" | "xgb" | "svm" | "mlp";

// Backend Weather Data Structure
export interface WeatherMain {
  temp: number; // Kelvin
  humidity: number; // Percentage
  pressure: number; // hPa
}

export interface WeatherWind {
  speed: number; // m/s
  deg: number; // degrees
}

export interface WeatherClouds {
  all: number; // percentage
}

export interface WeatherRain {
  h1?: number; // mm
}

export interface WeatherSys {
  sunrise: number;
  sunset: number;
}

export interface WeatherCondition {
  id: number;
  main: string;
  description: string;
  icon: string;
}

export interface WeatherCoord {
  lat: number;
  lon: number;
}

export interface WeatherData {
  main: WeatherMain;
  wind: WeatherWind;
  clouds: WeatherClouds;
  rain?: WeatherRain;
  sys: WeatherSys;
  weather: WeatherCondition[];
  visibility: number; // meters
  coord: WeatherCoord;
  mock_data?: boolean;
}

// Backend Forecast Structure
export interface ForecastDay {
  date: string; // YYYY-MM-DD
  probability: number; // 0-1
  weather: WeatherData;
  key_factors: string[];
}

// Backend Factor Impacts
export interface FactorImpacts {
  temperature?: number; // percentage
  humidity?: number; // percentage
  pressure?: number; // percentage
  wind_speed?: number; // percentage
}

// Backend Prediction Metadata
export interface PredictionMetadata {
  location: string;
  model: PredictionModel;
  disaster_type: DisasterType;
  timestamp: string;
  weather_data: WeatherData;
}

// Backend Prediction Response
export interface PredictionResponse {
  probability: number;
  forecast: ForecastDay[];
  factors: FactorImpacts;
  metadata: PredictionMetadata;
}

// Backend API Response Wrapper
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  error?: string;
}

// Frontend Batch Prediction Response
export interface BatchPredictionResponse {
  tornado?: PredictionResponse;
  earthquake?: PredictionResponse;
  wildfire?: PredictionResponse;
  flood?: PredictionResponse;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
} 