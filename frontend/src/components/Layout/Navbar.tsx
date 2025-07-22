import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  Chip,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { Science, Warning } from "@mui/icons-material";
import { COLORS } from "../../utils/constants";

interface NavbarProps {
  title?: string;
}

const Navbar: React.FC<NavbarProps> = ({
  title = "Quantum-Inspired Natural Disaster Prediction",
}) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <AppBar
      position="static"
      elevation={2}
      sx={{
        background: COLORS.white,
        color: COLORS.text,
        borderBottom: `2px solid ${COLORS.sidebar_border}`,
      }}
    >
      <Toolbar>
        <Box display="flex" alignItems="center" gap={2} flexGrow={1}>
          <Science
            sx={{
              color: COLORS.guide,
              fontSize: isMobile ? 28 : 32,
            }}
          />
          <Box>
            <Typography
              variant={isMobile ? "h6" : "h5"}
              component="h1"
              sx={{
                color: COLORS.flood,
                fontWeight: "bold",
                lineHeight: 1.2,
              }}
            >
              {isMobile ? "Quantum Disaster Prediction" : title}
            </Typography>
            <Box display="flex" gap={1} mt={0.5}>
              <Chip
                icon={<Science />}
                label="Quantum AI"
                size="small"
                sx={{
                  backgroundColor: COLORS.guide,
                  color: COLORS.white,
                  fontSize: "0.7rem",
                }}
              />
              <Chip
                icon={<Warning />}
                label="Real-time"
                size="small"
                sx={{
                  backgroundColor: COLORS.warning,
                  color: COLORS.white,
                  fontSize: "0.7rem",
                }}
              />
            </Box>
          </Box>
        </Box>

        {!isMobile && (
          <Box display="flex" alignItems="center" gap={1}>
            <Typography variant="caption" color="text.secondary">
              Powered by
            </Typography>
            <Chip
              label="Qiskit + PennyLane"
              size="small"
              sx={{
                backgroundColor: COLORS.earthquake,
                color: COLORS.white,
                fontSize: "0.7rem",
              }}
            />
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
