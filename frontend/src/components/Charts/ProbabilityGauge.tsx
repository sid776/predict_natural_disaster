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

  // Enhanced risk level with vibrant colors and gradients
  const getRiskLevel = (prob: number) => {
    if (prob < 0.3)
      return {
        level: "Low",
        color: COLORS.success,
        gradient: COLORS.gradient_low_risk,
        glowColor: "#00ff88",
      };
    if (prob < 0.6)
      return {
        level: "Medium",
        color: COLORS.warning,
        gradient: COLORS.gradient_medium_risk,
        glowColor: "#ff8c42",
      };
    return {
      level: "High",
      color: COLORS.error,
      gradient: COLORS.gradient_high_risk,
      glowColor: "#ff4757",
    };
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
        transition: "all 0.3s ease",
        "&:hover": {
          transform: "translateY(-4px)",
          boxShadow: `0 12px 40px 0 rgba(31, 38, 135, 0.5), 0 0 20px ${riskInfo.glowColor}40`,
        },
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "4px",
          background: `linear-gradient(90deg, ${color} 0%, ${riskInfo.glowColor} 100%)`,
        },
        "&::after": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `linear-gradient(45deg, transparent 30%, ${riskInfo.glowColor}10 50%, transparent 70%)`,
          animation: "shimmer 3s ease-in-out infinite",
          pointerEvents: "none",
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
          <defs>
            <linearGradient
              id={`gauge-gradient-${disasterType}`}
              x1="0%"
              y1="0%"
              x2="100%"
              y2="0%"
            >
              <stop offset="0%" stopColor={color} />
              <stop offset="100%" stopColor={riskInfo.glowColor} />
            </linearGradient>
          </defs>

          <circle
            cx={100}
            cy={100}
            r={radius}
            fill="none"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth={strokeWidth}
          />

          {/* Progress Circle with Gradient */}
          <circle
            cx={100}
            cy={100}
            r={radius}
            fill="none"
            stroke={`url(#gauge-gradient-${disasterType})`}
            strokeWidth={strokeWidth}
            strokeLinecap="round"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            style={{
              transition: "stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
              filter: `drop-shadow(0 0 12px ${riskInfo.glowColor})`,
            }}
          />

          {/* Glow effect for high risk */}
          {percentage > 60 && (
            <circle
              cx={100}
              cy={100}
              r={radius + 4}
              fill="none"
              stroke={riskInfo.glowColor}
              strokeWidth="2"
              opacity="0.6"
              style={{
                filter: `drop-shadow(0 0 8px ${riskInfo.glowColor})`,
                animation: "pulse 2s ease-in-out infinite",
              }}
            />
          )}
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
              textShadow: `0 0 15px ${riskInfo.glowColor}`,
              animation:
                percentage > 50 ? "pulse 2s ease-in-out infinite" : "none",
              transition: "all 0.3s ease",
            }}
          >
            {percentage.toFixed(1)}%
          </Typography>
          <Typography
            variant="body2"
            color={COLORS.text_secondary}
            sx={{
              fontSize: "0.875rem",
              textShadow: `0 0 5px ${riskInfo.glowColor}`,
            }}
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
            background: riskInfo.gradient,
            boxShadow: `0 0 12px ${riskInfo.glowColor}`,
            animation:
              percentage > 50 ? "pulse 2s ease-in-out infinite" : "none",
          }}
        />
        <Typography
          variant="h6"
          fontWeight="bold"
          color={riskInfo.color}
          sx={{
            textShadow: `0 0 8px ${riskInfo.glowColor}`,
            animation:
              percentage > 60 ? "pulse 1.5s ease-in-out infinite" : "none",
          }}
        >
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
          
          @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }
        `}
      </style>
    </Paper>
  );
};

export default ProbabilityGauge;
