import React, { useState, useEffect } from "react";
import {
  Box,
  Typography,
  Paper,
  Chip,
  Grid,
  Card,
  CardContent,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from "@mui/material";
import {
  Warning,
  Schedule,
  Timer,
  Speed,
  Navigation,
  ExitToApp,
} from "@mui/icons-material";
import { COLORS, DISASTER_TYPES } from "../utils/constants";
import { apiService } from "../services/api";

interface CountyPrediction {
  county: {
    name: string;
    coordinates: { lat: number; lon: number };
    distance_miles: number;
    population?: number;
  };
  predicted_impact_time_hours: number;
  risk_level: string;
  probability: number;
  weather_conditions: any;
  evacuation_priority: string;
}

interface DisasterProgression {
  direction_degrees: number;
  speed_mph: number;
  estimated_duration_hours: number;
  affected_counties: CountyPrediction[];
}

interface MultiCountyPredictionData {
  center_location: string;
  disaster_type: string;
  progression: DisasterProgression;
  evacuation_recommendations: {
    immediate_evacuation: any[];
    prepare_to_evacuate: any[];
    monitor_situation: any[];
  };
  timestamp: string;
}

interface MultiCountyPredictionProps {
  location: string;
  disasterType: string;
  model: string;
  dataSource: string;
}

const MultiCountyPrediction: React.FC<MultiCountyPredictionProps> = ({
  location,
  disasterType,
  model,
  dataSource,
}) => {
  const [data, setData] = useState<MultiCountyPredictionData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (location && disasterType) {
      fetchMultiCountyPrediction();
    }
  }, [location, disasterType, model, dataSource]);

  const fetchMultiCountyPrediction = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await apiService.getMultiCountyPrediction(
        location,
        disasterType,
        model,
        dataSource
      );
      setData(response);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to fetch multi-county prediction"
      );
    } finally {
      setLoading(false);
    }
  };

  const getRiskLevelColor = (riskLevel: string) => {
    switch (riskLevel) {
      case "CRITICAL":
        return "#DC2626";
      case "HIGH":
        return "#F97316";
      case "MEDIUM":
        return "#F59E0B";
      case "LOW":
        return "#16A34A";
      default:
        return COLORS.text_secondary;
    }
  };

  const getEvacuationPriorityColor = (priority: string) => {
    switch (priority) {
      case "IMMEDIATE":
        return "#DC2626";
      case "HIGH":
        return "#F97316";
      case "MEDIUM":
        return "#F59E0B";
      case "LOW":
        return "#16A34A";
      default:
        return COLORS.text_secondary;
    }
  };

  const formatTime = (hours: number) => {
    if (hours === 0) return "Immediate";
    if (hours < 1) return `${Math.round(hours * 60)} minutes`;
    return `${hours.toFixed(1)} hours`;
  };

  const getDirectionName = (degrees: number) => {
    const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
    const index = Math.round(degrees / 45) % 8;
    return directions[index];
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" py={4}>
        <CircularProgress size={60} sx={{ color: COLORS.primary }} />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        {error}
      </Alert>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <Box>
      {/* Header */}
      <Paper
        elevation={0}
        sx={{
          background: COLORS.card_bg,
          border: `2px solid ${
            DISASTER_TYPES[disasterType as keyof typeof DISASTER_TYPES]?.color
          }`,
          borderRadius: 3,
          p: 4,
          mb: 3,
        }}
      >
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <Box sx={{ fontSize: "2rem" }}>
            {DISASTER_TYPES[disasterType as keyof typeof DISASTER_TYPES]?.icon}
          </Box>
          <Box>
            <Typography variant="h5" fontWeight="bold">
              Multi-County Impact Prediction
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {data.center_location} •{" "}
              {data.disaster_type.charAt(0).toUpperCase() +
                data.disaster_type.slice(1)}
            </Typography>
          </Box>
        </Box>

        {/* Progression Summary */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Box display="flex" alignItems="center" gap={1}>
              <Speed sx={{ color: COLORS.primary }} />
              <Typography variant="body2" fontWeight="bold">
                Speed: {data.progression.speed_mph} mph
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box display="flex" alignItems="center" gap={1}>
              <Navigation sx={{ color: COLORS.primary }} />
              <Typography variant="body2" fontWeight="bold">
                Direction:{" "}
                {getDirectionName(data.progression.direction_degrees)} (
                {data.progression.direction_degrees}°)
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Box display="flex" alignItems="center" gap={1}>
              <Timer sx={{ color: COLORS.primary }} />
              <Typography variant="body2" fontWeight="bold">
                Duration: {data.progression.estimated_duration_hours.toFixed(1)}{" "}
                hours
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* County Predictions */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Paper
            elevation={0}
            sx={{
              background: COLORS.card_bg,
              border: `1px solid ${COLORS.glass_border}`,
              borderRadius: 3,
              p: 4,
              boxShadow: COLORS.glass_shadow,
            }}
          >
            <Typography variant="h6" fontWeight="bold" mb={3}>
              📍 Affected Counties Timeline
            </Typography>

            <Box display="flex" flexDirection="column" gap={2}>
              {data.progression.affected_counties.map((county) => (
                <Card
                  key={county.county.name}
                  sx={{
                    border: `2px solid ${getRiskLevelColor(county.risk_level)}`,
                    borderRadius: 2,
                    background: `${getRiskLevelColor(county.risk_level)}10`,
                  }}
                >
                  <CardContent>
                    <Box
                      display="flex"
                      justifyContent="space-between"
                      alignItems="center"
                      mb={2}
                    >
                      <Box>
                        <Typography variant="h6" fontWeight="bold">
                          {county.county.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {county.county.distance_miles.toFixed(1)} miles away
                        </Typography>
                      </Box>
                      <Box display="flex" gap={1}>
                        <Chip
                          label={county.risk_level}
                          size="small"
                          sx={{
                            backgroundColor: getRiskLevelColor(
                              county.risk_level
                            ),
                            color: "white",
                            fontWeight: "bold",
                          }}
                        />
                        <Chip
                          label={county.evacuation_priority}
                          size="small"
                          sx={{
                            backgroundColor: getEvacuationPriorityColor(
                              county.evacuation_priority
                            ),
                            color: "white",
                            fontWeight: "bold",
                          }}
                        />
                      </Box>
                    </Box>

                    <Grid container spacing={2}>
                      <Grid item xs={6} md={3}>
                        <Box textAlign="center">
                          <Typography variant="caption" color="text.secondary">
                            Impact Time
                          </Typography>
                          <Typography
                            variant="h6"
                            fontWeight="bold"
                            color={COLORS.primary}
                          >
                            {formatTime(county.predicted_impact_time_hours)}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Box textAlign="center">
                          <Typography variant="caption" color="text.secondary">
                            Probability
                          </Typography>
                          <Typography
                            variant="h6"
                            fontWeight="bold"
                            color={COLORS.primary}
                          >
                            {county.probability.toFixed(1)}%
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Box textAlign="center">
                          <Typography variant="caption" color="text.secondary">
                            Population
                          </Typography>
                          <Typography
                            variant="h6"
                            fontWeight="bold"
                            color={COLORS.primary}
                          >
                            {county.county.population?.toLocaleString() ||
                              "N/A"}
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={6} md={3}>
                        <Box textAlign="center">
                          <Typography variant="caption" color="text.secondary">
                            Priority
                          </Typography>
                          <Typography
                            variant="h6"
                            fontWeight="bold"
                            color={getEvacuationPriorityColor(
                              county.evacuation_priority
                            )}
                          >
                            {county.evacuation_priority}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              ))}
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Paper
            elevation={0}
            sx={{
              background: COLORS.card_bg,
              border: `1px solid ${COLORS.glass_border}`,
              borderRadius: 3,
              p: 4,
              boxShadow: COLORS.glass_shadow,
            }}
          >
            <Typography variant="h6" fontWeight="bold" mb={3}>
              🚨 Evacuation Recommendations
            </Typography>

            {/* Immediate Evacuation */}
            {data.evacuation_recommendations.immediate_evacuation.length >
              0 && (
              <Box mb={3}>
                <Alert severity="error" sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold">
                    IMMEDIATE EVACUATION REQUIRED
                  </Typography>
                </Alert>
                <List dense>
                  {data.evacuation_recommendations.immediate_evacuation.map(
                    (item, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <ExitToApp sx={{ color: "#DC2626" }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={item.county}
                          secondary={`${item.time_remaining} • ${item.risk_level} Risk`}
                        />
                      </ListItem>
                    )
                  )}
                </List>
              </Box>
            )}

            {/* Prepare to Evacuate */}
            {data.evacuation_recommendations.prepare_to_evacuate.length > 0 && (
              <Box mb={3}>
                <Alert severity="warning" sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold">
                    PREPARE TO EVACUATE
                  </Typography>
                </Alert>
                <List dense>
                  {data.evacuation_recommendations.prepare_to_evacuate.map(
                    (item, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Warning sx={{ color: "#F97316" }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={item.county}
                          secondary={`${item.time_remaining} • ${item.risk_level} Risk`}
                        />
                      </ListItem>
                    )
                  )}
                </List>
              </Box>
            )}

            {/* Monitor Situation */}
            {data.evacuation_recommendations.monitor_situation.length > 0 && (
              <Box>
                <Alert severity="info" sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" fontWeight="bold">
                    MONITOR SITUATION
                  </Typography>
                </Alert>
                <List dense>
                  {data.evacuation_recommendations.monitor_situation.map(
                    (item, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Schedule sx={{ color: "#0EA5E9" }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={item.county}
                          secondary={`${item.time_remaining} • ${item.risk_level} Risk`}
                        />
                      </ListItem>
                    )
                  )}
                </List>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default MultiCountyPrediction;
