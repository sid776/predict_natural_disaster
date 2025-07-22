import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import type { DisasterType } from "../../types";

interface ProbabilityGaugeProps {
  probability: number;
  disasterType: DisasterType;
}

const ProbabilityGauge: React.FC<ProbabilityGaugeProps> = ({
  probability,
  disasterType,
}) => {
  const percentage = probability * 100;
  const color = DISASTER_TYPES[disasterType].color;

  // Calculate gauge angle (0-180 degrees)
  const angle = (percentage / 100) * 180;

  return (
    <Paper
      elevation={0}
      sx={{
        backgroundColor: COLORS.card_bg,
        border: `2px solid ${color}`,
        borderRadius: 3,
        p: 3,
        textAlign: "center",
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={2} color={COLORS.text}>
        Probability Gauge
      </Typography>

      {/* Gauge Visualization */}
      <Box
        sx={{
          position: "relative",
          width: 200,
          height: 100,
          mx: "auto",
          mb: 2,
        }}
      >
        {/* Gauge Background */}
        <Box
          sx={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: 100,
            borderRadius: "100px 100px 0 0",
            background: `conic-gradient(from 0deg, ${color} 0deg, ${color} ${angle}deg, ${COLORS.sidebar_border} ${angle}deg, ${COLORS.sidebar_border} 180deg)`,
          }}
        />

        {/* Gauge Center */}
        <Box
          sx={{
            position: "absolute",
            top: 10,
            left: "50%",
            transform: "translateX(-50%)",
            width: 180,
            height: 80,
            borderRadius: "90px 90px 0 0",
            backgroundColor: COLORS.card_bg,
          }}
        />

        {/* Needle */}
        <Box
          sx={{
            position: "absolute",
            bottom: 0,
            left: "50%",
            transform: `translateX(-50%) rotate(${angle - 90}deg)`,
            width: 4,
            height: 80,
            backgroundColor: color,
            borderRadius: 2,
            transformOrigin: "bottom center",
            transition: "transform 0.5s ease-in-out",
          }}
        />

        {/* Center Point */}
        <Box
          sx={{
            position: "absolute",
            bottom: 0,
            left: "50%",
            transform: "translateX(-50%)",
            width: 12,
            height: 12,
            backgroundColor: color,
            borderRadius: "50%",
          }}
        />
      </Box>

      {/* Percentage Display */}
      <Typography variant="h3" fontWeight="bold" color={color} sx={{ mb: 1 }}>
        {percentage.toFixed(1)}%
      </Typography>

      <Typography variant="body2" color={COLORS.text_secondary}>
        {DISASTER_TYPES[disasterType].label} Probability
      </Typography>

      {/* Risk Level */}
      <Box mt={2}>
        <Typography
          variant="body2"
          color={COLORS.text_secondary}
          sx={{ mb: 0.5 }}
        >
          Risk Level:
        </Typography>
        <Typography
          variant="body1"
          fontWeight="bold"
          color={
            percentage < 30
              ? COLORS.success
              : percentage < 70
              ? COLORS.warning
              : COLORS.error
          }
        >
          {percentage < 30
            ? "Low Risk"
            : percentage < 70
            ? "Medium Risk"
            : "High Risk"}
        </Typography>
      </Box>
    </Paper>
  );
};

export default ProbabilityGauge;
