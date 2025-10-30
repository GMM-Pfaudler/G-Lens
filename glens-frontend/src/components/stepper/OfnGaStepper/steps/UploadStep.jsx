import React, { useEffect, useRef } from "react";
import { Paper, Typography, Box, Button } from "@mui/material";
import OfnUploader from "../../../uploads/OfnUploader";
import GaUploader from "../../../uploads/GaUpload";
import { useComparison } from "../../../../context/ComparisonContext";

const API_URL = import.meta.env.VITE_API_URL;

const UploadStep = ({ handleNext }) => {
  const {
    // OFN
    ofnFile,
    setOfnFile,
    ofnResult,
    setOfnResult,
    ofnLoading,
    setOfnLoading,
    ofnExtracted,
    setOfnExtracted,
    // GA
    gaFile,
    setGaFile,
    gaResult,
    setGaResult,
    gaJobId,
    setGaJobId,
    gaExtracted,
    setGaExtracted
  } = useComparison();

  const wsRef = useRef(null);

  /** --- WebSocket for GA extraction --- */
  useEffect(() => {
    if (!gaJobId) return;

    const wsUrl = `${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${gaJobId}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => console.log(`✅ Connected to GA WebSocket: job ${gaJobId}`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setGaResult((prev) => ({ ...prev, ...data }));
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

  /** --- Next button is enabled only if both extractions are completed --- */
  const nextDisabled = !(ofnExtracted && gaExtracted);

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
        Upload PDFs
      </Typography>

      {/* --- OFN Upload --- */}
      <OfnUploader
        file={ofnFile}
        setFile={setOfnFile}
        loading={ofnLoading}
        setLoading={setOfnLoading}
        extracted={ofnExtracted}
        setExtracted={setOfnExtracted}
        setOfnResult={setOfnResult}
      />

      {/* --- GA Upload --- */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle1" sx={{ mb: 1 }}>
          GA Upload
        </Typography>
        <GaUploader
          file={gaFile}
          setFile={setGaFile}
          gaResult={gaResult}
          setGaResult={setGaResult}
          gaJobId={gaJobId}
          setGaJobId={setGaJobId}
        />
      </Box>

      <Box sx={{ mt: 3, display: "flex", justifyContent: "flex-end" }}>
        <Button variant="contained" onClick={handleNext} disabled={nextDisabled}>
          Next
        </Button>
      </Box>
    </Paper>
  );
};

export default UploadStep;
