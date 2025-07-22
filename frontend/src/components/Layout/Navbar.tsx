import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import { COLORS } from "../../utils/constants";

const Navbar: React.FC = () => {
  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: COLORS.guide,
        borderBottom: `1px solid ${COLORS.sidebar_border}`,
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
      }}
    >
      <Toolbar>
        <Box display="flex" alignItems="center" gap={2}>
          <Typography
            variant="h6"
            component="div"
            sx={{
              color: "#ffffff",
              fontWeight: "bold",
              fontSize: "1.5rem",
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
