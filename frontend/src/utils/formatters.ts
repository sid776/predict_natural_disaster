import type { WeatherData, FactorImpacts } from '../types';

// Temperature conversion utilities
export const kelvinToCelsius = (kelvin: number): number => {
  return kelvin - 273.15;
};

export const kelvinToFahrenheit = (kelvin: number): number => {
  return (kelvin - 273.15) * 9/5 + 32;
};

export const celsiusToFahrenheit = (celsius: number): number => {
  return celsius * 9/5 + 32;
};

// Format temperature for display
export const formatTemperature = (kelvin: number, unit: 'C' | 'F' = 'C'): string => {
  if (unit === 'F') {
    return `${kelvinToFahrenheit(kelvin).toFixed(1)}°F`;
  }
  return `${kelvinToCelsius(kelvin).toFixed(1)}°C`;
};

// Format percentage
export const formatPercentage = (value: number, decimals: number = 1): string => {
  return `${(value * 100).toFixed(decimals)}%`;
};

// Format pressure
export const formatPressure = (pressure: number): string => {
  return `${pressure.toFixed(0)} hPa`;
};

// Format wind speed
export const formatWindSpeed = (speed: number, unit: 'm/s' | 'mph' | 'km/h' = 'm/s'): string => {
  switch (unit) {
    case 'mph':
      return `${(speed * 2.237).toFixed(1)} mph`;
    case 'km/h':
      return `${(speed * 3.6).toFixed(1)} km/h`;
    default:
      return `${speed.toFixed(1)} m/s`;
  }
};

// Format humidity
export const formatHumidity = (humidity: number): string => {
  return `${humidity.toFixed(0)}%`;
};

// Format date
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });
};

// Format date for charts
export const formatChartDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
};

// Format timestamp
export const formatTimestamp = (timestamp: string): string => {
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

// Format large numbers
export const formatLargeNumber = (num: number): string => {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
};

// Format currency
export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(amount);
};

// Get weather description
export const getWeatherDescription = (weatherData: WeatherData): string => {
  if (weatherData.weather && weatherData.weather.length > 0) {
    return weatherData.weather[0].description;
  }
  return 'Unknown weather conditions';
};

// Get weather icon
export const getWeatherIcon = (weatherData: WeatherData): string => {
  if (weatherData.weather && weatherData.weather.length > 0) {
    return weatherData.weather[0].icon;
  }
  return '01d'; // Default sunny icon
};

// Calculate risk level based on probability
export const getRiskLevel = (probability: number): {
  level: 'low' | 'medium' | 'high' | 'extreme';
  color: string;
  label: string;
} => {
  if (probability < 0.3) {
    return { level: 'low', color: '#4CAF50', label: 'Low Risk' };
  } else if (probability < 0.7) {
    return { level: 'medium', color: '#FF9800', label: 'Medium Risk' };
  } else if (probability < 0.9) {
    return { level: 'high', color: '#F44336', label: 'High Risk' };
  } else {
    return { level: 'extreme', color: '#9C27B0', label: 'Extreme Risk' };
  }
};

// Format factor impacts for display
export const formatFactorImpacts = (factors: FactorImpacts): Array<{
  name: string;
  value: number;
  formatted: string;
}> => {
  return Object.entries(factors)
    .map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1).replace('_', ' '),
      value: value || 0,
      formatted: formatPercentage(value || 0),
    }))
    .sort((a, b) => b.value - a.value); // Sort by impact (highest first)
};

// Get dominant factors (top 3)
export const getDominantFactors = (factors: FactorImpacts, count: number = 3): string[] => {
  const formattedFactors = formatFactorImpacts(factors);
  return formattedFactors.slice(0, count).map(factor => factor.name);
};

// Calculate average probability from forecast
export const calculateAverageProbability = (forecast: Array<{ probability: number }>): number => {
  if (forecast.length === 0) return 0;
  const sum = forecast.reduce((acc, day) => acc + day.probability, 0);
  return sum / forecast.length;
};

// Get trend direction from forecast
export const getTrendDirection = (forecast: Array<{ probability: number }>): 'increasing' | 'decreasing' | 'stable' => {
  if (forecast.length < 2) return 'stable';
  
  const firstHalf = forecast.slice(0, Math.floor(forecast.length / 2));
  const secondHalf = forecast.slice(Math.floor(forecast.length / 2));
  
  const firstAvg = calculateAverageProbability(firstHalf);
  const secondAvg = calculateAverageProbability(secondHalf);
  
  const difference = secondAvg - firstAvg;
  
  if (Math.abs(difference) < 0.05) return 'stable';
  return difference > 0 ? 'increasing' : 'decreasing';
};

// Format location for display
export const formatLocation = (location: string): string => {
  return location.split(',').map(part => part.trim()).join(', ');
};

// Validate location input
export const validateLocation = (location: string): boolean => {
  return location.trim().length >= 3 && /^[a-zA-Z\s,]+$/.test(location);
};

// Get weather summary for display
export const getWeatherSummary = (weatherData: WeatherData): {
  temperature: string;
  humidity: string;
  pressure: string;
  windSpeed: string;
  description: string;
} => {
  return {
    temperature: formatTemperature(weatherData.main.temp),
    humidity: formatHumidity(weatherData.main.humidity),
    pressure: formatPressure(weatherData.main.pressure),
    windSpeed: formatWindSpeed(weatherData.wind.speed),
    description: getWeatherDescription(weatherData),
  };
}; 