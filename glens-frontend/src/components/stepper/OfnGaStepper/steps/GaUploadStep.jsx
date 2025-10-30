import React, { useEffect, useRef } from "react";
import { Paper, Typography, Box, Button } from "@mui/material";
import GaUploader from "../../../uploads/GaUpload";
import { useComparison } from "../../../../context/ComparisonContext";

const API_URL = import.meta.env.VITE_API_URL;

const GaUploadStep = ({ handleNext, handleBack }) => {
  const {
    gaFile,
    setGaFile,
    gaResult,
    setGaResult,
    gaJobId,
    setGaJobId
  } = useComparison(); // ✅ use context instead of local state

  const wsRef = useRef(null);

  useEffect(() => {
    if (!gaJobId) return;

    const wsUrl = `${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${gaJobId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => console.log(`✅ Connected to GA WebSocket: job ${gaJobId}`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("[WS MESSAGE]", data);
        setGaResult((prev) => ({ ...prev, ...data })); // update context state
      } catch (err) {
        console.error("Invalid WS message:", event.data, err);
      }
    };

    ws.onclose = () => {
      wsRef.current = null;
      console.log("WebSocket closed");
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
      ws.close();
    };

    return () => {
      if (wsRef.current) wsRef.current.close();
      wsRef.current = null;
    };
  }, [gaJobId]);

  const nextDisabled = !(gaResult?.status === "completed");

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
        Upload GA File
      </Typography>

      <GaUploader />

      <Box sx={{ mt: 3, display: "flex", justifyContent: "space-between" }}>
        <Button variant="outlined" onClick={handleBack}>
          Back
        </Button>
        <Button variant="contained" onClick={handleNext} disabled={nextDisabled}>
          Next
        </Button>
      </Box>
    </Paper>
  );
};

export default GaUploadStep;
