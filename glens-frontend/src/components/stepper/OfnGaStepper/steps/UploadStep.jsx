import React, { useEffect, useRef} from "react";
import { Paper, Typography, Box, Button } from "@mui/material";
import { History } from "@mui/icons-material";
import OfnUploader from "../../../uploads/OfnUploader";
import GaUploader from "../../../uploads/GaUpload";
import UploadCard from "./UploadCard";
import StatusSummary from "./StatusSummary";
import { useComparison } from "../../../../context/ComparisonContext";
import { useNavigate } from "react-router-dom";

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

  const navigate = useNavigate();

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

  const nextDisabled = !(ofnExtracted && gaExtracted);

  const handleViewHistory = () => {
    console.log("View History clicked");
    // Replace with modal or navigation later
  };

  return (
    <Paper
      elevation={0}
      sx={{
        p: 4,
        borderRadius: 4,
        background: "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
        border: "1px solid",
        borderColor: "divider",
        boxShadow: "0 4px 20px rgba(0,0,0,0.08)"
      }}
    >
      {/* Header */}
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
            mb: 1,
            background: "linear-gradient(135deg, #1976d2 0%, #1565c0 100%)",
            backgroundClip: "text",
            WebkitBackgroundClip: "text",
            color: "transparent"
          }}
        >
          Upload Documents
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 700, mx: "auto" }}>
          Upload both OFN and GA PDF documents to begin the comparison process
        </Typography>
      </Box>

      {/* Upload Panels */}
      <Box sx={{ display: "flex", flexDirection: { xs: "column", md: "row" }, gap: 3, mb: 4 }}>
        <UploadCard
          title="OFN Document"
          loading={ofnLoading}
          extracted={ofnExtracted}
          isProcessing={ofnLoading}
        >
          <OfnUploader
            file={ofnFile}
            setFile={setOfnFile}
            loading={ofnLoading}
            setLoading={setOfnLoading}
            extracted={ofnExtracted}
            setExtracted={setOfnExtracted}
            setOfnResult={setOfnResult}
          />
        </UploadCard>

        <UploadCard
          title="GA Document"
          loading={!!gaJobId && !gaExtracted}
          extracted={gaExtracted}
          isProcessing={!!gaJobId && !gaExtracted}
        >
          <GaUploader
            file={gaFile}
            setFile={setGaFile}
            gaResult={gaResult}
            setGaResult={setGaResult}
            gaJobId={gaJobId}
            setGaJobId={setGaJobId}
          />
        </UploadCard>
      </Box>

      {/* Status Summary */}
      <StatusSummary ofnExtracted={ofnExtracted} gaExtracted={gaExtracted} />

      {/* Action Buttons */}
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 2
        }}
      >
        <Button
          variant="outlined"
          onClick={() => navigate(`/ofn-ga-comparison/history`)}
          startIcon={<History />}
          sx={{
            px: 3,
            py: 1.2,
            borderRadius: 3,
            fontSize: "0.95rem",
            fontWeight: 600,
            textTransform: "none",
            borderWidth: 2,
            "&:hover": {
              borderWidth: 2,
              transform: "translateY(-1px)",
              boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
            }
          }}
        >
          View History
        </Button>

        <Button
          variant="contained"
          onClick={handleNext}
          disabled={nextDisabled}
          size="large"
          sx={{
            px: 4,
            py: 1.2,
            borderRadius: 3,
            fontSize: "1rem",
            fontWeight: 600,
            textTransform: "none",
            boxShadow: "0 4px 12px rgba(25, 118, 210, 0.3)",
            "&:hover": {
              boxShadow: "0 6px 16px rgba(25, 118, 210, 0.4)",
              transform: "translateY(-1px)"
            },
            "&:disabled": {
              boxShadow: "none",
              transform: "none"
            }
          }}
        >
          Continue to Comparison
        </Button>
      </Box>
    </Paper>
  );
};

export default UploadStep;
