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
import { useComparison } from "../../context/ComparisonContext";

const GaUploader = () => {
  const {
    gaFile, setGaFile,
    gaResult, setGaResult,
    gaJobId, setGaJobId,
    setGaExtracted
  } = useComparison();

  const [localFile, setLocalFile] = useState(null);

  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setLocalFile(selectedFile);
    setGaFile(selectedFile);
    setGaResult(null);
    setGaJobId(null);
    setGaExtracted(false);
  };

  const handleExtract = async () => {
    if (!gaFile) return;

    try {
      const data = await extractGa(gaFile);
      const newResult = { status: "started", progress: 0, ...data };
      setGaResult(newResult);
      if (data.job_id) setGaJobId(data.job_id);
    } catch (err) {
      console.error("[GaUploader] Extraction error:", err);
      setGaResult({ status: "error", message: err.message });
    }
  };

  useEffect(() => {
    if (gaResult?.status === "completed") {
      setGaExtracted(true);
    }
  }, [gaResult, setGaExtracted]);

  const handleRemove = () => {
    setLocalFile(null);
    setGaFile(null);
    setGaResult(null);
    setGaJobId(null);
    setGaExtracted(false);
  };

  const isRunning = gaResult?.status === "started" || gaResult?.status === "running";
  const isCompleted = gaResult?.status === "completed";
  const isError = gaResult?.status === "error";

  const displayFile = localFile || gaFile;

  return (
    <Card variant="outlined" sx={{ mb: 2, borderColor: 'grey.300' }}>
      <CardContent sx={{ p: 2 }}>
        {/* Compact Header */}
        <Stack direction="row" alignItems="center" spacing={1.5} sx={{ mb: 1.5 }}>
          <Box
            sx={{
              width: 32,
              height: 32,
              borderRadius: '50%',
              backgroundColor: 'primary.main',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white'
            }}
          >
            <Description fontSize="small" />
          </Box>
          <Box>
            <Typography variant="subtitle1" fontWeight="bold" color="primary.main">
              GA Document
            </Typography>
          </Box>
        </Stack>

        {/* Upload Area */}
        {!displayFile && (
          <Button 
            variant="outlined" 
            component="label" 
            startIcon={<CloudUpload />}
            fullWidth
            size="small"
            sx={{ 
              py: 1,
              borderStyle: 'dashed',
              borderWidth: 1,
              borderColor: 'grey.400',
              '&:hover': {
                borderColor: 'primary.main',
                boxShadow: '0 0 0 2px rgba(25, 118, 210, 0.1)'
              }
            }}
          >
            Upload GA PDF
            <input hidden type="file" accept=".pdf" onChange={handleUpload} />
          </Button>
        )}

        {/* File Info & Actions */}
        {displayFile && (
          <Box>
            <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1 }}>
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
                    disabled={!gaFile}
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

            {/* Loading Indicator */}
            {isRunning && (
              <Box sx={{ mt: 1 }}>
                <LinearProgress 
                  sx={{ 
                    height: 4, 
                    borderRadius: 2,
                  }} 
                />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  Extracting data...
                </Typography>
              </Box>
            )}

            {/* Upload Processing Indicator */}
            {localFile && !gaFile && (
              <Box sx={{ mt: 1 }}>
                <LinearProgress 
                  sx={{ 
                    height: 4, 
                    borderRadius: 2,
                  }} 
                />
                <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                  Processing upload...
                </Typography>
              </Box>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default GaUploader;