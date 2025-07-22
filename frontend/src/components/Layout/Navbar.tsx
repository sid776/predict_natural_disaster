import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import { COLORS } from "../../utils/constants";

const Navbar: React.FC = () => {
  return (
    <AppBar
      position="static"
      sx={{
        background: COLORS.gradient_primary,
        borderBottom: `2px solid ${COLORS.border}`,
        boxShadow:
          "0 8px 32px -8px rgba(0, 0, 0, 0.2), 0 4px 16px -4px rgba(0, 0, 0, 0.1)",
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
