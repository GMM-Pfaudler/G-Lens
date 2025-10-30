import React, { useEffect, useState } from "react";
import {
  Box,
  Button,
  Typography,
  Chip,
  LinearProgress,
  Card,
  CardContent,
  Stack
} from "@mui/material";
import {
  CloudUpload,
  Description,
  CheckCircle,
  Error,
  AutoAwesome
} from "@mui/icons-material";
import { extractGa } from "../../services/gaService";

/**
 * A lightweight reusable GA uploader.
 * It works for firstGa or secondGa depending on props.
 */
const GaUploaderGeneric = ({
  file,
  setFile,
  gaResult,
  setGaResult,
  gaJobId,
  setGaJobId,
  setExtracted,
  label = "GA Document"
}) => {
  const [localFile, setLocalFile] = useState(null);

  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;
    setLocalFile(selectedFile);
    setFile(selectedFile);
    setGaResult(null);
    setGaJobId(null);
    setExtracted(false);
  };

  const handleExtract = async () => {
    if (!file) return;
    try {
      const data = await extractGa(file);
      const newResult = { status: "started", progress: 0, ...data };
      setGaResult(newResult);
      if (data.job_id) setGaJobId(data.job_id);
    } catch (err) {
      console.error("[GaUploaderGeneric] Extraction error:", err);
      setGaResult({ status: "error", message: err.message });
    }
  };

  useEffect(() => {
    if (gaResult?.status === "completed") {
      setExtracted(true);
    }
  }, [gaResult, setExtracted]);

  const handleRemove = () => {
    setLocalFile(null);
    setFile(null);
    setGaResult(null);
    setGaJobId(null);
    setExtracted(false);
  };

  const isRunning = gaResult?.status === "started" || gaResult?.status === "running";
  const isCompleted = gaResult?.status === "completed";
  const isError = gaResult?.status === "error";
  const displayFile = localFile || file;

  return (
    <Card variant="outlined" sx={{ mb: 2, borderColor: "grey.300" }}>
      <CardContent sx={{ p: 2 }}>
        <Stack direction="row" alignItems="center" spacing={1.5} sx={{ mb: 1.5 }}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: "50%",
              backgroundColor: "primary.main",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "white"
            }}
          >
            <Description fontSize="small" />
          </Box>
          <Typography variant="subtitle1" fontWeight="bold" color="primary.main">
            {label}
          </Typography>
        </Stack>

        {!displayFile && (
          <Button
            variant="outlined"
            component="label"
            startIcon={<CloudUpload />}
            fullWidth
            size="small"
            sx={{
              py: 1,
              borderStyle: "dashed",
              borderWidth: 1,
              borderColor: "grey.400",
              "&:hover": {
                borderColor: "primary.main",
                boxShadow: "0 0 0 2px rgba(25, 118, 210, 0.1)"
              }
            }}
          >
            Upload GA PDF
            <input hidden type="file" accept=".pdf" onChange={handleUpload} />
          </Button>
        )}

        {displayFile && (
          <Box>
            <Stack
              direction="row"
              alignItems="center"
              justifyContent="space-between"
              sx={{ mb: 1 }}
            >
              <Stack direction="row" alignItems="center" spacing={1} sx={{ flex: 1 }}>
                <Description color="primary" sx={{ fontSize: 20 }} />
                <Box sx={{ minWidth: 0, flex: 1 }}>
                  <Typography variant="body2" fontWeight="medium" noWrap>
                    {displayFile.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(displayFile.size / 1024 / 1024).toFixed(2)} MB
                  </Typography>
                </Box>
              </Stack>

              <Stack direction="row" spacing={1} alignItems="center">
                {!isCompleted && !isRunning ? (
                  <Button
                    variant="contained"
                    size="small"
                    onClick={handleExtract}
                    disabled={!file}
                    sx={{ minWidth: 100 }}
                  >
                    Extract
                  </Button>
                ) : isRunning ? (
                  <Button
                    variant="contained"
                    size="small"
                    disabled
                    startIcon={<AutoAwesome />}
                    sx={{ minWidth: 100 }}
                  >
                    Extracting...
                  </Button>
                ) : isCompleted ? (
                  <Chip
                    icon={<CheckCircle />}
                    label="Extracted"
                    color="success"
                    size="small"
                  />
                ) : isError ? (
                  <Chip
                    icon={<Error />}
                    label="Error"
                    color="error"
                    size="small"
                  />
                ) : null}

                <Button
                  size="small"
                  onClick={handleRemove}
                  variant="outlined"
                  disabled={isRunning}
                >
                  Change
                </Button>
              </Stack>
            </Stack>

            {isRunning && (
              <Box sx={{ mt: 1 }}>
                <LinearProgress sx={{ height: 4, borderRadius: 2 }} />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  Extracting data...
                </Typography>
              </Box>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default GaUploaderGeneric;
