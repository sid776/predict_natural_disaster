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
  Area,
  AreaChart,
} from "recharts";
import type { DisasterType, ForecastDay } from "../../types";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import { formatChartDate, getTrendDirection } from "../../utils/formatters";

interface ForecastChartProps {
  forecast: ForecastDay[];
  disasterType: DisasterType;
  title?: string;
}

const ForecastChart: React.FC<ForecastChartProps> = ({
  forecast,
  disasterType,
  title,
}) => {
  const disasterColor = DISASTER_TYPES[disasterType].color;
  const trendDirection = getTrendDirection(forecast);

  // Transform data for the chart
  const chartData = forecast.map((day) => ({
    date: formatChartDate(day.date),
    probability: day.probability * 100, // Convert to percentage
    fullDate: day.date,
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <Box
          sx={{
            backgroundColor: COLORS.white,
            border: `1px solid ${disasterColor}`,
            borderRadius: 2,
            p: 2,
            boxShadow: 3,
          }}
        >
          <Typography variant="body2" fontWeight="bold">
            {label}
          </Typography>
          <Typography variant="body2" color={disasterColor}>
            Probability: {payload[0].value.toFixed(1)}%
          </Typography>
        </Box>
      );
    }
    return null;
  };

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
        {title || "30-Day Probability Forecast"}
      </Typography>

      <Box sx={{ height: 300, width: "100%" }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={COLORS.sidebar_border}
            />
            <XAxis
              dataKey="date"
              stroke={COLORS.text}
              fontSize={12}
              tick={{ fill: COLORS.text }}
            />
            <YAxis
              stroke={COLORS.text}
              fontSize={12}
              tick={{ fill: COLORS.text }}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="probability"
              stroke={disasterColor}
              strokeWidth={3}
              fill={disasterColor}
              fillOpacity={0.3}
            />
          </AreaChart>
        </ResponsiveContainer>
      </Box>

      {/* Trend indicator */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: 1,
          mt: 2,
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Trend:
        </Typography>
        <Typography
          variant="body2"
          sx={{
            color:
              trendDirection === "increasing"
                ? COLORS.danger
                : trendDirection === "decreasing"
                ? COLORS.success
                : COLORS.warning,
            fontWeight: "bold",
            textTransform: "capitalize",
          }}
        >
          {trendDirection}
        </Typography>
      </Box>

      {/* Summary stats */}
      {forecast.length > 0 && (
        <Box
          sx={{
            display: "flex",
            justifyContent: "space-around",
            mt: 2,
            pt: 2,
            borderTop: `1px solid ${COLORS.sidebar_border}`,
          }}
        >
          <Box textAlign="center">
            <Typography variant="caption" color="text.secondary">
              Average
            </Typography>
            <Typography variant="body2" fontWeight="bold" color={disasterColor}>
              {(
                (forecast.reduce((sum, day) => sum + day.probability, 0) /
                  forecast.length) *
                100
              ).toFixed(1)}
              %
            </Typography>
          </Box>
          <Box textAlign="center">
            <Typography variant="caption" color="text.secondary">
              Max
            </Typography>
            <Typography variant="body2" fontWeight="bold" color={disasterColor}>
              {(
                Math.max(...forecast.map((day) => day.probability)) * 100
              ).toFixed(1)}
              %
            </Typography>
          </Box>
          <Box textAlign="center">
            <Typography variant="caption" color="text.secondary">
              Min
            </Typography>
            <Typography variant="body2" fontWeight="bold" color={disasterColor}>
              {(
                Math.min(...forecast.map((day) => day.probability)) * 100
              ).toFixed(1)}
              %
            </Typography>
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default ForecastChart;
