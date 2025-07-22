import axios from "axios";
import type { BatchPredictionResponse, PredictionModel, DisasterType } from "../types";

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
      const disasterTypes: DisasterType[] = ["tornado", "earthquake", "wildfire", "flood"];
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
    model: PredictionModel
  ): Promise<any> {
    try {
      const response = await apiClient.post("/api/predict", {
        location,
        model,
        disaster_type: disasterType,
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
}; 