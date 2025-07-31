import React, { useState, useEffect } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Alert,
  CircularProgress,
  Collapse,
  IconButton,
  Badge,
} from "@mui/material";
import {
  Warning as WarningIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
  AccessTime as TimeIcon,
  LocationOn as LocationIcon,
  Info as InfoIcon,
} from "@mui/icons-material";
import { apiService } from "../services/api";
import type { WeatherAlert } from "../types";
import { COLORS } from "../utils/constants";

interface WeatherAlertsProps {
  location: string;
  coordinates?: { lat: number; lon: number };
}

const getSeverityColor = (severity: string): string => {
  switch (severity.toLowerCase()) {
    case "extreme":
      return "#d32f2f";
    case "severe":
      return "#f57c00";
    case "moderate":
      return "#fbc02d";
    case "minor":
      return "#388e3c";
    default:
      return "#757575";
  }
};

const getUrgencyColor = (urgency: string): string => {
  switch (urgency.toLowerCase()) {
    case "immediate":
      return "#d32f2f";
    case "expected":
      return "#f57c00";
    case "future":
      return "#388e3c";
    default:
      return "#757575";
  }
};

const formatDateTime = (dateString: string): string => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString();
  } catch {
    return dateString;
  }
};

const WeatherAlerts: React.FC<WeatherAlertsProps> = ({
  location,
  coordinates,
}) => {
  const [alerts, setAlerts] = useState<WeatherAlert[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedAlerts, setExpandedAlerts] = useState<Set<string>>(new Set());

  useEffect(() => {
    const fetchAlerts = async () => {
      if (!location) return;

      setLoading(true);
      setError(null);

      try {
        let alertsData: WeatherAlert[] = [];

        if (coordinates) {
          // Use coordinates if available for more accurate results
          alertsData = await apiService.getWeatherAlertsByCoordinates(
            coordinates.lat,
            coordinates.lon
          );
        } else {
          // Fallback to location string
          alertsData = await apiService.getWeatherAlerts(location);
        }

        setAlerts(alertsData);
      } catch (err: any) {
        const errorMessage = err?.message || "Failed to fetch weather alerts";
        setError(errorMessage);
        console.error("Error fetching weather alerts:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAlerts();
  }, [location, coordinates]);

  const toggleAlertExpansion = (alertId: string) => {
    const newExpanded = new Set(expandedAlerts);
    if (newExpanded.has(alertId)) {
      newExpanded.delete(alertId);
    } else {
      newExpanded.add(alertId);
    }
    setExpandedAlerts(newExpanded);
  };

  if (loading) {
    return (
      <Card
        sx={{
          backgroundColor: COLORS.card_bg,
          border: `1px solid ${COLORS.glass_border}`,
          backdropFilter: "blur(10px)",
          mb: 2,
        }}
      >
        <CardContent sx={{ textAlign: "center", py: 3 }}>
          <CircularProgress size={40} sx={{ color: COLORS.primary, mb: 2 }} />
          <Typography variant="body2" color={COLORS.text_secondary}>
            Fetching weather alerts...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Alert severity="warning" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  if (alerts.length === 0) {
    return (
      <Card
        sx={{
          backgroundColor: COLORS.card_bg,
          border: `1px solid ${COLORS.glass_border}`,
          backdropFilter: "blur(10px)",
          mb: 2,
        }}
      >
        <CardContent sx={{ textAlign: "center", py: 3 }}>
          <InfoIcon
            sx={{ fontSize: 40, color: COLORS.text_secondary, mb: 2 }}
          />
          <Typography variant="h6" color={COLORS.text} mb={1}>
            No Active Weather Alerts
          </Typography>
          <Typography variant="body2" color={COLORS.text_secondary}>
            No active weather alerts found for {location}
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <WarningIcon sx={{ color: "#f57c00", fontSize: 24 }} />
        <Typography variant="h6" color={COLORS.text} fontWeight="bold">
          Weather Alerts ({alerts.length})
        </Typography>
        <Badge badgeContent={alerts.length} color="warning" />
      </Box>

      {alerts.map((alert) => (
        <Card
          key={alert.id}
          sx={{
            backgroundColor: COLORS.card_bg,
            border: `1px solid ${getSeverityColor(alert.severity)}40`,
            backdropFilter: "blur(10px)",
            mb: 2,
            "&:hover": {
              borderColor: getSeverityColor(alert.severity),
              boxShadow: `0 4px 12px ${getSeverityColor(alert.severity)}20`,
            },
          }}
        >
          <CardContent sx={{ p: 0 }}>
            {/* Alert Header */}
            <Box
              sx={{
                p: 2,
                borderBottom: `1px solid ${COLORS.glass_border}`,
                cursor: "pointer",
              }}
              onClick={() => toggleAlertExpansion(alert.id)}
            >
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="flex-start"
              >
                <Box flex={1}>
                  <Box display="flex" alignItems="center" gap={1} mb={1}>
                    <Typography
                      variant="h6"
                      fontWeight="bold"
                      color={getSeverityColor(alert.severity)}
                    >
                      {alert.event}
                    </Typography>
                    <Chip
                      label={alert.severity}
                      size="small"
                      sx={{
                        backgroundColor: `${getSeverityColor(
                          alert.severity
                        )}20`,
                        color: getSeverityColor(alert.severity),
                        fontWeight: "bold",
                      }}
                    />
                    <Chip
                      label={alert.urgency}
                      size="small"
                      sx={{
                        backgroundColor: `${getUrgencyColor(alert.urgency)}20`,
                        color: getUrgencyColor(alert.urgency),
                        fontWeight: "bold",
                      }}
                    />
                  </Box>

                  <Typography variant="body1" color={COLORS.text} mb={1}>
                    {alert.headline}
                  </Typography>

                  <Box
                    display="flex"
                    alignItems="center"
                    gap={2}
                    flexWrap="wrap"
                  >
                    <Box display="flex" alignItems="center" gap={0.5}>
                      <LocationIcon
                        sx={{ fontSize: 16, color: COLORS.text_secondary }}
                      />
                      <Typography
                        variant="caption"
                        color={COLORS.text_secondary}
                      >
                        {alert.areas}
                      </Typography>
                    </Box>
                    <Box display="flex" alignItems="center" gap={0.5}>
                      <TimeIcon
                        sx={{ fontSize: 16, color: COLORS.text_secondary }}
                      />
                      <Typography
                        variant="caption"
                        color={COLORS.text_secondary}
                      >
                        Effective: {formatDateTime(alert.effective)}
                      </Typography>
                    </Box>
                  </Box>
                </Box>

                <IconButton size="small">
                  {expandedAlerts.has(alert.id) ? (
                    <ExpandLessIcon />
                  ) : (
                    <ExpandMoreIcon />
                  )}
                </IconButton>
              </Box>
            </Box>

            {/* Alert Details */}
            <Collapse in={expandedAlerts.has(alert.id)}>
              <Box sx={{ p: 2, backgroundColor: "rgba(255, 255, 255, 0.02)" }}>
                <Typography variant="body2" color={COLORS.text} mb={2}>
                  {alert.description}
                </Typography>

                <Box
                  display="grid"
                  gridTemplateColumns="repeat(auto-fit, minmax(200px, 1fr))"
                  gap={2}
                >
                  <Box>
                    <Typography variant="caption" color={COLORS.text_secondary}>
                      Category
                    </Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {alert.category}
                    </Typography>
                  </Box>

                  <Box>
                    <Typography variant="caption" color={COLORS.text_secondary}>
                      Certainty
                    </Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {alert.certainty}
                    </Typography>
                  </Box>

                  <Box>
                    <Typography variant="caption" color={COLORS.text_secondary}>
                      Status
                    </Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {alert.status}
                    </Typography>
                  </Box>

                  <Box>
                    <Typography variant="caption" color={COLORS.text_secondary}>
                      Expires
                    </Typography>
                    <Typography variant="body2" fontWeight="bold">
                      {formatDateTime(alert.expires)}
                    </Typography>
                  </Box>
                </Box>

                <Box mt={2}>
                  <Typography variant="caption" color={COLORS.text_secondary}>
                    Alert ID: {alert.id}
                  </Typography>
                </Box>
              </Box>
            </Collapse>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default WeatherAlerts;
