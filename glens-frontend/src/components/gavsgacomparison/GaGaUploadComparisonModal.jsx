import React, { useState, useRef } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Chip,
  Alert,
  IconButton,
  Stack
} from "@mui/material";
import {
  Close as CloseIcon,
  CloudUpload as UploadIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  PlayArrow as StartIcon,
  Refresh as RefreshIcon,
  Description as FileIcon
} from "@mui/icons-material";
import axios from "axios";

// Reusing your FileUploadCard component
const FileUploadCard = ({ 
  title, 
  file, 
  status, 
  onFileSelect, 
  onExtract, 
  loading,
  accept = ".pdf"
}) => {
  const statusConfig = {
    loading: { color: 'primary', icon: <CircularProgress size={16} />, text: 'Extracting...' },
    success: { color: 'success', icon: <SuccessIcon />, text: 'Extracted' },
    ready: { color: 'primary', icon: <UploadIcon />, text: 'Ready to extract' },
    pending: { color: 'default', icon: <UploadIcon />, text: 'Upload file' },
    uploading: {
          color: "primary",
          icon: <CircularProgress size={16} />,
          text: "Uploading...",
        },
  };

  const config = statusConfig[status] || statusConfig.pending;

  return (
    <Card 
      variant="outlined" 
      sx={{ 
        mb: 2, 
        border: '1px solid',
        borderColor: 'grey.200',
        borderRadius: 2,
        background: 'white'
      }}
    >
      <CardContent sx={{ p: 2.5 }}>
        <Stack spacing={2}>
          {/* Header */}
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h6" fontWeight="600" color="grey.800">
              {title}
            </Typography>
            <Chip 
              icon={config.icon}
              label={config.text}
              color={config.color}
              variant="filled"
              size="small"
              sx={{ fontWeight: '500' }}
            />
          </Box>

          {/* File Selection */}
          <Stack direction="row" spacing={1.5} alignItems="center">
            <Button
              variant="outlined"
              component="label"
              startIcon={<UploadIcon />}
              disabled={loading}
              sx={{ borderRadius: 2 }}
            >
              Select File
              <input
                type="file"
                accept={accept}
                hidden
                onChange={onFileSelect}
              />
            </Button>

            {file && (
              <Stack direction="row" spacing={1} alignItems="center">
                <FileIcon color="primary" fontSize="small" />
                <Typography variant="body2" color="grey.700" fontWeight="500">
                  {file.name}
                </Typography>
              </Stack>
            )}
          </Stack>

          {/* Extract Button */}
          {file && status !== 'success' && (
            <Button
              variant="contained"
              onClick={onExtract}
              disabled={loading}
              startIcon={loading ? <CircularProgress size={16} /> : <RefreshIcon />}
              sx={{
                borderRadius: 2,
                alignSelf: 'flex-start',
                background: loading ? 'grey.400' : 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                '&:hover': {
                  background: loading ? 'grey.400' : 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
                }
              }}
            >
              {loading ? 'Extracting...' : 'Extract'}
            </Button>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};

// Main GA vs GA Modal Component
const GaVsGaComparisonModal = ({ open, onClose, onSuccess }) => {
  const API_URL = import.meta.env.VITE_API_URL;

  // State management for two GA instances
  const [files, setFiles] = useState({ ga1: null, ga2: null });
  const [results, setResults] = useState({ ga1: null, ga2: null });
  const [loading, setLoading] = useState({ 
    ga1: false, 
    ga2: false, 
    comparison: false 
  });
  const [message, setMessage] = useState("");
  const wsRefs = useRef({ ga1: null, ga2: null });

  // Derived states
  const canStartComparison = results.ga1 && results.ga2 && !loading.comparison;

  const getFileStatus = (type) => {
    if (loading[type] === "uploading") return "uploading";
    if (loading[type]) return 'loading';
    if (results[type]) return 'success';
    if (files[type]) return 'ready';
    return 'pending';
  };

  // File handlers
  const handleFileSelect = (type) => (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(prev => ({ ...prev, [type]: "uploading" }));
      setMessage(`Uploading ${type.toUpperCase()} file...`);
      setFiles(prev => ({ ...prev, [type]: file }));
      setResults(prev => ({ ...prev, [type]: null }));
      setLoading(prev => ({ ...prev, [type]: false}));
    }
    
  };

  // GA Extraction handler (reusable for both instances)
  const handleExtractGa = async (type) => {
    if (!files[type]) return;
    setLoading(prev => ({ ...prev, [type]: "uploading" }));
    setMessage(`Uploading ${type.toUpperCase()} file...`);
    
    try {
      const formData = new FormData();
      formData.append("file", files[type]);
      
      const res = await axios.post(`${API_URL}/api/ga/extract`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (ev)=>{
          const percent = Math.round((ev.loaded*100)/ev.total);
          setMessage(`Uploading GA: ${percent}%`);
        }
      });
      setLoading(prev => ({ ...prev, [type]: true }));
      setMessage(`Extracting ${type.toUpperCase()} file...`);
      
      const ws = new WebSocket(
        `${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${res.data.job_id}`
      );
      wsRefs.current[type] = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setResults(prev => ({ 
          ...prev, 
          [type]: { ...prev[type], ...data.result }
        }));
        
        if (data.status === 'completed') {
          setMessage(`${type.toUpperCase()} extraction completed successfully!`);
          setLoading(prev => ({ ...prev, [type]: false }));
        } else if (data.status === 'error') {
          setMessage(`${type.toUpperCase()} extraction failed`);
          setLoading(prev => ({ ...prev, [type]: false }));
          ws.close();
        } else {
          setMessage(`${type.toUpperCase()} extraction: ${data.status}...`);
        }
      };
      
      ws.onclose = () => console.log(`${type.toUpperCase()} WebSocket closed`);
      ws.onerror = () => {
        setMessage(`WebSocket connection error for ${type.toUpperCase()} extraction`);
        setLoading(prev => ({ ...prev, [type]: false }));
      };
      
    } catch (err) {
      console.error(`${type.toUpperCase()} extraction error:`, err);
      setMessage(`${type.toUpperCase()} extraction failed`);
      setLoading(prev => ({ ...prev, [type]: false }));
    }
  };

  // Comparison handler for GA vs GA
  const handleStartComparison = async () => {
    if (!canStartComparison) return;
    
    setLoading(prev => ({ ...prev, comparison: true }));
    setMessage("Starting GA vs GA comparison process...");

    try {
      const userId = localStorage.getItem("user_id");
      const formData = new FormData();
      formData.append("ga1_json", new Blob([JSON.stringify(results.ga1)], { type: "application/json" }), "ga1.json");
      formData.append("ga2_json", new Blob([JSON.stringify(results.ga2)], { type: "application/json" }), "ga2.json");

      const res = await axios.post(
        `${API_URL}/api/comparison/ga-ga/start?user_id=${userId}`, 
        formData
      );

      if (res.status === 200) {
        setMessage("GA vs GA comparison started successfully!");
        handleClose();
        onSuccess?.();
      } else {
        throw new Error("Failed to start GA vs GA comparison");
      }
    } catch (err) {
      console.error("GA vs GA comparison error:", err);
      setMessage("Failed to start GA vs GA comparison");
    } finally {
      setLoading(prev => ({ ...prev, comparison: false }));
    }
  };

  // Cleanup
  const handleClose = () => {
    // Close all WebSocket connections
    Object.values(wsRefs.current).forEach(ws => ws?.close());
    setFiles({ ga1: null, ga2: null });
    setResults({ ga1: null, ga2: null });
    setLoading({ ga1: false, ga2: false, comparison: false });
    setMessage("");
    onClose();
  };

  const getAlertSeverity = () => {
    if (message.includes('successfully')) return 'success';
    if (message.includes('failed') || message.includes('error')) return 'error';
    return 'info';
  };

  return (
    <Dialog 
      open={open} 
      onClose={(event, reason) => {
        if (reason === 'backdropClick' || reason === 'escapeKeyDown') return;
        handleClose();
      }}
      maxWidth="sm" 
      fullWidth
    >
      <DialogTitle sx={{ pb: 2 }}>
        <Stack direction="row" alignItems="center" justifyContent="space-between">
          <Typography variant="h5" fontWeight="600">
            GA vs GA Comparison
          </Typography>
          <IconButton onClick={handleClose} size="small">
            <CloseIcon />
          </IconButton>
        </Stack>
      </DialogTitle>

      <DialogContent>
        <Stack spacing={2}>
          <FileUploadCard
            title="First GA File"
            file={files.ga1}
            status={getFileStatus('ga1')}
            onFileSelect={handleFileSelect('ga1')}
            onExtract={() => handleExtractGa('ga1')}
            loading={loading.ga1 !== false}
          />

          <FileUploadCard
            title="Second GA File"
            file={files.ga2}
            status={getFileStatus('ga2')}
            onFileSelect={handleFileSelect('ga2')}
            onExtract={() => handleExtractGa('ga2')}
            loading={loading.ga2 !== false}
          />

          {message && (
            <Alert severity={getAlertSeverity()} sx={{ borderRadius: 2 }}>
              {message}
            </Alert>
          )}
        </Stack>
      </DialogContent>

      <DialogActions sx={{ p: 3, gap: 1 }}>
        <Button 
          onClick={handleClose} 
          disabled={loading.comparison}
          sx={{ borderRadius: 2, px: 3 }}
        >
          Cancel
        </Button>
        <Button
          variant="contained"
          onClick={handleStartComparison}
          disabled={!canStartComparison || loading.comparison}
          startIcon={loading.comparison ? <CircularProgress size={16} /> : <StartIcon />}
          sx={{
            borderRadius: 2,
            px: 3,
            fontWeight: '600',
            background: !canStartComparison ? 'grey.400' : 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            '&:hover': {
              background: !canStartComparison ? 'grey.400' : 'linear-gradient(135deg, #059669 0%, #047857 100%)',
            }
          }}
        >
          {loading.comparison ? 'Starting...' : 'Start GA vs GA'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default GaVsGaComparisonModal;