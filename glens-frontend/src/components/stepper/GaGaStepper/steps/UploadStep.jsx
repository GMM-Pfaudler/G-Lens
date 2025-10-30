import React, { useEffect, useRef } from "react";
import { Paper, Typography, Box, Button } from "@mui/material";
import GaUploaderGeneric from "../../../uploads/GaUploaderGeneric";
import { useComparison } from "../../../../context/ComparisonContext";

const API_URL = import.meta.env.VITE_API_URL;

const UploadStep = ({ handleNext }) => {
  const {
    firstGaFile,
    setFirstGaFile,
    firstGaResult,
    setFirstGaResult,
    firstGaJobId,
    setFirstGaJobId,
    firstGaExtracted,
    setFirstGaExtracted,
    secondGaFile,
    setSecondGaFile,
    secondGaResult,
    setSecondGaResult,
    secondGaJobId,
    setSecondGaJobId,
    secondGaExtracted,
    setSecondGaExtracted
  } = useComparison();

  const wsRefFirst = useRef(null);
  const wsRefSecond = useRef(null);

  /** --- WebSocket for first GA extraction --- */
  useEffect(() => {
    if (!firstGaJobId) return;
    const ws = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${firstGaJobId}`);
    wsRefFirst.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setFirstGaResult((prev) => ({ ...prev, ...data }));
    };
    ws.onclose = () => (wsRefFirst.current = null);
    ws.onerror = () => ws.close();

    return () => wsRefFirst.current?.close();
  }, [firstGaJobId]);

  /** --- WebSocket for second GA extraction --- */
  useEffect(() => {
    if (!secondGaJobId) return;
    const ws = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${secondGaJobId}`);
    wsRefSecond.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setSecondGaResult((prev) => ({ ...prev, ...data }));
    };
    ws.onclose = () => (wsRefSecond.current = null);
    ws.onerror = () => ws.close();

    return () => wsRefSecond.current?.close();
  }, [secondGaJobId]);

  const nextDisabled = !(firstGaExtracted && secondGaExtracted);

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
        Upload GA Files
      </Typography>

      {/* First GA Upload */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1">First GA</Typography>
        <GaUploaderGeneric
            file={firstGaFile}
            setFile={setFirstGaFile}
            gaResult={firstGaResult}
            setGaResult={setFirstGaResult}
            gaJobId={firstGaJobId}
            setGaJobId={setFirstGaJobId}
            setExtracted={setFirstGaExtracted}
        />
        </Box>

        <Box sx={{ mb: 3 }}>
        <Typography variant="subtitle1">Second GA</Typography>
        <GaUploaderGeneric
            file={secondGaFile}
            setFile={setSecondGaFile}
            gaResult={secondGaResult}
            setGaResult={setSecondGaResult}
            gaJobId={secondGaJobId}
            setGaJobId={setSecondGaJobId}
            setExtracted={setSecondGaExtracted}
        />
        </Box>

      <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
        <Button variant="contained" onClick={handleNext} disabled={nextDisabled}>
          Next
        </Button>
      </Box>
    </Paper>
  );
};

export default UploadStep;
