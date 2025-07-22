import React from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Alert,
  CircularProgress,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { LocationOn, Psychology, TrendingUp } from "@mui/icons-material";
import type { PredictionModel, DisasterType } from "../../types";
import { COLORS, PREDICTION_MODELS } from "../../utils/constants";
import { validateLocation } from "../../utils/formatters";

interface SidebarProps {
  location: string;
  selectedModel: PredictionModel;
  onLocationChange: (location: string) => void;
  onModelChange: (model: PredictionModel) => void;
  onPredict: () => void;
  loading: boolean;
  error: string | null;
  forecastData?: Array<{ date: string; probability: number }>;
}

const Sidebar: React.FC<SidebarProps> = ({
  location,
  selectedModel,
  onLocationChange,
  onModelChange,
  onPredict,
  loading,
  error,
  forecastData,
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  const isLocationValid = validateLocation(location);
  const canPredict = isLocationValid && location.trim().length > 0 && !loading;

  return (
    <Box
      sx={{
        width: isMobile ? "100%" : 320,
        p: 2,
        backgroundColor: COLORS.sidebar_bg,
        borderRight: isMobile ? "none" : `2px solid ${COLORS.sidebar_border}`,
        minHeight: "100vh",
      }}
    >
      <Typography
        variant="h5"
        component="h2"
        sx={{
          color: COLORS.earthquake,
          fontWeight: "bold",
          mb: 3,
          textAlign: "center",
        }}
      >
        Input Parameters
      </Typography>

      {/* Location Input */}
      <Card
        sx={{
          mb: 3,
          backgroundColor: COLORS.sidebar_bg,
          border: `2px solid ${COLORS.sidebar_border}`,
        }}
      >
        <CardContent>
          <Typography
            variant="h6"
            sx={{
              color: COLORS.guide,
              mb: 2,
              display: "flex",
              alignItems: "center",
              gap: 1,
            }}
          >
            <LocationOn />
            Location
          </Typography>

          <TextField
            fullWidth
            label="Enter city, state"
            value={location}
            onChange={(e) => onLocationChange(e.target.value)}
            variant="outlined"
            size="small"
            sx={{
              mb: 2,
              "& .MuiOutlinedInput-root": {
                borderColor: COLORS.guide,
              },
            }}
            error={location.length > 0 && !isLocationValid}
            helperText={
              location.length > 0 && !isLocationValid
                ? 'Please enter a valid location (e.g., "New York, NY")'
                : ""
            }
          />

          {/* Model Selection */}
          <Typography
            variant="h6"
            sx={{
              color: COLORS.guide,
              mb: 2,
              mt: 3,
              display: "flex",
              alignItems: "center",
              gap: 1,
            }}
          >
            <Psychology />
            Prediction Model
          </Typography>

          <FormControl fullWidth size="small" sx={{ mb: 3 }}>
            <InputLabel>Select Model</InputLabel>
            <Select
              value={selectedModel}
              label="Select Model"
              onChange={(e) => onModelChange(e.target.value as PredictionModel)}
            >
              {Object.entries(PREDICTION_MODELS).map(([key, model]) => (
                <MenuItem key={key} value={key}>
                  <Box display="flex" alignItems="center" gap={1}>
                    <span>{model.icon}</span>
                    <Box>
                      <Typography variant="body2" fontWeight="bold">
                        {model.label}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {model.description}
                      </Typography>
                    </Box>
                  </Box>
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {/* Predict Button */}
          <Button
            fullWidth
            variant="contained"
            onClick={onPredict}
            disabled={!canPredict}
            startIcon={
              loading ? <CircularProgress size={20} /> : <TrendingUp />
            }
            sx={{
              backgroundColor: COLORS.sidebar_button,
              color: COLORS.sidebar_button_text,
              fontWeight: "bold",
              py: 1.5,
              "&:hover": {
                backgroundColor: COLORS.earthquake,
              },
              "&:disabled": {
                backgroundColor: COLORS.text,
                color: COLORS.white,
              },
            }}
          >
            {loading ? "Predicting..." : "Predict"}
          </Button>

          {/* Error Display */}
          {error && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {error}
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* 30-Day Forecast Card */}
      <Card
        sx={{
          backgroundColor: COLORS.card_bg,
          border: `2px solid ${COLORS.tornado}`,
        }}
      >
        <CardContent>
          <Typography
            variant="h6"
            sx={{
              color: COLORS.tornado,
              mb: 2,
              display: "flex",
              alignItems: "center",
              gap: 1,
            }}
          >
            <TrendingUp />
            30-Day Tornado Forecast
          </Typography>

          {forecastData && forecastData.length > 0 ? (
            <Box>
              <Typography variant="body2" color="text.secondary" mb={1}>
                Average Probability:
              </Typography>
              <Typography
                variant="h4"
                sx={{
                  color: COLORS.tornado,
                  fontWeight: "bold",
                  textAlign: "center",
                }}
              >
                {(
                  (forecastData.reduce((sum, day) => sum + day.probability, 0) /
                    forecastData.length) *
                  100
                ).toFixed(1)}
                %
              </Typography>

              <Box mt={2}>
                <Typography variant="body2" color="text.secondary" mb={1}>
                  Recent Trend:
                </Typography>
                <Box
                  display="flex"
                  justifyContent="space-between"
                  alignItems="center"
                >
                  {forecastData.slice(-7).map((day, index) => (
                    <Box
                      key={day.date}
                      sx={{
                        width: 20,
                        height: 20,
                        backgroundColor: COLORS.tornado,
                        opacity: 0.3 + index * 0.1,
                        borderRadius: "50%",
                      }}
                    />
                  ))}
                </Box>
              </Box>
            </Box>
          ) : (
            <Typography
              variant="body2"
              color="text.secondary"
              textAlign="center"
            >
              Enter a location and click predict to see the forecast
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default Sidebar;
