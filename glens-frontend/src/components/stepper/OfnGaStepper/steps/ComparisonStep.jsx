import React, { useEffect, useRef, useState } from "react";
import { Paper, Box, Button, LinearProgress, Typography } from "@mui/material";
import { ArrowBack } from "@mui/icons-material";
import OfnResultViewer from "../../../results/OfnResultViewer";
import GaResultViewer from "../../../results/GaResultViewer";
import ComparisonViewer from "../../../results/ComparisonViewer";
import ResultTabs from "../../../tabs/ResultsTabs";
import axios from "axios";
import { useComparison } from "../../../../context/ComparisonContext";

const ComparisonStep = ({ handleBack }) => {
  const API_URL = import.meta.env.VITE_API_URL;
  const wsRef = useRef(null);
  const [progress, setProgress] = useState(0);
  const [wsMessage, setWsMessage] = useState("");

  const {
    ofnResult,
    gaResult,
    comparisonResult,
    setComparisonResult,
    comparisonLoading,
    setComparisonLoading,
    comparisonTab,
    setComparisonTab
  } = useComparison();

  const handleStartComparison = async () => {
    try {
      setComparisonResult(null);
      setComparisonLoading(true);
      setProgress(0);

      const formData = new FormData();
      formData.append(
        "ga_json",
        new Blob([JSON.stringify(gaResult?.result || gaResult)], { type: "application/json" }),
        "ga.json"
      );
      formData.append(
        "ofn_json",
        new Blob([JSON.stringify(ofnResult?.result || ofnResult)], { type: "application/json" }),
        "ofn.json"
      );

      const res = await axios.post(`${API_URL}/api/comparison/ofn-ga/start`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const { job_id } = res.data;

      wsRef.current = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/comparison/ofn-ga/ws/${job_id}`);
      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          // 🔹 Update progress if available
          if (data.progress != null) setProgress(data.progress);

          // 🔹 Update current message if available
          if (data.message) setWsMessage(data.message);

          // 🔹 Handle completion
          if (data.status === "completed" && data.result) {
            const parsedResult = {
              ...data.result,
              comparison_report: data.result.comparison_report.map(item => ({
                ...item,
                answer: typeof item.answer === "string" ? JSON.parse(item.answer) : item.answer
              }))
            };
            setComparisonResult(parsedResult);
            setComparisonLoading(false);
            setWsMessage(""); // clear message on completion
          }

          // 🔹 Handle error
          else if (data.status === "error") {
            console.error("Comparison Error:", data.error_msg);
            setComparisonLoading(false);
            setWsMessage(`Error: ${data.error_msg}`);
          }

          // 🔹 Log every WS message for debugging
          console.log("[WS MESSAGE]", data.progress, "%", data.message || "", data.status || "");
          
        } catch (err) {
          console.error("WS parsing error:", err);
        }
      };

      wsRef.current.onclose = () => console.log("Comparison WS closed");
    } catch (err) {
      console.error("❌ Comparison failed:", err);
      setComparisonLoading(false);
    }
  };

  useEffect(() => {
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  return (
    <Paper 
      variant="outlined" 
      sx={{ 
        p: 2, 
        borderRadius: 2, 
        position: "relative",
        maxWidth: '100%',
        overflow: 'hidden'
      }}
    >
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Button 
          variant="outlined" 
          onClick={handleBack} 
          disabled={comparisonLoading}
          startIcon={<ArrowBack />}
          size="small"
          sx={{ mr: 2 }}
        >
          Back
        </Button>
        
        <Typography variant="h6" sx={{ fontWeight: "bold", color: 'primary.main', flex: 1 }}>
          Results
        </Typography>
      </Box>

      {/* Enhanced ResultTabs Component */}
      <ResultTabs
        comparisonTab={comparisonTab}
        setComparisonTab={setComparisonTab}
        comparisonLoading={comparisonLoading}
        ofnResult={ofnResult}
        gaResult={gaResult}
        comparisonResult={comparisonResult}
      />

      {/* Content Area with Safe Boundaries */}
      <Box sx={{ 
        minHeight: 400,
        maxHeight: '60vh',
        overflow: 'auto',
        mt: 2,
        pr: 1
      }}>
        {comparisonTab === 0 && <OfnResultViewer data={ofnResult?.result || ofnResult} />}
        {comparisonTab === 1 && <GaResultViewer data={gaResult?.result || gaResult} />}
        {comparisonTab === 2 && (
          <Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                onClick={handleStartComparison}
                disabled={comparisonLoading}
                size="medium"
              >
                {comparisonLoading ? "Comparing..." : "Start Comparison"}
              </Button>

            </Box>

            {!comparisonLoading && comparisonResult && (
              <ComparisonViewer data={comparisonResult} />
            )}
          </Box>
        )}
      </Box>

      {/* Enhanced Overlay */}
      {comparisonLoading && (
        <Box sx={{ flex: 1, minWidth: 200 }}>
          <LinearProgress sx={{ height: 8, borderRadius: 2 }} />
          <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
            Processing your comparison...
          </Typography>
        </Box>
      )}

      {/*Simplified overlay - remove percentage and backend messages*/}
      {comparisonLoading && (
        <Box
          sx={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0,0,0,0.7)",
            zIndex: 2000,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
          }}
        >
          <Box sx={{ textAlign: 'center', p: 3, maxWidth: 400 }}>
            <Typography variant="h6" gutterBottom fontWeight="bold">
              Comparing Documents
            </Typography>
            <LinearProgress sx={{ width: "100%", height: 6, borderRadius: 3, mb: 2 }} />
            <Typography variant="body2">
              Please wait while we compare your documents...
            </Typography>
          </Box>
        </Box>
      )}
    </Paper>
  );
};

export default ComparisonStep;