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
import { ApiService } from "./services/api";

// Types and Utils
import type {
  DisasterType,
  PredictionModel,
  PredictionResponse,
} from "./types";
import { COLORS, DISASTER_TYPES } from "./utils/constants";
import { formatPercentage, getWeatherSummary } from "./utils/formatters";

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: COLORS.guide,
    },
    secondary: {
      main: COLORS.earthquake,
    },
    background: {
      default: COLORS.main_bg,
    },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
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

  // Prediction hook
  const {
    loading,
    error,
    data: predictions,
    predictAll,
    reset,
  } = useBatchPrediction();

  // Check API health on mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const isHealthy = await ApiService.healthCheck();
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
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setSelectedTab(newValue);
  };

  // Get current disaster type
  const disasterTypes: DisasterType[] = [
    "tornado",
    "earthquake",
    "wildfire",
    "flood",
  ];
  const currentDisasterType = disasterTypes[selectedTab];

  // Get current prediction data
  const currentPrediction = predictions?.[currentDisasterType];

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ backgroundColor: COLORS.main_bg, minHeight: "100vh" }}>
        <Navbar />

        {/* API Health Warning */}
        {apiHealth === false && (
          <Alert severity="warning" sx={{ m: 2 }}>
            Backend API is not available. Some features may not work properly.
          </Alert>
        )}

        <Container maxWidth={false} sx={{ mt: 2 }}>
          <Box display="flex" flexDirection={isMobile ? "column" : "row"}>
            {/* Sidebar */}
            <Sidebar
              location={location}
              selectedModel={selectedModel}
              onLocationChange={setLocation}
              onModelChange={setSelectedModel}
              onPredict={handlePredict}
              loading={loading}
              error={error}
              forecastData={predictions?.tornado?.forecast}
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
                      color: DISASTER_TYPES[currentDisasterType].color,
                    },
                    "& .MuiTabs-indicator": {
                      backgroundColor:
                        DISASTER_TYPES[currentDisasterType].color,
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
                    />
                  ))}
                </Tabs>
              </Box>

              {/* Tab Panels */}
              {disasterTypes.map((disasterType, index) => (
                <TabPanel key={disasterType} value={selectedTab} index={index}>
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
                      <Box display="flex" justifyContent="center" my={4}>
                        <CircularProgress size={60} />
                      </Box>
                    )}

                    {error && (
                      <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                      </Alert>
                    )}

                    {currentPrediction && !loading && (
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
                                {currentPrediction.metadata.location}
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
                                {formatPercentage(
                                  currentPrediction.probability
                                )}
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
                                {currentPrediction.metadata.model.toUpperCase()}
                              </Typography>
                            </Box>
                          </Box>

                          {/* Weather Summary */}
                          {currentPrediction.metadata.weather_data && (
                            <Box
                              mt={2}
                              pt={2}
                              borderTop={`1px solid ${COLORS.sidebar_border}`}
                            >
                              <Typography
                                variant="body2"
                                color="text.secondary"
                                mb={1}
                              >
                                Current Weather Conditions:
                              </Typography>
                              <Box display="flex" flexWrap="wrap" gap={2}>
                                {Object.entries(
                                  getWeatherSummary(
                                    currentPrediction.metadata.weather_data
                                  )
                                ).map(([key, value]) => (
                                  <Box key={key}>
                                    <Typography
                                      variant="caption"
                                      color="text.secondary"
                                    >
                                      {key.charAt(0).toUpperCase() +
                                        key.slice(1)}
                                    </Typography>
                                    <Typography
                                      variant="body2"
                                      fontWeight="bold"
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
                          gridTemplateColumns={
                            isMobile
                              ? "1fr"
                              : "repeat(auto-fit, minmax(400px, 1fr))"
                          }
                          gap={3}
                        >
                          <ProbabilityGauge
                            probability={currentPrediction.probability}
                            disasterType={disasterType}
                          />

                          <ForecastChart
                            forecast={currentPrediction.forecast}
                            disasterType={disasterType}
                          />

                          <FactorsChart
                            factors={currentPrediction.factors}
                            disasterType={disasterType}
                          />
                        </Box>
                      </Box>
                    )}

                    {!currentPrediction && !loading && !error && (
                      <Box
                        sx={{
                          textAlign: "center",
                          py: 8,
                          color: COLORS.text,
                        }}
                      >
                        <Typography variant="h6" mb={2}>
                          No prediction data available
                        </Typography>
                        <Typography variant="body2">
                          Enter a location and click predict to see{" "}
                          {DISASTER_TYPES[disasterType].label.toLowerCase()}{" "}
                          analysis.
                        </Typography>
                      </Box>
                    )}
                  </Box>
                </TabPanel>
              ))}
            </Box>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
