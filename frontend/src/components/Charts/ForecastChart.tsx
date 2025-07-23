import React from "react";
import { Box, Typography, Paper, Chip } from "@mui/material";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { TrendingUp, TrendingDown, TrendingFlat } from "@mui/icons-material";
import { COLORS } from "../../utils/constants";
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
  const color = COLORS[disasterType];

  // Transform data for the chart
  const chartData = forecast.map((day, index) => ({
    ...day,
    probability: day.probability * 100,
    formattedDate: formatDate(day.date),
    dayNumber: index + 1,
  }));

  // Calculate trend
  const getTrend = () => {
    if (chartData.length < 2) return { direction: "flat", percentage: 0 };

    const first = chartData[0].probability;
    const last = chartData[chartData.length - 1].probability;
    const change = ((last - first) / first) * 100;

    if (change > 5) return { direction: "up", percentage: Math.abs(change) };
    if (change < -5) return { direction: "down", percentage: Math.abs(change) };
    return { direction: "flat", percentage: Math.abs(change) };
  };

  const trend = getTrend();

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <Box
          sx={{
            backgroundColor: COLORS.card_bg,
            backdropFilter: "blur(10px)",
            border: `1px solid ${COLORS.glass_border}`,
            borderRadius: 2,
            p: 2,
            boxShadow: COLORS.glass_shadow,
          }}
        >
          <Typography
            variant="body2"
            fontWeight="bold"
            color={COLORS.text}
            mb={1}
          >
            {label}
          </Typography>
          <Typography variant="body2" color={color} mb={1}>
            Risk: {formatPercentage(payload[0].value / 100)}
          </Typography>
          <Typography variant="caption" color={COLORS.text_secondary}>
            Day {data.dayNumber} of 30
          </Typography>
          {data.key_factors && data.key_factors.length > 0 && (
            <Box mt={1}>
              <Typography variant="caption" color={COLORS.text_secondary}>
                Key Factors: {data.key_factors.join(", ")}
              </Typography>
            </Box>
          )}
        </Box>
      );
    }
    return null;
  };

  return (
    <Paper
      elevation={0}
      sx={{
        background: COLORS.gradient_glass,
        backdropFilter: "blur(20px)",
        border: `2px solid ${color}`,
        borderRadius: 3,
        p: 4,
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
      {/* Header with Trend */}
      <Box
        display="flex"
        justifyContent="space-between"
        alignItems="center"
        mb={3}
      >
        <Box>
          <Typography variant="h6" fontWeight="bold" color={COLORS.text}>
            30-Day Risk Forecast
          </Typography>
          <Typography variant="body2" color={COLORS.text_secondary}>
            Predictive analysis based on weather patterns
          </Typography>
        </Box>

        {/* Trend Indicator */}
        <Box display="flex" alignItems="center" gap={1}>
          {trend.direction === "up" && (
            <TrendingUp sx={{ color: "#ef4444", fontSize: 20 }} />
          )}
          {trend.direction === "down" && (
            <TrendingDown sx={{ color: "#10b981", fontSize: 20 }} />
          )}
          {trend.direction === "flat" && (
            <TrendingFlat sx={{ color: "#f59e0b", fontSize: 20 }} />
          )}
          <Chip
            label={`${
              trend.direction === "up"
                ? "+"
                : trend.direction === "down"
                ? "-"
                : "±"
            }${trend.percentage.toFixed(1)}%`}
            size="small"
            sx={{
              backgroundColor:
                trend.direction === "up"
                  ? "rgba(239, 68, 68, 0.2)"
                  : trend.direction === "down"
                  ? "rgba(16, 185, 129, 0.2)"
                  : "rgba(245, 158, 11, 0.2)",
              color:
                trend.direction === "up"
                  ? "#ef4444"
                  : trend.direction === "down"
                  ? "#10b981"
                  : "#f59e0b",
              border: `1px solid ${
                trend.direction === "up"
                  ? "rgba(239, 68, 68, 0.3)"
                  : trend.direction === "down"
                  ? "rgba(16, 185, 129, 0.3)"
                  : "rgba(245, 158, 11, 0.3)"
              }`,
            }}
          />
        </Box>
      </Box>

      {/* Stats Summary */}
      <Box display="flex" gap={2} mb={3}>
        <Box
          sx={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${COLORS.glass_border}`,
          }}
        >
          <Typography variant="caption" color={COLORS.text_secondary}>
            Average Risk
          </Typography>
          <Typography variant="h6" fontWeight="bold" color={COLORS.text}>
            {formatPercentage(
              chartData.reduce((sum, day) => sum + day.probability, 0) /
                chartData.length /
                100
            )}
          </Typography>
        </Box>
        <Box
          sx={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${COLORS.glass_border}`,
          }}
        >
          <Typography variant="caption" color={COLORS.text_secondary}>
            Peak Risk
          </Typography>
          <Typography variant="h6" fontWeight="bold" color={color}>
            {formatPercentage(
              Math.max(...chartData.map((d) => d.probability)) / 100
            )}
          </Typography>
        </Box>
        <Box
          sx={{
            backgroundColor: "rgba(255, 255, 255, 0.05)",
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${COLORS.glass_border}`,
          }}
        >
          <Typography variant="caption" color={COLORS.text_secondary}>
            Days Analyzed
          </Typography>
          <Typography variant="h6" fontWeight="bold" color={COLORS.text}>
            {chartData.length}
          </Typography>
        </Box>
      </Box>

      {chartData.length > 0 ? (
        <Box sx={{ height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData}>
              <defs>
                <linearGradient
                  id={`gradient-${disasterType}`}
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop offset="5%" stopColor={color} stopOpacity={0.3} />
                  <stop offset="95%" stopColor={color} stopOpacity={0.05} />
                </linearGradient>
              </defs>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke={COLORS.glass_border}
                opacity={0.3}
              />
              <XAxis
                dataKey="formattedDate"
                stroke={COLORS.text_secondary}
                fontSize={12}
                tickLine={false}
                axisLine={false}
                tick={{ fill: COLORS.text_secondary }}
              />
              <YAxis
                stroke={COLORS.text_secondary}
                fontSize={12}
                tickFormatter={(value) => `${value}%`}
                tickLine={false}
                axisLine={false}
                tick={{ fill: COLORS.text_secondary }}
              />
              <RechartsTooltip content={<CustomTooltip />} />
              <Area
                type="monotone"
                dataKey="probability"
                stroke={color}
                strokeWidth={3}
                fill={`url(#gradient-${disasterType})`}
                dot={{
                  fill: color,
                  strokeWidth: 2,
                  r: 4,
                  stroke: COLORS.card_bg,
                }}
                activeDot={{
                  r: 6,
                  stroke: color,
                  strokeWidth: 3,
                  fill: COLORS.highlight,
                }}
              />
            </AreaChart>
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

      {/* Legend */}
      <Box mt={2} display="flex" justifyContent="center">
        <Box display="flex" alignItems="center" gap={1}>
          <Box
            sx={{
              width: 12,
              height: 12,
              borderRadius: "50%",
              background: `linear-gradient(45deg, ${color}40, ${color})`,
            }}
          />
          <Typography variant="caption" color={COLORS.text_secondary}>
            Risk probability over time
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};

export default ForecastChart;
