import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Chip,
  Tooltip,
} from "@mui/material";
import {
  Brightness4,
  Brightness7,
  Analytics,
  Timeline,
} from "@mui/icons-material";
import { COLORS } from "../../utils/constants";

interface NavbarProps {
  currentSection?: string;
  onThemeToggle?: () => void;
  isDarkMode?: boolean;
}

const Navbar: React.FC<NavbarProps> = ({
  currentSection = "Dashboard",
  onThemeToggle,
  isDarkMode = true,
}) => {
  return (
    <AppBar
      position="static"
      sx={{
        background: COLORS.gradient_primary,
        borderBottom: `2px solid ${COLORS.glass_border}`,
        boxShadow: COLORS.glass_shadow,
        backdropFilter: "blur(10px)",
      }}
    >
      <Toolbar sx={{ justifyContent: "space-between" }}>
        {/* Left Section - Logo & Breadcrumb */}
        <Box display="flex" alignItems="center" gap={3}>
          <Box display="flex" alignItems="center" gap={2}>
            <Box
              sx={{
                width: 40,
                height: 40,
                borderRadius: 2,
                background: "rgba(255, 255, 255, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                backdropFilter: "blur(10px)",
              }}
            >
              <Analytics sx={{ color: "#ffffff", fontSize: 24 }} />
            </Box>
            <Typography
              variant="h6"
              component="div"
              sx={{
                color: "#ffffff",
                fontWeight: "700",
                fontSize: "1.25rem",
                letterSpacing: "-0.025em",
              }}
            >
              DisasterPredict AI
            </Typography>
          </Box>

          {/* Breadcrumb */}
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="body2" color="rgba(255, 255, 255, 0.7)">
              Dashboard
            </Typography>
            <Typography variant="body2" color="rgba(255, 255, 255, 0.4)">
              /
            </Typography>
            <Typography
              variant="body2"
              color="rgba(255, 255, 255, 0.9)"
              fontWeight={500}
            >
              {currentSection}
            </Typography>
          </Box>
        </Box>

        {/* Right Section - Status & Theme */}
        <Box display="flex" alignItems="center" gap={2}>
          {/* AI Status Indicator */}
          <Chip
            icon={<Timeline />}
            label="Quantum AI Active"
            size="small"
            sx={{
              backgroundColor: "rgba(16, 185, 129, 0.2)",
              color: "#10b981",
              border: "1px solid rgba(16, 185, 129, 0.3)",
              "& .MuiChip-icon": {
                color: "#10b981",
              },
            }}
          />

          {/* Theme Toggle */}
          {onThemeToggle && (
            <Tooltip
              title={
                isDarkMode ? "Switch to Light Mode" : "Switch to Dark Mode"
              }
            >
              <IconButton
                onClick={onThemeToggle}
                sx={{ color: "rgba(255, 255, 255, 0.8)" }}
              >
                {isDarkMode ? <Brightness7 /> : <Brightness4 />}
              </IconButton>
            </Tooltip>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
