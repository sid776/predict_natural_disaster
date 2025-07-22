import axios from 'axios';
import type { AxiosResponse } from 'axios';
import type {
  PredictionRequest,
  PredictionResponse,
  WeatherData,
  GeocodingResponse,
  ApiResponse,
  PredictionModel,
  DisasterType
} from '../types';

// API configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

// API endpoints
export const API_ENDPOINTS = {
  PREDICT: `${API_BASE_URL}/api/predict`,
  WEATHER: (lat: number, lon: number) => `${API_BASE_URL}/api/weather/${lat}/${lon}`,
  GEOCODE: (location: string) => `${API_BASE_URL}/api/geocode/${encodeURIComponent(location)}`,
  MODELS: `${API_BASE_URL}/api/models`,
  STATS: `${API_BASE_URL}/api/stats`,
  HEALTH: `${API_BASE_URL}/api/health`,
};

// API service functions
export const apiService = {
  async predict(data: PredictionRequest): Promise<PredictionResponse> {
    const response = await fetch(API_ENDPOINTS.PREDICT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return response.json();
  },

  async getWeather(lat: number, lon: number): Promise<WeatherData> {
    const response = await fetch(API_ENDPOINTS.WEATHER(lat, lon));
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  },

  async geocode(location: string): Promise<GeocodingResponse> {
    const response = await fetch(API_ENDPOINTS.GEOCODE(location));
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  },

  async getModels(): Promise<PredictionModel[]> {
    const response = await fetch(API_ENDPOINTS.MODELS);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  },

  async getStats(): Promise<Record<DisasterType, any>> {
    const response = await fetch(API_ENDPOINTS.STATS);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  },

  async healthCheck(): Promise<boolean> {
    const response = await fetch(API_ENDPOINTS.HEALTH);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response.json();
  },
}; 