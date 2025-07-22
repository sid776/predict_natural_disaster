import { useState, useCallback } from "react";
import { apiService } from "../services/api";
import type { BatchPredictionResponse, PredictionModel } from "../types";

export const useBatchPrediction = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BatchPredictionResponse | null>(null);

  const predictAll = useCallback(
    async (location: string, model: PredictionModel) => {
      setLoading(true);
      setError(null);

      try {
        const predictions = await apiService.getBatchPredictions(location, model);
        setData(predictions);
      } catch (err: any) {
        setError(err.message || "Failed to get predictions");
        setData(null);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setData(null);
  }, []);

  return {
    loading,
    error,
    data,
    predictAll,
    reset,
  };
}; 