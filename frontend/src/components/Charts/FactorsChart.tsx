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
    .filter(([, value]) => value !== undefined && value !== null && value > 0)
    .map(([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1).replace("_", " "),
      value: Math.abs(value || 0), // Use absolute value for display
      originalValue: value || 0,
      impact: value > 0 ? "positive" : value < 0 ? "negative" : "neutral",
    }))
    .sort((a, b) => b.value - a.value) // Sort by impact value
    .slice(0, 10); // Show top 10 factors

  // If no data after filtering, show at least one factor with 0 value
  if (chartData.length === 0) {
    const firstFactor = Object.keys(factors)[0];
    if (firstFactor) {
      chartData.push({
        name:
          firstFactor.charAt(0).toUpperCase() +
          firstFactor.slice(1).replace("_", " "),
        value: 0,
        originalValue: 0,
        impact: "neutral",
      });
    }
  }

  // Debug logging
  console.log("Factors data:", factors);
  console.log("Chart data:", chartData);
  console.log("Chart data length:", chartData.length);
  console.log("First chart item:", chartData[0]);

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
            Impact: {factor?.originalValue?.toFixed(1)}%
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
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={2}
      >
        <Typography variant="h6" fontWeight="bold" color={COLORS.text}>
          Contributing Factors
        </Typography>
        <Box display="flex" gap={1}>
          {chartData.slice(0, 3).map((factor) => (
            <Box
              key={factor.name}
              sx={{
                backgroundColor: color,
                color: "#ffffff",
                px: 1,
                py: 0.5,
                borderRadius: 1,
                fontSize: "0.75rem",
                fontWeight: "bold",
              }}
            >
              {factor.name}: {factor.originalValue?.toFixed(1)}%
            </Box>
          ))}
        </Box>
      </Box>

      {chartData.length > 0 ? (
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={COLORS.sidebar_border}
              />
              <XAxis
                type="category"
                dataKey="name"
                stroke={COLORS.text_secondary}
                fontSize={12}
                axisLine={true}
                tickLine={true}
              />
              <YAxis
                type="number"
                stroke={COLORS.text_secondary}
                fontSize={12}
                tickFormatter={(value) => `${value}%`}
                domain={[0, 100]}
                axisLine={true}
                tickLine={true}
              />
              <Tooltip content={<CustomTooltip />} />
              <Bar
                dataKey="value"
                fill={color}
                radius={[4, 4, 0, 0]}
                maxBarSize={50}
              />
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
            flexDirection: "column",
            gap: 1,
          }}
        >
          <Typography variant="body2" color={COLORS.text_secondary}>
            No factor data available
          </Typography>
          <Typography variant="caption" color={COLORS.text_secondary}>
            Debug: {JSON.stringify(factors)}
          </Typography>
          <Typography variant="caption" color={COLORS.text_secondary}>
            Chart data length: {chartData.length}
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
            Factor Breakdown:
          </Typography>
          <Box display="flex" flexDirection="column" gap={1}>
            {chartData.map((factor) => (
              <Box
                key={factor.name}
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                sx={{
                  px: 2,
                  py: 1,
                  backgroundColor: COLORS.card_bg,
                  borderRadius: 1,
                  border: `1px solid ${COLORS.border}`,
                }}
              >
                <Typography variant="body2" color={COLORS.text}>
                  {factor.name}
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <Box
                    sx={{
                      width: 60,
                      height: 8,
                      backgroundColor: COLORS.sidebar_border,
                      borderRadius: 4,
                      overflow: "hidden",
                    }}
                  >
                    <Box
                      sx={{
                        width: `${factor.value}%`,
                        height: "100%",
                        backgroundColor: color,
                        borderRadius: 4,
                      }}
                    />
                  </Box>
                  <Typography variant="body2" fontWeight="bold" color={color}>
                    {factor.originalValue?.toFixed(1)}%
                  </Typography>
                </Box>
              </Box>
            ))}
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default FactorsChart;
