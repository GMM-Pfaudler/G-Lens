import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import MainLayout from "../../../layouts/MainLayout";
import ComparisonViewer from "../../../components/results/ComparisonViewer";
import {
  Box,
  CircularProgress,
  Typography,
  Alert,
  Stack,
  Button
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8006";

const GaGaResultPage = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const fetchResult = useCallback(async () => {
    try {
      if (!id) {
        setError("Invalid result ID");
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10s timeout

      const res = await fetch(`${API_BASE}/api/comparison/ga-ga/result/${id}`, {
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Failed to load: ${res.status} ${errorText || "Unknown error"}`);
      }

      const json = await res.json();
      setData(json);
      setRetryCount(0);
    } catch (err) {
      console.error("❌ Error fetching GA–GA result:", err);
      const message =
        err.name === "AbortError"
          ? "Request timed out"
          : err.message || "Failed to load comparison result";
      setError(message);
      setRetryCount((prev) => prev + 1);
    } finally {
      setLoading(false);
    }
  }, [id]);

  const handleRetry = () => {
    if (retryCount < 3) {
      fetchResult();
    } else {
      setError("Maximum retries reached. Please refresh the page.");
    }
  };

  useEffect(() => {
    fetchResult();
  }, [fetchResult]);

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "GA vs GA", href: "/ga-ga-comparison" },
        { label: `Result #${id}`, active: true },
      ]}
    >
      <Box p={3}>
        {loading ? (
          <Stack alignItems="center" justifyContent="center" minHeight="50vh" spacing={2}>
            <CircularProgress />
            <Typography>Loading GA–GA result...</Typography>
          </Stack>
        ) : error ? (
          <Stack alignItems="center" justifyContent="center" minHeight="50vh" spacing={2}>
            <Alert severity="error">
              {error}
              {retryCount > 0 && ` (Attempt ${retryCount}/3)`}
            </Alert>
            <Button
              startIcon={<RefreshIcon />}
              variant="outlined"
              onClick={handleRetry}
              disabled={retryCount >= 3}
            >
              {retryCount < 3 ? "Retry" : "Max Retries Reached"}
            </Button>
          </Stack>
        ) : data ? (
          <ComparisonViewer data={data?.result || data} />
        ) : (
          <Typography color="text.secondary">No data available</Typography>
        )}
      </Box>
    </MainLayout>
  );
};

export default GaGaResultPage;
