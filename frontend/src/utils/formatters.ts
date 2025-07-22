import type { WeatherData } from "../types";

export const formatPercentage = (value: number): string => {
  return `${(value * 100).toFixed(1)}%`;
};

export const formatTemperature = (temp: number): string => {
  // Convert from Kelvin to Celsius
  const celsius = temp - 273.15;
  return `${Math.round(celsius)}°C`;
};

export const formatWindSpeed = (speed: number): string => {
  return `${Math.round(speed)} m/s`;
};

export const formatPressure = (pressure: number): string => {
  return `${Math.round(pressure)} hPa`;
};

export const formatHumidity = (humidity: number): string => {
  return `${Math.round(humidity)}%`;
};

export const getWeatherSummary = (weatherData: WeatherData) => {
  return {
    temperature: formatTemperature(weatherData.main.temp),
    humidity: formatHumidity(weatherData.main.humidity),
    pressure: formatPressure(weatherData.main.pressure),
    wind_speed: formatWindSpeed(weatherData.wind.speed),
    visibility: `${(weatherData.visibility / 1000).toFixed(1)} km`,
    description: weatherData.weather[0]?.description || "Unknown",
  };
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}; 