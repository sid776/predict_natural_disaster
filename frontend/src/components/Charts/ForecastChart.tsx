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
        backgroundColor: COLORS.card_bg,
        border: `1px solid ${color}`,
        borderRadius: "12px",
        p: 3,
        boxShadow:
          "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
      }}
    >
      <Typography variant="h6" fontWeight="bold" mb={2} color={COLORS.text}>
        Forecast Timeline
      </Typography>

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
                strokeWidth={3}
                dot={{ fill: color, strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, stroke: color, strokeWidth: 2 }}
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
