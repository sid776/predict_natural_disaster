import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import { formatDate, formatPercentage } from "../../utils/formatters";
import type { DisasterType, ForecastDay } from "../../types";

interface ForecastChartProps {
  forecast: ForecastDay[];
  disasterType: DisasterType;
}

const ForecastChart: React.FC<ForecastChartProps> = ({
  forecast,
  disasterType,
}) => {
  const color = DISASTER_TYPES[disasterType].color;

  // Transform data for the chart
  const chartData = forecast.map((day) => ({
    ...day,
    probability: day.probability * 100, // Convert to percentage
    formattedDate: formatDate(day.date),
  }));

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <Box
          sx={{
            backgroundColor: COLORS.card_bg,
            border: `1px solid ${COLORS.sidebar_border}`,
            borderRadius: 1,
            p: 1,
          }}
        >
          <Typography variant="body2" color={COLORS.text}>
            {label}
          </Typography>
          <Typography variant="body2" color={color}>
            Probability: {formatPercentage(payload[0].value / 100)}
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
          30-Day Forecast Timeline
        </Typography>
        <Box display="flex" gap={2}>
          <Typography variant="body2" color={COLORS.text_secondary}>
            {chartData.length} days
          </Typography>
          <Typography variant="body2" color={COLORS.text_secondary}>
            Avg:{" "}
            {formatPercentage(
              chartData.reduce((sum, day) => sum + day.probability, 0) /
                chartData.length /
                100
            )}
          </Typography>
        </Box>
      </Box>

      {chartData.length > 0 ? (
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={COLORS.sidebar_border}
              />
              <XAxis
                dataKey="formattedDate"
                stroke={COLORS.text_secondary}
                fontSize={12}
              />
              <YAxis
                stroke={COLORS.text_secondary}
                fontSize={12}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="monotone"
                dataKey="probability"
                stroke={color}
                strokeWidth={4}
                dot={{
                  fill: color,
                  strokeWidth: 2,
                  r: 5,
                  stroke: COLORS.card_bg,
                }}
                activeDot={{
                  r: 8,
                  stroke: color,
                  strokeWidth: 3,
                  fill: COLORS.highlight,
                }}
                strokeDasharray="0"
              />
            </LineChart>
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
            No forecast data available
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ForecastChart;
