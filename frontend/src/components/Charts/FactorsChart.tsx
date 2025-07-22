import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import type { DisasterType, FactorImpacts } from "../../types";

interface FactorsChartProps {
  factors: FactorImpacts;
  disasterType: DisasterType;
}

const FactorsChart: React.FC<FactorsChartProps> = ({
  factors,
  disasterType,
}) => {
  const color = DISASTER_TYPES[disasterType].color;

  // Transform factors data for the chart
  const chartData = Object.entries(factors)
    .filter(([, value]) => value !== undefined && value !== null)
    .map(([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1).replace("_", " "),
      value: value || 0,
      impact: value > 0 ? "positive" : value < 0 ? "negative" : "neutral",
    }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value)) // Sort by absolute impact
    .slice(0, 10); // Show top 10 factors

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const factor = chartData.find((item) => item.name === label);
      return (
        <Box
          sx={{
            backgroundColor: COLORS.card_bg,
            border: `1px solid ${COLORS.sidebar_border}`,
            borderRadius: 1,
            p: 1,
          }}
        >
          <Typography variant="body2" color={COLORS.text} fontWeight="bold">
            {label}
          </Typography>
          <Typography variant="body2" color={COLORS.text_secondary}>
            Impact: {payload[0].value.toFixed(1)}%
          </Typography>
          <Typography variant="body2" color={COLORS.text_secondary}>
            Type: {factor?.impact}
          </Typography>
        </Box>
      );
    }
    return null;
  };

  return (
    <Paper
      elevation={0}
      sx={{
        background: `linear-gradient(135deg, ${COLORS.card_bg} 0%, ${COLORS.main_bg} 100%)`,
        border: `2px solid ${color}`,
        borderRadius: "16px",
        p: 3,
        boxShadow: `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`,
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
      <Typography variant="h6" fontWeight="bold" mb={2} color={COLORS.text}>
        Contributing Factors
      </Typography>

      {chartData.length > 0 ? (
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="horizontal">
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={COLORS.sidebar_border}
              />
              <XAxis
                type="number"
                stroke={COLORS.text_secondary}
                fontSize={12}
                tickFormatter={(value) => `${value}%`}
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke={COLORS.text_secondary}
                fontSize={12}
                width={100}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="value" fill={color} radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Box>
      ) : (
        <Box
          sx={{
            height: 300,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Typography variant="body2" color={COLORS.text_secondary}>
            No factor data available
          </Typography>
        </Box>
      )}

      {/* Factor Summary */}
      {chartData.length > 0 && (
        <Box
          mt={2}
          p={2}
          sx={{ backgroundColor: COLORS.sidebar_bg, borderRadius: 1 }}
        >
          <Typography variant="body2" color={COLORS.text_secondary} mb={1}>
            Top Factors:
          </Typography>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {chartData.slice(0, 3).map((factor) => (
              <Box
                key={factor.name}
                sx={{
                  px: 1,
                  py: 0.5,
                  backgroundColor: color,
                  color: COLORS.text,
                  borderRadius: 1,
                  fontSize: "0.75rem",
                }}
              >
                {factor.name}
              </Box>
            ))}
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default FactorsChart;
