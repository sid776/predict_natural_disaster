import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import { COLORS } from "../../utils/constants";

const Navbar: React.FC = () => {
  return (
    <AppBar
      position="static"
      sx={{
        background: `linear-gradient(135deg, ${COLORS.primary} 0%, ${COLORS.secondary} 100%)`,
        borderBottom: `1px solid ${COLORS.sidebar_border}`,
        boxShadow:
          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
      }}
    >
      <Toolbar>
        <Box display="flex" alignItems="center" gap={2}>
          <Typography
            variant="h6"
            component="div"
            sx={{
              color: "#ffffff",
              fontWeight: "700",
              fontSize: "1.5rem",
              letterSpacing: "-0.025em",
            }}
          >
            🌪️ Natural Disaster Predictor
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
