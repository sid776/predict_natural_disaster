import React, { useState, useEffect } from "react";
import {
  Box,
  Container,
  Tabs,
  Tab,
  Typography,
  Alert,
  CircularProgress,
  useTheme,
  useMediaQuery,
} from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

// Components
import Navbar from "./components/Layout/Navbar";
import Sidebar from "./components/Layout/Sidebar";
import ProbabilityGauge from "./components/Charts/ProbabilityGauge";
import ForecastChart from "./components/Charts/ForecastChart";
import FactorsChart from "./components/Charts/FactorsChart";

// Hooks and Services
import { useBatchPrediction } from "./hooks/usePrediction";
import { apiService } from "./services/api";

// Types and Utils
import type { DisasterType, PredictionModel } from "./types";
import { COLORS, DISASTER_TYPES } from "./utils/constants";
import { formatPercentage, getWeatherSummary } from "./utils/formatters";

// Create dynamic enterprise theme
const createAppTheme = (isDark: boolean) =>
  createTheme({
    palette: {
      mode: isDark ? "dark" : "light",
      primary: {
        main: COLORS.primary,
      },
      secondary: {
        main: COLORS.secondary,
      },
      background: {
        default: isDark ? COLORS.main_bg : "#f8fafc",
        paper: isDark ? COLORS.card_bg : "#ffffff",
      },
      text: {
        primary: isDark ? COLORS.text : "#1e293b",
        secondary: isDark ? COLORS.text_secondary : "#64748b",
      },
    },
    typography: {
      fontFamily:
        '"Inter", "IBM Plex Sans", "Roboto", "Helvetica", "Arial", sans-serif',
      h1: {
        fontWeight: 700,
        letterSpacing: "-0.025em",
      },
      h2: {
        fontWeight: 600,
        letterSpacing: "-0.025em",
      },
      h3: {
        fontWeight: 600,
        letterSpacing: "-0.025em",
      },
      h4: {
        fontWeight: 600,
        letterSpacing: "-0.025em",
      },
      h5: {
        fontWeight: 600,
        letterSpacing: "-0.025em",
      },
      h6: {
        fontWeight: 600,
        letterSpacing: "-0.025em",
      },
      body1: {
        lineHeight: 1.6,
      },
      body2: {
        lineHeight: 1.6,
      },
    },
    shape: {
      borderRadius: 12,
    },
    components: {
      MuiPaper: {
        styleOverrides: {
          root: {
            backgroundImage: "none",
            backgroundColor: isDark ? COLORS.card_bg : "#ffffff",
            backdropFilter: isDark ? "blur(10px)" : "none",
            border: isDark
              ? `1px solid ${COLORS.glass_border}`
              : `1px solid #e2e8f0`,
            boxShadow: isDark
              ? COLORS.glass_shadow
              : "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
          },
        },
      },
      MuiButton: {
        styleOverrides: {
          root: {
            borderRadius: 25,
            textTransform: "none",
            fontWeight: 600,
            letterSpacing: "0.025em",
          },
        },
      },
    },
  });

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`disaster-tabpanel-${index}`}
      aria-labelledby={`disaster-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));

  // State
  const [location, setLocation] = useState("");
  const [selectedModel, setSelectedModel] =
    useState<PredictionModel>("quantum");
  const [selectedTab, setSelectedTab] = useState(0);
  const [apiHealth, setApiHealth] = useState<boolean | null>(null);
  const [isDarkMode, setIsDarkMode] = useState(true);

  // Prediction hook
  const {
    loading,
    error,
    data: predictions,
    predictAll,
  } = useBatchPrediction();

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const isHealthy = await apiService.healthCheck();
        setApiHealth(isHealthy);
      } catch (err) {
        setApiHealth(false);
      }
    };
    checkHealth();
  }, []);

  // Handle prediction
  const handlePredict = async () => {
    if (!location.trim()) return;

    try {
      await predictAll(location, selectedModel);
    } catch (err) {
      console.error("Prediction failed:", err);
    }
  };

  // Handle tab change
  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  // Theme toggle handler
  const handleThemeToggle = () => {
    setIsDarkMode(!isDarkMode);
  };

  // Get current disaster type
  const disasterTypes: DisasterType[] = [
    "tornado",
    "earthquake",
    "wildfire",
    "flood",
  ];

  return (
    <ThemeProvider theme={createAppTheme(isDarkMode)}>
      <CssBaseline />
      <Box
        sx={{
          minHeight: "100vh",
          background: COLORS.main_bg,
          position: "relative",
          overflow: "hidden",
          "&::before": {
            content: '""',
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `
              radial-gradient(circle at 20% 80%, rgba(26, 35, 126, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 20%, rgba(124, 58, 237, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 40% 40%, rgba(99, 102, 241, 0.05) 0%, transparent 50%)
            `,
            animation: "float 20s ease-in-out infinite",
            zIndex: 0,
          },
        }}
      >
        <style>
          {`
            @keyframes float {
              0%, 100% { transform: translateY(0px) rotate(0deg); }
              33% { transform: translateY(-20px) rotate(1deg); }
              66% { transform: translateY(10px) rotate(-1deg); }
            }
          `}
        </style>
        <Navbar
          currentSection={DISASTER_TYPES[disasterTypes[selectedTab]].label}
          onThemeToggle={handleThemeToggle}
          isDarkMode={isDarkMode}
        />

        {/* API Health Warning */}
        {apiHealth === false && (
          <Alert severity="warning" sx={{ m: 2 }}>
            Backend API is not available. Some features may not work properly.
          </Alert>
        )}

        <Container
          maxWidth="xl"
          sx={{
            position: "relative",
            zIndex: 1,
            py: { xs: 2, md: 4 },
            px: { xs: 2, md: 4 },
          }}
        >
          <Box
            display="grid"
            gridTemplateColumns={{
              xs: "1fr",
              md: "350px 1fr",
            }}
            gap={{ xs: 3, md: 4 }}
            alignItems="start"
          >
            {/* Sidebar */}
            <Sidebar
              location={location}
              selectedModel={selectedModel}
              onLocationChange={setLocation}
              onModelChange={setSelectedModel}
              onPredict={handlePredict}
              loading={loading}
              error={error}
            />

            {/* Main Content */}
            <Box flex={1} sx={{ ml: isMobile ? 0 : 2 }}>
              {/* Disaster Type Tabs */}
              <Box sx={{ borderBottom: 1, borderColor: COLORS.sidebar_border }}>
                <Tabs
                  value={selectedTab}
                  onChange={handleTabChange}
                  variant={isMobile ? "scrollable" : "fullWidth"}
                  scrollButtons={isMobile ? "auto" : false}
                  sx={{
                    "& .MuiTab-root": {
                      color: COLORS.text,
                      fontWeight: "bold",
                      textTransform: "none",
                      minHeight: 64,
                    },
                    "& .Mui-selected": {
                      color: DISASTER_TYPES[disasterTypes[selectedTab]].color,
                    },
                    "& .MuiTabs-indicator": {
                      backgroundColor:
                        DISASTER_TYPES[disasterTypes[selectedTab]].color,
                      height: 3,
                    },
                  }}
                >
                  {disasterTypes.map((disasterType, index) => (
                    <Tab
                      key={disasterType}
                      label={
                        <Box display="flex" alignItems="center" gap={1}>
                          <span>{DISASTER_TYPES[disasterType].icon}</span>
                          <Typography variant="body1">
                            {DISASTER_TYPES[disasterType].label}
                          </Typography>
                        </Box>
                      }
                      id={`disaster-tab-${index}`}
                      aria-controls={`disaster-tabpanel-${index}`}
                      sx={{
                        "&.Mui-selected": {
                          color: DISASTER_TYPES[disasterType].color,
                        },
                      }}
                    />
                  ))}
                </Tabs>
              </Box>

              {/* Tab Panels */}
              {disasterTypes.map((disasterType, index) => {
                const prediction = predictions?.[disasterType];

                return (
                  <TabPanel
                    key={disasterType}
                    value={selectedTab}
                    index={index}
                  >
                    <Box>
                      <Typography
                        variant="h4"
                        component="h2"
                        sx={{
                          color: DISASTER_TYPES[disasterType].color,
                          fontWeight: "bold",
                          mb: 3,
                          textAlign: "center",
                        }}
                      >
                        {DISASTER_TYPES[disasterType].label} Analysis
                      </Typography>

                      {loading && (
                        <Box
                          display="flex"
                          flexDirection="column"
                          alignItems="center"
                          my={4}
                          gap={3}
                        >
                          <CircularProgress
                            size={60}
                            sx={{
                              color: COLORS.primary,
                              "& .MuiCircularProgress-circle": {
                                strokeLinecap: "round",
                              },
                            }}
                          />
                          <Box textAlign="center">
                            <Typography variant="h6" color={COLORS.text} mb={1}>
                              Analyzing{" "}
                              {DISASTER_TYPES[disasterType].label.toLowerCase()}{" "}
                              risk...
                            </Typography>
                            <Typography
                              variant="body2"
                              color={COLORS.text_secondary}
                            >
                              Processing weather data and running AI models
                            </Typography>
                          </Box>
                          <Box
                            sx={{
                              width: "100%",
                              maxWidth: 400,
                              height: 4,
                              backgroundColor: "rgba(255, 255, 255, 0.1)",
                              borderRadius: 2,
                              overflow: "hidden",
                              position: "relative",
                              "&::after": {
                                content: '""',
                                position: "absolute",
                                top: 0,
                                left: "-100%",
                                width: "100%",
                                height: "100%",
                                background: `linear-gradient(90deg, transparent, ${COLORS.primary}40, transparent)`,
                                animation: "shimmer 2s infinite",
                              },
                            }}
                          />
                          <style>
                            {`
                              @keyframes shimmer {
                                0% { left: -100%; }
                                100% { left: 100%; }
                              }
                            `}
                          </style>
                        </Box>
                      )}

                      {error && (
                        <Alert severity="error" sx={{ mb: 3 }}>
                          {error}
                        </Alert>
                      )}

                      {prediction && !loading && (
                        <Box>
                          {/* Results Summary */}
                          <Box
                            sx={{
                              backgroundColor: COLORS.card_bg,
                              border: `2px solid ${DISASTER_TYPES[disasterType].color}`,
                              borderRadius: 3,
                              p: 3,
                              mb: 3,
                            }}
                          >
                            <Typography variant="h6" fontWeight="bold" mb={2}>
                              Prediction Results
                            </Typography>

                            <Box display="flex" flexWrap="wrap" gap={2}>
                              <Box>
                                <Typography
                                  variant="body2"
                                  color="text.secondary"
                                >
                                  Location
                                </Typography>
                                <Typography variant="body1" fontWeight="bold">
                                  {prediction?.metadata?.location}
                                </Typography>
                              </Box>

                              <Box>
                                <Typography
                                  variant="body2"
                                  color="text.secondary"
                                >
                                  Probability
                                </Typography>
                                <Typography
                                  variant="body1"
                                  fontWeight="bold"
                                  color={DISASTER_TYPES[disasterType].color}
                                >
                                  {formatPercentage(prediction.probability)}
                                </Typography>
                              </Box>

                              <Box>
                                <Typography
                                  variant="body2"
                                  color="text.secondary"
                                >
                                  Model Used
                                </Typography>
                                <Typography variant="body1" fontWeight="bold">
                                  {prediction?.metadata?.model?.toUpperCase()}
                                </Typography>
                              </Box>
                            </Box>

                            {/* Weather Summary with Badges */}
                            {prediction?.metadata?.weather_data && (
                              <Box
                                sx={{
                                  backgroundColor: "rgba(255, 255, 255, 0.05)",
                                  borderRadius: 2,
                                  p: 3,
                                  mt: 2,
                                  border: `1px solid ${COLORS.glass_border}`,
                                }}
                              >
                                <Box
                                  display="flex"
                                  justifyContent="space-between"
                                  alignItems="center"
                                  mb={2}
                                >
                                  <Typography
                                    variant="body2"
                                    fontWeight="600"
                                    color={COLORS.text}
                                  >
                                    Current Weather Conditions
                                  </Typography>
                                  <Typography
                                    variant="caption"
                                    color={COLORS.text_secondary}
                                    sx={{ fontStyle: "italic" }}
                                  >
                                    Last updated:{" "}
                                    {new Date().toLocaleTimeString()}
                                  </Typography>
                                </Box>
                                <Box display="flex" flexWrap="wrap" gap={1.5}>
                                  {Object.entries(
                                    getWeatherSummary(
                                      prediction?.metadata?.weather_data
                                    )
                                  ).map(([key, value]) => (
                                    <Box
                                      key={key}
                                      sx={{
                                        backgroundColor:
                                          "rgba(255, 255, 255, 0.1)",
                                        borderRadius: 2,
                                        px: 2,
                                        py: 1,
                                        border: `1px solid ${COLORS.glass_border}`,
                                        backdropFilter: "blur(10px)",
                                      }}
                                    >
                                      <Typography
                                        variant="caption"
                                        color={COLORS.text_secondary}
                                        sx={{ display: "block", mb: 0.5 }}
                                      >
                                        {key.charAt(0).toUpperCase() +
                                          key.slice(1).replace("_", " ")}
                                      </Typography>
                                      <Typography
                                        variant="body2"
                                        fontWeight="bold"
                                        color={COLORS.text}
                                      >
                                        {value}
                                      </Typography>
                                    </Box>
                                  ))}
                                </Box>
                              </Box>
                            )}
                          </Box>

                          {/* Charts Grid */}
                          <Box
                            display="grid"
                            gridTemplateColumns={{
                              xs: "1fr",
                              sm: "repeat(auto-fit, minmax(300px, 1fr))",
                              md: "repeat(auto-fit, minmax(400px, 1fr))",
                            }}
                            gap={{ xs: 2, md: 3 }}
                          >
                            <ProbabilityGauge
                              probability={prediction.probability}
                              disasterType={disasterType}
                            />

                            <ForecastChart
                              forecast={prediction?.forecast || []}
                              disasterType={disasterType}
                            />

                            <FactorsChart
                              factors={prediction?.factors || {}}
                              disasterType={disasterType}
                            />
                          </Box>
                        </Box>
                      )}

                      {!prediction && !loading && !error && (
                        <Box
                          sx={{
                            backgroundColor: COLORS.card_bg,
                            border: `2px solid ${DISASTER_TYPES[disasterType].color}`,
                            borderRadius: 3,
                            p: 4,
                            textAlign: "center",
                          }}
                        >
                          {/* Welcome Icon */}
                          <Box
                            sx={{
                              fontSize: "4rem",
                              mb: 2,
                              opacity: 0.7,
                            }}
                          >
                            {DISASTER_TYPES[disasterType].icon}
                          </Box>

                          {/* Welcome Title */}
                          <Typography
                            variant="h5"
                            fontWeight="bold"
                            color={DISASTER_TYPES[disasterType].color}
                            mb={2}
                          >
                            Welcome to {DISASTER_TYPES[disasterType].label}{" "}
                            Analysis
                          </Typography>

                          {/* Description */}
                          <Typography
                            variant="body1"
                            color="text.secondary"
                            mb={3}
                            sx={{ maxWidth: 600, mx: "auto" }}
                          >
                            {DISASTER_TYPES[disasterType].description}
                          </Typography>

                          {/* Quick Start Guide */}
                          <Box
                            sx={{
                              backgroundColor: COLORS.main_bg,
                              borderRadius: 2,
                              p: 3,
                              mb: 3,
                              textAlign: "left",
                            }}
                          >
                            <Typography variant="h6" fontWeight="bold" mb={2}>
                              🚀 Quick Start Guide
                            </Typography>
                            <Box component="ol" sx={{ pl: 2, m: 0 }}>
                              <Typography component="li" variant="body2" mb={1}>
                                Enter a city name (e.g., "New York, NY" or
                                "London, UK")
                              </Typography>
                              <Typography component="li" variant="body2" mb={1}>
                                Select your preferred AI model from the sidebar
                              </Typography>
                              <Typography component="li" variant="body2" mb={1}>
                                Click "Predict" to analyze{" "}
                                {DISASTER_TYPES[
                                  disasterType
                                ].label.toLowerCase()}{" "}
                                risk
                              </Typography>
                              <Typography component="li" variant="body2">
                                View detailed forecasts, probability gauges, and
                                contributing factors
                              </Typography>
                            </Box>
                          </Box>

                          {/* Example Locations */}
                          <Box
                            sx={{
                              backgroundColor: COLORS.main_bg,
                              borderRadius: 2,
                              p: 3,
                              mb: 3,
                            }}
                          >
                            <Typography variant="h6" fontWeight="bold" mb={2}>
                              🌍 Try These Locations
                            </Typography>
                            <Box
                              display="flex"
                              flexWrap="wrap"
                              gap={1}
                              justifyContent="center"
                            >
                              {[
                                "Miami, FL",
                                "Los Angeles, CA",
                                "Tokyo, Japan",
                                "Sydney, Australia",
                                "London, UK",
                              ].map((loc) => (
                                <Box
                                  key={loc}
                                  sx={{
                                    backgroundColor: COLORS.card_bg,
                                    border: `1px solid ${COLORS.border}`,
                                    borderRadius: 1,
                                    px: 2,
                                    py: 1,
                                    cursor: "pointer",
                                    "&:hover": {
                                      backgroundColor: COLORS.primary,
                                      color: "#ffffff",
                                    },
                                  }}
                                  onClick={() => setLocation(loc)}
                                >
                                  <Typography variant="body2" fontWeight="500">
                                    {loc}
                                  </Typography>
                                </Box>
                              ))}
                            </Box>
                          </Box>

                          {/* What You'll Get */}
                          <Box
                            sx={{
                              backgroundColor: COLORS.main_bg,
                              borderRadius: 2,
                              p: 3,
                            }}
                          >
                            <Typography variant="h6" fontWeight="bold" mb={2}>
                              📊 What You'll Get
                            </Typography>
                            <Box
                              display="grid"
                              gridTemplateColumns="repeat(auto-fit, minmax(200px, 1fr))"
                              gap={2}
                            >
                              <Box textAlign="center">
                                <Typography
                                  variant="h4"
                                  color={DISASTER_TYPES[disasterType].color}
                                  mb={1}
                                >
                                  🎯
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  Risk Probability
                                </Typography>
                                <Typography
                                  variant="caption"
                                  color="text.secondary"
                                >
                                  Current risk assessment
                                </Typography>
                              </Box>
                              <Box textAlign="center">
                                <Typography
                                  variant="h4"
                                  color={DISASTER_TYPES[disasterType].color}
                                  mb={1}
                                >
                                  📈
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  30-Day Forecast
                                </Typography>
                                <Typography
                                  variant="caption"
                                  color="text.secondary"
                                >
                                  Future risk trends
                                </Typography>
                              </Box>
                              <Box textAlign="center">
                                <Typography
                                  variant="h4"
                                  color={DISASTER_TYPES[disasterType].color}
                                  mb={1}
                                >
                                  🔍
                                </Typography>
                                <Typography variant="body2" fontWeight="bold">
                                  Key Factors
                                </Typography>
                                <Typography
                                  variant="caption"
                                  color="text.secondary"
                                >
                                  Weather influences
                                </Typography>
                              </Box>
                            </Box>
                          </Box>

                          {/* Call to Action */}
                          <Box mt={3}>
                            <Typography
                              variant="body2"
                              color="text.secondary"
                              sx={{ fontStyle: "italic" }}
                            >
                              Ready to get started? Enter a location above and
                              click "Predict"!
                            </Typography>
                          </Box>
                        </Box>
                      )}
                    </Box>
                  </TabPanel>
                );
              })}
            </Box>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
