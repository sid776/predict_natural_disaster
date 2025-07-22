import React from "react";
import {
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Typography,
  Alert,
  Paper,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { PlayArrow } from "@mui/icons-material";
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
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  return (
    <Paper
      elevation={0}
      sx={{
        backgroundColor: COLORS.sidebar_bg,
        border: `1px solid ${COLORS.sidebar_border}`,
        borderRadius: 2,
        p: 3,
        width: isMobile ? "100%" : 350,
        height: "fit-content",
        position: "sticky",
        top: 16,
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={3} color={COLORS.text}>
        Prediction Controls
      </Typography>

      {/* Location Input */}
      <TextField
        fullWidth
        label="Location"
        value={location}
        onChange={(e) => onLocationChange(e.target.value)}
        placeholder="Enter city, state, or coordinates"
        variant="outlined"
        sx={{
          mb: 3,
          "& .MuiOutlinedInput-root": {
            color: COLORS.text,
            backgroundColor: "#ffffff",
            "& fieldset": {
              borderColor: COLORS.sidebar_border,
            },
            "&:hover fieldset": {
              borderColor: COLORS.guide,
            },
            "&.Mui-focused fieldset": {
              borderColor: COLORS.guide,
            },
          },
          "& .MuiInputLabel-root": {
            color: COLORS.text_secondary,
          },
        }}
      />

      {/* Model Selection */}
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel sx={{ color: COLORS.text_secondary }}>Model</InputLabel>
        <Select
          value={selectedModel}
          onChange={(e) => onModelChange(e.target.value as PredictionModel)}
          label="Model"
          sx={{
            color: COLORS.text,
            backgroundColor: "#ffffff",
            "& .MuiOutlinedInput-notchedOutline": {
              borderColor: COLORS.sidebar_border,
            },
            "&:hover .MuiOutlinedInput-notchedOutline": {
              borderColor: COLORS.guide,
            },
            "&.Mui-focused .MuiOutlinedInput-notchedOutline": {
              borderColor: COLORS.guide,
            },
          }}
        >
          {Object.entries(PREDICTION_MODELS).map(([key, model]) => (
            <MenuItem key={key} value={key}>
              <Box display="flex" alignItems="center" gap={1}>
                <Typography variant="body2">{model.label}</Typography>
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
        disabled={loading || !location.trim()}
        startIcon={<PlayArrow />}
        sx={{
          backgroundColor: COLORS.guide,
          color: COLORS.text,
          py: 1.5,
          fontSize: "1.1rem",
          fontWeight: "bold",
          "&:hover": {
            backgroundColor: COLORS.guide,
            opacity: 0.9,
          },
          "&:disabled": {
            backgroundColor: COLORS.sidebar_border,
            color: COLORS.text_secondary,
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

      {/* Model Description */}
      <Box
        mt={3}
        p={2}
        sx={{ backgroundColor: COLORS.card_bg, borderRadius: 1 }}
      >
        <Typography variant="body2" color={COLORS.text_secondary} mb={1}>
          Selected Model:
        </Typography>
        <Typography variant="body1" fontWeight="bold" color={COLORS.text}>
          {PREDICTION_MODELS[selectedModel].label}
        </Typography>
        <Typography variant="caption" color={COLORS.text_secondary}>
          {PREDICTION_MODELS[selectedModel].description}
        </Typography>
      </Box>
    </Paper>
  );
};

export default Sidebar;
