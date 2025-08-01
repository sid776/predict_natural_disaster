import axios from "axios";
import type { BatchPredictionResponse, PredictionModel, DisasterType, DataSourceType, DataSourceInfo, WeatherAlert } from "../types";

const API_BASE_URL = process.env.VITE_API_BASE_URL || "https://predictnaturaldisasterbackend-production.up.railway.app";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export const apiService = {
  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      const response = await apiClient.get("/api/health");
      return response.status === 200;
    } catch (error: any) {
      console.error("Health check failed:", error);
      return false;
    }
  },

  // Get batch predictions for all disaster types
  async getBatchPredictions(
    location: string,
    model: PredictionModel
  ): Promise<BatchPredictionResponse> {
    try {
      // Make individual predictions for each disaster type
      const disasterTypes: DisasterType[] = ["earthquake", "flood", "tornado", "wildfire"];
      const predictions: BatchPredictionResponse = {};

      for (const disasterType of disasterTypes) {
        try {
          const response = await apiClient.post("/api/predict", {
            location,
            model,
            disaster_type: disasterType,
          });
          
          // Extract the prediction data from the API response
          if (response.data.success && response.data.data) {
            console.log(`${disasterType} prediction data:`, response.data.data);
            predictions[disasterType] = response.data.data;
          }
        } catch (error: any) {
          console.error(`${disasterType} prediction failed:`, error);
          // Continue with other disaster types even if one fails
        }
      }

      return predictions;
    } catch (error: any) {
      console.error("Batch prediction failed:", error);
      throw new Error(
        error.response?.data?.detail || "Failed to get predictions"
      );
    }
  },

  // Get prediction for a specific disaster type
  async getPrediction(
    location: string,
    disasterType: DisasterType,
    model: PredictionModel,
    dataSource?: DataSourceType
  ): Promise<any> {
    try {
      const response = await apiClient.post("/api/predict", {
        location,
        model,
        disaster_type: disasterType,
        data_source: dataSource,
      });
      
      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error(response.data.error || "Prediction failed");
      }
    } catch (error: any) {
      console.error(`${disasterType} prediction failed:`, error);
      throw new Error(
        error.response?.data?.detail || `Failed to get ${disasterType} prediction`
      );
    }
  },

  // Get available data sources
  async getDataSources(): Promise<DataSourceInfo[]> {
    try {
      const response = await apiClient.get("/api/data-sources");
      if (response.data.success) {
        return response.data.data;
      } else {
        throw new Error("Failed to get data sources");
      }
    } catch (error: any) {
      console.error("Failed to get data sources:", error);
      throw new Error(
        error.response?.data?.detail || "Failed to get data sources"
      );
    }
  },

  // Get batch predictions with data source
  async getBatchPredictionsWithDataSource(
    location: string,
    model: PredictionModel,
    dataSource: DataSourceType
  ): Promise<BatchPredictionResponse> {
    try {
      const disasterTypes: DisasterType[] = ["earthquake", "flood", "tornado", "wildfire"];
      const predictions: BatchPredictionResponse = {};

      for (const disasterType of disasterTypes) {
        try {
          const response = await apiClient.post("/api/predict", {
            location,
            model,
            disaster_type: disasterType,
            data_source: dataSource,
          });
          
          if (response.data.success && response.data.data) {
            console.log(`${disasterType} prediction data:`, response.data.data);
            predictions[disasterType] = response.data.data;
          }
        } catch (error: any) {
          console.error(`${disasterType} prediction failed:`, error);
          // Continue with other disaster types even if one fails
        }
      }

      return predictions;
    } catch (error: any) {
      console.error("Batch prediction failed:", error);
      throw new Error(
        error.response?.data?.detail || "Failed to get predictions"
      );
    }
  },

  // Get weather alerts for a location
  async getWeatherAlerts(location: string): Promise<WeatherAlert[]> {
    try {
      const response = await apiClient.get(`/api/weather-alerts/${encodeURIComponent(location)}`);
      
      if (response.data.success && response.data.data?.alerts) {
        return response.data.data.alerts;
      } else {
        return [];
      }
    } catch (error: any) {
      console.error("Failed to get weather alerts:", error);
      return [];
    }
  },

  // Get weather alerts for coordinates
  async getWeatherAlertsByCoordinates(lat: number, lon: number): Promise<WeatherAlert[]> {
    try {
      const response = await apiClient.get(`/api/weather-alerts/coordinates/${lat}/${lon}`);
      
      if (response.data.success && response.data.data?.alerts) {
        return response.data.data.alerts;
      } else {
        return [];
      }
    } catch (error: any) {
      console.error("Failed to get weather alerts:", error);
      return [];
    }
  },

  // Get multi-county prediction
  async getMultiCountyPrediction(
    location: string,
    disasterType: string,
    model: string = "quantum",
    dataSource: string = "openweathermap"
  ): Promise<any> {
    try {
      const response = await apiClient.get(
        `/api/multi-county-prediction/${encodeURIComponent(location)}`,
        {
          params: {
            disaster_type: disasterType,
            model,
            data_source: dataSource,
          },
        }
      );
      
      if (response.data.success && response.data.data) {
        return response.data.data;
      } else {
        throw new Error("Failed to get multi-county prediction");
      }
    } catch (error: any) {
      console.error("Failed to get multi-county prediction:", error);
      throw new Error(
        error.response?.data?.detail || "Failed to get multi-county prediction"
      );
    }
  },
}; 