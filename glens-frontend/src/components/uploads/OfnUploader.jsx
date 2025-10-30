import React from "react";
import { 
  Button, 
  Box, 
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
  AutoAwesome
} from "@mui/icons-material";
import { extractOfn } from "../../services/ofnService";
import { useComparison } from "../../context/ComparisonContext";

const OfnUploader = () => {
  const {
    ofnFile,
    setOfnFile,
    ofnLoading,
    setOfnLoading,
    ofnExtracted,
    setOfnExtracted,
    setOfnResult
  } = useComparison();

  const handleUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setOfnFile(selectedFile);
    setOfnResult(null);
    setOfnExtracted(false);
  };

  const handleExtract = async () => {
    if (!ofnFile) return;

    setOfnLoading(true);
    try {
      const data = await extractOfn(ofnFile);
      setOfnResult(data);
      setOfnExtracted(true);
    } catch (err) {
      console.error("Extraction failed:", err);
    } finally {
      setOfnLoading(false);
    }
  };

  const handleRemove = () => {
    setOfnFile(null);
    setOfnResult(null);
    setOfnExtracted(false);
  };

  const isExtracting = ofnLoading;
  const isExtracted = ofnExtracted;

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
              OFN Document
            </Typography>
          </Box>
        </Stack>

        {/* Upload Area */}
        {!ofnFile && (
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
            Upload OFN PDF
            <input hidden type="file" accept=".pdf" onChange={handleUpload} />
          </Button>
        )}

        {/* File Info & Actions */}
        {ofnFile && (
          <Box>
            <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ mb: 1 }}>
              <Stack direction="row" alignItems="center" spacing={1} sx={{ flex: 1 }}>
                <Description color="primary" sx={{ fontSize: 20 }} />
                <Box sx={{ minWidth: 0, flex: 1 }}>
                  <Typography variant="body2" fontWeight="medium" noWrap>
                    {ofnFile.name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {(ofnFile.size / 1024 / 1024).toFixed(2)} MB
                  </Typography>
                </Box>
              </Stack>

              <Stack direction="row" spacing={1} alignItems="center">
                {!isExtracted ? (
                  <Button
                    variant="contained"
                    size="small"
                    onClick={handleExtract}
                    disabled={isExtracting}
                    startIcon={isExtracting ? <AutoAwesome /> : null}
                    sx={{ minWidth: 100 }}
                  >
                    {isExtracting ? 'Extracting...' : 'Extract'}
                  </Button>
                ) : (
                  <Chip 
                    icon={<CheckCircle />} 
                    label="Extracted" 
                    color="success" 
                    size="small"
                  />
                )}
                
                <Button 
                  size="small" 
                  onClick={handleRemove}
                  variant="outlined"
                  disabled={isExtracting}
                >
                  Change
                </Button>
              </Stack>
            </Stack>

            {/* Loading Indicator */}
            {isExtracting && (
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
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default OfnUploader;