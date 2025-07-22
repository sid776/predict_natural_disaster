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
import type { DisasterType, FactorImpacts } from "../../types";
import { COLORS, DISASTER_TYPES } from "../../utils/constants";
import { formatFactorImpacts } from "../../utils/formatters";

interface FactorsChartProps {
  factors: FactorImpacts;
  disasterType: DisasterType;
  title?: string;
}

const FactorsChart: React.FC<FactorsChartProps> = ({
  factors,
  disasterType,
  title,
}) => {
  const disasterColor = DISASTER_TYPES[disasterType].color;
  const formattedFactors = formatFactorImpacts(factors);

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
            Impact: {payload[0].value.toFixed(1)}%
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
        {title || "Factor Impact Analysis"}
      </Typography>

      <Box sx={{ height: 300, width: "100%" }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={formattedFactors}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke={COLORS.sidebar_border}
            />
            <XAxis
              dataKey="name"
              stroke={COLORS.text}
              fontSize={12}
              tick={{ fill: COLORS.text }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis
              stroke={COLORS.text}
              fontSize={12}
              tick={{ fill: COLORS.text }}
              domain={[0, 100]}
              tickFormatter={(value) => `${value}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" fill={disasterColor} radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </Box>

      {/* Key factors summary */}
      {formattedFactors.length > 0 && (
        <Box mt={2}>
          <Typography variant="body2" color="text.secondary" mb={1}>
            Key Factors (by impact):
          </Typography>
          <Box
            sx={{
              display: "flex",
              flexWrap: "wrap",
              gap: 1,
            }}
          >
            {formattedFactors.slice(0, 3).map((factor, index) => (
              <Box
                key={factor.name}
                sx={{
                  backgroundColor: disasterColor,
                  color: COLORS.white,
                  px: 2,
                  py: 0.5,
                  borderRadius: 2,
                  fontSize: "0.75rem",
                  fontWeight: "bold",
                  opacity: 1 - index * 0.2,
                }}
              >
                {factor.name}: {factor.formatted}
              </Box>
            ))}
          </Box>
        </Box>
      )}

      {/* Total impact */}
      {formattedFactors.length > 0 && (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            mt: 2,
            pt: 2,
            borderTop: `1px solid ${COLORS.sidebar_border}`,
          }}
        >
          <Typography variant="body2" color="text.secondary">
            Total Impact:{" "}
            <Typography
              component="span"
              variant="body2"
              fontWeight="bold"
              color={disasterColor}
            >
              {formattedFactors
                .reduce((sum, factor) => sum + factor.value, 0)
                .toFixed(1)}
              %
            </Typography>
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default FactorsChart;
