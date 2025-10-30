// src/components/stepper/GaGaStepper/steps/ComparisonStep.jsx
import React, { useState, useRef, useEffect } from "react";
import { Paper, Box, Button, LinearProgress, Typography } from "@mui/material";
import { ArrowBack } from "@mui/icons-material";
import GAtoGAComparisonViewer from "../../../results/ga_vs_ga_results/GAtoGAComparisonViewer";
import { useComparison } from "../../../../context/ComparisonContext";
import axios from "axios";

const ComparisonStep = ({ handleBack }) => {
  const { firstGaResult, secondGaResult, comparisonResult, setComparisonResult } = useComparison();
  const [activeTab, setActiveTab] = useState(0);
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const wsRef = useRef(null);

  const API_URL = import.meta.env.VITE_API_URL;

  const handleStartComparison = async () => {
    if (!firstGaResult || !secondGaResult) return;

    try {
      setComparisonResult(null);
      setComparisonLoading(true);

      // Prepare FormData with two GA JSONs
      const formData = new FormData();
      formData.append(
        "ga1_json",
        new Blob([JSON.stringify(firstGaResult?.result || firstGaResult)], { type: "application/json" }),
        "ga1.json"
      );
      formData.append(
        "ga2_json",
        new Blob([JSON.stringify(secondGaResult?.result || secondGaResult)], { type: "application/json" }),
        "ga2.json"
      );

      // Start backend comparison
      const res = await axios.post(`${API_URL}/api/comparison/ga-ga/start`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { job_id } = res.data;

      // Open WebSocket to get live updates
      wsRef.current = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/comparison/ga-ga/ws/${job_id}`);

      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("📨 WS Message Received:", data);

        // Check for completion
        if (data.status === "completed") {
          setComparisonResult(data.result || { message: "No comparison result" });
          setComparisonLoading(false);
        }

        // Check for error
        if (data.status === "error") {
          console.error("GA-to-GA Comparison Error:", data.error_msg);
          setComparisonResult({ error: data.error_msg });
          setComparisonLoading(false);
        }
      };

      wsRef.current.onclose = () => console.log("GA-to-GA WebSocket closed");
    } catch (err) {
      console.error("Failed to start GA-to-GA comparison:", err);
      setComparisonLoading(false);
    }
  };

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
        <Button variant="outlined" onClick={handleBack} startIcon={<ArrowBack />}>
          Back
        </Button>
        <Typography variant="h6" sx={{ fontWeight: "bold", ml: 2 }}>
          GA vs GA Comparison
        </Typography>
      </Box>

      {/* Show the start button first */}
      <Box sx={{ mt: 2 }}>
        <Button
          variant="contained"
          onClick={handleStartComparison}
          disabled={comparisonLoading || !firstGaResult || !secondGaResult}
          sx={{ mb: 2 }}
        >
          {comparisonLoading ? "Comparing..." : "Start Comparison"}
        </Button>

        {/* Only show results when they exist */}
        {!comparisonLoading && comparisonResult && (
          <GAtoGAComparisonViewer data={comparisonResult} />
        )}
      </Box>

      {/* Loading Indicator */}
      {comparisonLoading && (
        <Box sx={{ mt: 2 }}>
          <LinearProgress />
          <Typography variant="body2" sx={{ mt: 1 }}>
            Comparing documents...
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ComparisonStep;
