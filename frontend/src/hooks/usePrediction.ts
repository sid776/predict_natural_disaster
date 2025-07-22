import { useState, useCallback } from 'react';
import type { PredictionRequest, PredictionResponse, DisasterType, PredictionModel } from '../types';
import { ApiService } from '../services/api';

interface UsePredictionReturn {
  loading: boolean;
  error: string | null;
  data: PredictionResponse | null;
  predict: (request: PredictionRequest) => Promise<void>;
  reset: () => void;
}

export const usePrediction = (): UsePredictionReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<PredictionResponse | null>(null);

  const predict = useCallback(async (request: PredictionRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await ApiService.predict(request);
      setData(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setData(null);
  }, []);

  return {
    loading,
    error,
    data,
    predict,
    reset,
  };
};

// Hook for batch predictions (all disaster types)
interface UseBatchPredictionReturn {
  loading: boolean;
  error: string | null;
  data: Record<DisasterType, PredictionResponse> | null;
  predictAll: (location: string, model: PredictionModel) => Promise<void>;
  reset: () => void;
}

export const useBatchPrediction = (): UseBatchPredictionReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<Record<DisasterType, PredictionResponse> | null>(null);

  const predictAll = useCallback(async (location: string, model: PredictionModel) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await ApiService.predictAll(location, model);
      setData(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, []);

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