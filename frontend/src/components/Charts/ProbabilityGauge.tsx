import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import { PieChart, Pie, Cell, ResponsiveContainer } from "recharts";
import type { DisasterType } from "../../types";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import { getRiskLevel } from "../../utils/formatters";

interface ProbabilityGaugeProps {
  probability: number; // 0-1
  disasterType: DisasterType;
  title?: string;
  size?: "small" | "medium" | "large";
}

const ProbabilityGauge: React.FC<ProbabilityGaugeProps> = ({
  probability,
  disasterType,
  title,
  size = "medium",
}) => {
  const percentage = probability * 100;
  const riskLevel = getRiskLevel(probability);
  const disasterColor = DISASTER_TYPES[disasterType].color;

  // Create data for the gauge
  const gaugeData = [
    { name: "Probability", value: percentage, fill: disasterColor },
    { name: "Remaining", value: 100 - percentage, fill: "#f0f0f0" },
  ];

  const sizeConfig = {
    small: { width: 200, height: 200, fontSize: 16 },
    medium: { width: 300, height: 300, fontSize: 24 },
    large: { width: 400, height: 400, fontSize: 32 },
  };

  const config = sizeConfig[size];

  return (
    <Paper
      elevation={2}
      sx={{
        p: 3,
        backgroundColor: COLORS.card_bg,
        border: `2px solid ${disasterColor}`,
        borderRadius: 3,
      }}
    >
      <Typography
        variant="h6"
        component="h3"
        sx={{
          color: disasterColor,
          fontWeight: "bold",
          mb: 2,
          textAlign: "center",
        }}
      >
        {title || `${DISASTER_TYPES[disasterType].label} Probability`}
      </Typography>

      <Box
        sx={{
          width: config.width,
          height: config.height,
          mx: "auto",
          position: "relative",
        }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={gaugeData}
              cx="50%"
              cy="50%"
              innerRadius={config.width * 0.3}
              outerRadius={config.width * 0.4}
              startAngle={180}
              endAngle={-180}
              dataKey="value"
            >
              {gaugeData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.fill} />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>

        {/* Center text */}
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
            sx={{
              color: disasterColor,
              fontWeight: "bold",
              fontSize: config.fontSize,
              lineHeight: 1,
            }}
          >
            {percentage.toFixed(1)}%
          </Typography>
          <Typography
            variant="body2"
            sx={{
              color: riskLevel.color,
              fontWeight: "bold",
              mt: 1,
            }}
          >
            {riskLevel.label}
          </Typography>
        </Box>
      </Box>

      {/* Risk level indicator */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 1,
          mt: 2,
        }}
      >
        <Box
          sx={{
            width: 12,
            height: 12,
            borderRadius: "50%",
            backgroundColor: riskLevel.color,
          }}
        />
        <Typography variant="body2" color="text.secondary">
          Risk Level: {riskLevel.label}
        </Typography>
      </Box>
    </Paper>
  );
};

export default ProbabilityGauge;
