import React from "react";
import {
  Paper,
  Typography,
  TextField,
  FormControl,
  Select,
  MenuItem,
  Button,
  Box,
  Alert,
  Chip,
  Divider,
} from "@mui/material";
import {
  LocationOn,
  Psychology,
  PlayArrow,
  Schedule,
  TrendingUp,
  Info,
} from "@mui/icons-material";
import { COLORS, PREDICTION_MODELS } from "../../utils/constants";
import type { PredictionModel } from "../../types";

interface SidebarProps {
  location: string;
  selectedModel: PredictionModel;
  onLocationChange: (location: string) => void;
  onModelChange: (model: PredictionModel) => void;
  onPredict: () => void;
  loading: boolean;
  error: string | null;
}

const Sidebar: React.FC<SidebarProps> = ({
  location,
  selectedModel,
  onLocationChange,
  onModelChange,
  onPredict,
  loading,
  error,
}) => {
  return (
    <Paper
      elevation={0}
      sx={{
        background: COLORS.gradient_glass,
        backdropFilter: "blur(20px)",
        border: `1px solid ${COLORS.glass_border}`,
        borderRadius: 3,
        p: 3,
        height: "fit-content",
        position: "sticky",
        top: 20,
        boxShadow: COLORS.glass_shadow,
      }}
    >
      {/* Header */}
      <Box mb={3}>
        <Typography variant="h6" fontWeight="bold" color={COLORS.text} mb={1}>
          Prediction Controls
        </Typography>
        <Typography variant="body2" color={COLORS.text_secondary}>
          Configure AI model and location parameters
        </Typography>
      </Box>

      {/* Location Input */}
      <Box mb={3}>
        <Typography variant="body2" fontWeight="600" color={COLORS.text} mb={1}>
          Target Location
        </Typography>
        <TextField
          fullWidth
          value={location}
          onChange={(e) => onLocationChange(e.target.value)}
          placeholder="Enter city name (e.g., Miami, FL)"
          variant="outlined"
          size="small"
          InputProps={{
            startAdornment: (
              <LocationOn sx={{ color: COLORS.text_secondary, mr: 1 }} />
            ),
          }}
          sx={{
            "& .MuiOutlinedInput-root": {
              backgroundColor: "rgba(255, 255, 255, 0.05)",
              border: `1px solid ${COLORS.glass_border}`,
              borderRadius: 2,
              "&:hover": {
                borderColor: COLORS.primary,
              },
              "&.Mui-focused": {
                borderColor: COLORS.primary,
                boxShadow: `0 0 0 2px ${COLORS.primary}20`,
              },
            },
            "& .MuiInputBase-input": {
              color: COLORS.text,
            },
            "& .MuiInputLabel-root": {
              color: COLORS.text_secondary,
            },
          }}
        />
      </Box>

      {/* Model Selection */}
      <Box mb={3}>
        <Typography variant="body2" fontWeight="600" color={COLORS.text} mb={1}>
          AI Model Selection
        </Typography>
        <FormControl fullWidth size="small">
          <Select
            value={selectedModel}
            onChange={(e) => onModelChange(e.target.value as PredictionModel)}
            sx={{
              backgroundColor: "rgba(255, 255, 255, 0.05)",
              border: `1px solid ${COLORS.glass_border}`,
              borderRadius: 2,
              "& .MuiSelect-select": {
                color: COLORS.text,
              },
              "& .MuiOutlinedInput-notchedOutline": {
                border: "none",
              },
              "&:hover": {
                borderColor: COLORS.primary,
              },
              "&.Mui-focused": {
                borderColor: COLORS.primary,
                boxShadow: `0 0 0 2px ${COLORS.primary}20`,
              },
            }}
          >
            {Object.entries(PREDICTION_MODELS).map(([key, model]) => (
              <MenuItem key={key} value={key}>
                <Box display="flex" alignItems="center" gap={2}>
                  <Box
                    sx={{
                      width: 32,
                      height: 32,
                      borderRadius: 1,
                      backgroundColor: `${model.color}20`,
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <Psychology sx={{ fontSize: 18, color: model.color }} />
                  </Box>
                  <Box>
                    <Typography
                      variant="body2"
                      fontWeight="bold"
                      color={COLORS.text}
                    >
                      {model.label}
                    </Typography>
                    <Typography variant="caption" color={COLORS.text_secondary}>
                      {model.description}
                    </Typography>
                  </Box>
                </Box>
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* Model Info Card */}
      <Box
        mb={3}
        sx={{
          backgroundColor: "rgba(255, 255, 255, 0.05)",
          borderRadius: 2,
          p: 2,
          border: `1px solid ${COLORS.glass_border}`,
        }}
      >
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Info sx={{ fontSize: 16, color: COLORS.accent }} />
          <Typography variant="body2" fontWeight="600" color={COLORS.text}>
            Selected Model
          </Typography>
        </Box>
        <Box display="flex" alignItems="center" gap={2}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: 1.5,
              backgroundColor: `${PREDICTION_MODELS[selectedModel].color}20`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Psychology
              sx={{
                fontSize: 20,
                color: PREDICTION_MODELS[selectedModel].color,
              }}
            />
          </Box>
          <Box>
            <Typography variant="body1" fontWeight="bold" color={COLORS.text}>
              {PREDICTION_MODELS[selectedModel].label}
            </Typography>
            <Typography variant="caption" color={COLORS.text_secondary}>
              {PREDICTION_MODELS[selectedModel].description}
            </Typography>
          </Box>
        </Box>
      </Box>

      <Divider sx={{ my: 3, borderColor: COLORS.glass_border }} />

      {/* Predict Button */}
      <Button
        fullWidth
        variant="contained"
        onClick={onPredict}
        disabled={loading || !location.trim()}
        startIcon={loading ? <Schedule /> : <PlayArrow />}
        sx={{
          background: COLORS.gradient_primary,
          color: "#ffffff",
          py: 1.5,
          fontSize: "1rem",
          fontWeight: "700",
          borderRadius: 3,
          textTransform: "none",
          boxShadow: "0 4px 12px rgba(26, 35, 126, 0.4)",
          "&:hover": {
            background: COLORS.gradient_secondary,
            boxShadow: "0 6px 16px rgba(124, 58, 237, 0.5)",
            transform: "translateY(-1px)",
          },
          "&:disabled": {
            background: COLORS.muted,
            color: COLORS.text_secondary,
            boxShadow: "none",
            transform: "none",
          },
        }}
      >
        {loading ? "Processing..." : "Run Prediction"}
      </Button>

      {/* Status Indicators */}
      <Box mt={2} display="flex" gap={1}>
        <Chip
          icon={<TrendingUp />}
          label="Real-time"
          size="small"
          sx={{
            backgroundColor: "rgba(16, 185, 129, 0.2)",
            color: "#10b981",
            border: "1px solid rgba(16, 185, 129, 0.3)",
            "& .MuiChip-icon": {
              color: "#10b981",
            },
          }}
        />
        <Chip
          label="High Accuracy"
          size="small"
          sx={{
            backgroundColor: "rgba(59, 130, 246, 0.2)",
            color: "#3b82f6",
            border: "1px solid rgba(59, 130, 246, 0.3)",
          }}
        />
      </Box>

      {/* Error Display */}
      {error && (
        <Alert
          severity="error"
          sx={{
            mt: 2,
            backgroundColor: "rgba(239, 68, 68, 0.1)",
            border: "1px solid rgba(239, 68, 68, 0.3)",
            color: "#ef4444",
          }}
        >
          {error}
        </Alert>
      )}
    </Paper>
  );
};

export default Sidebar;
