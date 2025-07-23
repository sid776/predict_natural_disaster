import React from "react";
import { Box, Typography, Paper, Tooltip } from "@mui/material";
import { COLORS } from "../../utils/constants";
import type { DisasterType } from "../../types";

interface ProbabilityGaugeProps {
  probability: number;
  disasterType: DisasterType;
}

const ProbabilityGauge: React.FC<ProbabilityGaugeProps> = ({
  probability,
  disasterType,
}) => {
  const color = COLORS[disasterType];
  const percentage = probability * 100;
  const radius = 80;
  const strokeWidth = 12;
  const circumference = 2 * Math.PI * radius;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  // Determine risk level and color
  const getRiskLevel = (prob: number) => {
    if (prob < 0.3) return { level: "Low", color: "#10b981" };
    if (prob < 0.6) return { level: "Medium", color: "#f59e0b" };
    return { level: "High", color: "#ef4444" };
  };

  const riskInfo = getRiskLevel(probability);

  return (
    <Paper
      elevation={0}
      sx={{
        background: COLORS.gradient_glass,
        backdropFilter: "blur(20px)",
        border: `2px solid ${color}`,
        borderRadius: 3,
        p: 4,
        textAlign: "center",
        position: "relative",
        overflow: "hidden",
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "4px",
          background: `linear-gradient(90deg, ${color} 0%, ${COLORS.accent} 100%)`,
        },
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={3} color={COLORS.text}>
        Risk Assessment
      </Typography>

      {/* Radial Gauge */}
      <Box
        sx={{
          position: "relative",
          display: "inline-block",
          mb: 3,
        }}
      >
        {/* Background Circle */}
        <svg width={200} height={200} style={{ transform: "rotate(-90deg)" }}>
          <circle
            cx={100}
            cy={100}
            r={radius}
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth={strokeWidth}
          />

          {/* Progress Circle */}
          <circle
            cx={100}
            cy={100}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            style={{
              transition: "stroke-dashoffset 1s ease-in-out",
              filter: "drop-shadow(0 0 8px rgba(239, 68, 68, 0.3))",
            }}
          />
        </svg>

        {/* Center Content */}
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            textAlign: "center",
          }}
        >
          <Typography
            variant="h3"
            fontWeight="bold"
            color={color}
            sx={{
              fontSize: "2.5rem",
              lineHeight: 1,
              mb: 0.5,
            }}
          >
            {percentage.toFixed(1)}%
          </Typography>
          <Typography
            variant="body2"
            color={COLORS.text_secondary}
            sx={{ fontSize: "0.875rem" }}
          >
            Probability
          </Typography>
        </Box>
      </Box>

      {/* Risk Level Indicator */}
      <Box
        sx={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 2,
          mb: 2,
        }}
      >
        <Box
          sx={{
            width: 12,
            height: 12,
            borderRadius: "50%",
            backgroundColor: riskInfo.color,
            boxShadow: `0 0 8px ${riskInfo.color}40`,
          }}
        />
        <Typography variant="h6" fontWeight="bold" color={riskInfo.color}>
          {riskInfo.level} Risk
        </Typography>
      </Box>

      {/* Risk Description */}
      <Tooltip
        title={`This ${disasterType} has a ${percentage.toFixed(
          1
        )}% probability based on current weather conditions and historical data analysis.`}
        arrow
      >
        <Typography
          variant="body2"
          color={COLORS.text_secondary}
          sx={{
            cursor: "help",
            maxWidth: 300,
            mx: "auto",
            lineHeight: 1.5,
          }}
        >
          Based on current conditions and AI analysis
        </Typography>
      </Tooltip>

      {/* Confidence Indicator */}
      <Box
        sx={{
          mt: 2,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 1,
        }}
      >
        <Box
          sx={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: "#10b981",
            animation: "pulse 2s infinite",
          }}
        />
        <Typography variant="caption" color={COLORS.text_secondary}>
          High Confidence Model
        </Typography>
      </Box>

      <style>
        {`
          @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
          }
        `}
      </style>
    </Paper>
  );
};

export default ProbabilityGauge;
