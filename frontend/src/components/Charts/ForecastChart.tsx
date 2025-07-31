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
        transition: "all 0.3s ease",
        "&:hover": {
          transform: "translateY(-2px)",
          boxShadow: `0 12px 40px 0 rgba(31, 38, 135, 0.5), 0 0 20px ${color}40`,
        },
        "&::before": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: "4px",
          background: `linear-gradient(90deg, ${color} 0%, ${COLORS.forecast_trend} 100%)`,
        },
        "&::after": {
          content: '""',
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `linear-gradient(45deg, transparent 30%, ${COLORS.forecast_trend}08 50%, transparent 70%)`,
          animation: "shimmer 4s ease-in-out infinite",
          pointerEvents: "none",
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
            <TrendingUp
              sx={{
                color: COLORS.error,
                fontSize: 20,
                filter: `drop-shadow(0 0 8px ${COLORS.error})`,
                animation: "pulse 2s ease-in-out infinite",
              }}
            />
          )}
          {trend.direction === "down" && (
            <TrendingDown
              sx={{
                color: COLORS.success,
                fontSize: 20,
                filter: `drop-shadow(0 0 8px ${COLORS.success})`,
              }}
            />
          )}
          {trend.direction === "flat" && (
            <TrendingFlat
              sx={{
                color: COLORS.warning,
                fontSize: 20,
                filter: `drop-shadow(0 0 8px ${COLORS.warning})`,
              }}
            />
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
              background:
                trend.direction === "up"
                  ? COLORS.gradient_error
                  : trend.direction === "down"
                  ? COLORS.gradient_success
                  : COLORS.gradient_warning,
              color: COLORS.text,
              border: `1px solid ${
                trend.direction === "up"
                  ? COLORS.error
                  : trend.direction === "down"
                  ? COLORS.success
                  : COLORS.warning
              }`,
              fontWeight: 600,
              textShadow: `0 0 5px ${
                trend.direction === "up"
                  ? COLORS.error
                  : trend.direction === "down"
                  ? COLORS.success
                  : COLORS.warning
              }`,
              animation:
                trend.direction === "up"
                  ? "pulse 1.5s ease-in-out infinite"
                  : "none",
            }}
          />
        </Box>
      </Box>

      {/* Stats Summary */}
      <Box display="flex" gap={2} mb={3}>
        <Box
          sx={{
            background: COLORS.gradient_glass,
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${COLORS.glass_border}`,
            transition: "all 0.3s ease",
            "&:hover": {
              transform: "translateY(-2px)",
              boxShadow: `0 8px 25px 0 rgba(31, 38, 135, 0.3)`,
            },
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
            background: COLORS.gradient_glass,
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${color}`,
            transition: "all 0.3s ease",
            "&:hover": {
              transform: "translateY(-2px)",
              boxShadow: `0 8px 25px 0 rgba(31, 38, 135, 0.3), 0 0 15px ${color}40`,
            },
          }}
        >
          <Typography variant="caption" color={COLORS.text_secondary}>
            Peak Risk
          </Typography>
          <Typography
            variant="h6"
            fontWeight="bold"
            color={color}
            sx={{
              textShadow: `0 0 8px ${color}`,
              animation: "pulse 2s ease-in-out infinite",
            }}
          >
            {formatPercentage(
              Math.max(...chartData.map((d) => d.probability)) / 100
            )}
          </Typography>
        </Box>
        <Box
          sx={{
            background: COLORS.gradient_glass,
            borderRadius: 2,
            p: 2,
            flex: 1,
            border: `1px solid ${COLORS.glass_border}`,
            transition: "all 0.3s ease",
            "&:hover": {
              transform: "translateY(-2px)",
              boxShadow: `0 8px 25px 0 rgba(31, 38, 135, 0.3)`,
            },
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
                  <stop offset="5%" stopColor={color} stopOpacity={0.4} />
                  <stop
                    offset="50%"
                    stopColor={COLORS.forecast_trend}
                    stopOpacity={0.2}
                  />
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
                  filter: `drop-shadow(0 0 4px ${color})`,
                }}
                activeDot={{
                  r: 8,
                  stroke: color,
                  strokeWidth: 3,
                  fill: COLORS.highlight,
                  filter: `drop-shadow(0 0 8px ${color})`,
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
              boxShadow: `0 0 8px ${color}`,
            }}
          />
          <Typography variant="caption" color={COLORS.text_secondary}>
            Risk probability over time
          </Typography>
        </Box>
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

export default ForecastChart;
