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
  Stack,
} from "@mui/material";
import {
  Close as CloseIcon,
  CloudUpload as UploadIcon,
  CheckCircle as SuccessIcon,
  Error as ErrorIcon,
  PlayArrow as StartIcon,
  Refresh as RefreshIcon,
  Description as FileIcon,
} from "@mui/icons-material";
import axios from "axios";
import { extractOfn } from "../../services/ofnService";

// Reusable File Upload Card Component
const FileUploadCard = ({
  title,
  file,
  status,
  onFileSelect,
  onExtract,
  loading,
  accept = ".pdf",
}) => {
  const statusConfig = {
    loading: {
      color: "primary",
      icon: <CircularProgress size={16} />,
      text: "Extracting...",
    },
    success: { color: "success", icon: <SuccessIcon />, text: "Extracted" },
    ready: { color: "primary", icon: <UploadIcon />, text: "Ready to extract" },
    pending: { color: "default", icon: <UploadIcon />, text: "Upload file" },
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
        border: "1px solid",
        borderColor: "grey.200",
        borderRadius: 2,
        background: "white",
      }}
    >
      <CardContent sx={{ p: 2.5 }}>
        <Stack spacing={2}>
          {/* Header */}
          <Box
            display="flex"
            alignItems="center"
            justifyContent="space-between"
          >
            <Typography variant="h6" fontWeight="600" color="grey.800">
              {title}
            </Typography>
            <Chip
              icon={config.icon}
              label={config.text}
              color={config.color}
              variant="filled"
              size="small"
              sx={{ fontWeight: "500" }}
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
          {file && status !== "success" && (
            <Button
              variant="contained"
              onClick={onExtract}
              disabled={loading}
              startIcon={
                loading ? <CircularProgress size={16} /> : <RefreshIcon />
              }
              sx={{
                borderRadius: 2,
                alignSelf: "flex-start",
                background: loading
                  ? "grey.400"
                  : "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                "&:hover": {
                  background: loading
                    ? "grey.400"
                    : "linear-gradient(135deg, #2563eb 0%, #1e40af 100%)",
                },
              }}
            >
              {loading ? "Extracting..." : "Extract"}
            </Button>
          )}
        </Stack>
      </CardContent>
    </Card>
  );
};

// Main Modal Component
const UploadComparisonModal = ({ open, onClose, onSuccess }) => {
  const API_URL = import.meta.env.VITE_API_URL;

  // State management
  const [files, setFiles] = useState({ ofn: null, ga: null });
  const [results, setResults] = useState({ ofn: null, ga: null });
  const [loading, setLoading] = useState({
    ofn: false,
    ga: false,
    comparison: false,
  });
  const [message, setMessage] = useState("");
  const wsGaRef = useRef(null);

  // Derived states
  const canStartComparison = results.ofn && results.ga && !loading.comparison;

  const getFileStatus = (type) => {
    if (loading[type] === "uploading") return "uploading";
    if (loading[type]) return "loading";
    if (results[type]) return "success";
    if (files[type]) return "ready";
    return "pending";
  };

  // File handlers
  const handleFileSelect = (type) => (event) => {
    const file = event.target.files[0];
    if (file) {
      setFiles((prev) => ({ ...prev, [type]: file }));
      setResults((prev) => ({ ...prev, [type]: null }));
    }
  };

  // Extraction handlers
  const handleExtractOfn = async () => {
    if (!files.ofn) return;
    setLoading((prev) => ({ ...prev, ofn: "uploading" }));
    setMessage("Uploading OFN...");

    try {
      const formData = new FormData();
      formData.append("file", files.ofn);

      const res = await axios.post(`${API_URL}/api/ofn/extract`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (ev) => {
          const percent = Math.round((ev.loaded * 100) / ev.total);
          setMessage(`Uploading OFN: ${percent}%`);
        },
      });
      setLoading((prev) => ({ ...prev, ofn: true }));
      setMessage("Extracting OFN file...");

      const data = await extractOfn(files.ofn);
      setResults((prev) => ({ ...prev, ofn: data.result }));
      setMessage("OFN extraction completed successfully!");
    } catch (error) {
      setMessage("OFN extraction failed");
      console.error("OFN extraction error:", error);
    } finally {
      setLoading((prev) => ({ ...prev, ofn: false }));
    }
  };

  const handleExtractGa = async () => {
    if (!files.ga) return;

    setLoading((prev) => ({ ...prev, ga: "uploading" }));
    setMessage("Uploading GA File...");
    try {
      const formData = new FormData();
      formData.append("file", files.ga);

      const res = await axios.post(`${API_URL}/api/ga/extract`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (ev) => {
          const percent = Math.round((ev.loaded * 100) / ev.total);
          setMessage(`Uploading GA: ${percent}%`);
        },
      });
      setLoading((prev) => ({ ...prev, ga: true }));
      setMessage("GA extraction started...");

      const ws = new WebSocket(
        `${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${res.data.job_id}`
      );
      wsGaRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setResults((prev) => ({
          ...prev,
          ga: { ...(prev.ga || {}), ...(data.result || {}) },
        }));

        if (data.status === "completed") {
          setMessage("GA extraction completed successfully!");
          setLoading((prev) => ({ ...prev, ga: false }));
        } else if (data.status === "error") {
          setMessage("GA extraction failed");
          setLoading((prev) => ({ ...prev, ga: false }));
          ws.close();
        } else {
          setMessage(`GA extraction: ${data.status}...`);
        }
      };

      ws.onclose = () => console.log("GA WebSocket closed");
      ws.onerror = () => {
        setMessage("WebSocket connection error for GA extraction");
        setLoading((prev) => ({ ...prev, ga: false }));
      };
    } catch (err) {
      console.error("GA extraction error:", err);
      setMessage("GA extraction failed");
      setLoading((prev) => ({ ...prev, ga: false }));
    }
  };

  // Comparison handler
  const handleStartComparison = async () => {
    if (!canStartComparison) return;

    setLoading((prev) => ({ ...prev, comparison: true }));
    setMessage("Starting comparison process...");

    try {
      const userId = localStorage.getItem("user_id");
      const formData = new FormData();
      formData.append(
        "ofn_json",
        new Blob([JSON.stringify(results.ofn)], { type: "application/json" }),
        "ofn.json"
      );
      formData.append(
        "ga_json",
        new Blob([JSON.stringify(results.ga)], { type: "application/json" }),
        "ga.json"
      );

      const res = await axios.post(
        `${API_URL}/api/comparison/ofn-ga/start?user_id=${userId}`,
        formData
      );

      if (res.status === 200) {
        setMessage("Comparison started successfully!");
        handleClose();
        onSuccess?.();
      } else {
        throw new Error("Failed to start comparison");
      }
    } catch (err) {
      console.error("Comparison error:", err);
      setMessage("Failed to start comparison");
    } finally {
      setLoading((prev) => ({ ...prev, comparison: false }));
    }
  };

  // Cleanup
  const handleClose = () => {
    wsGaRef.current?.close();
    setFiles({ ofn: null, ga: null });
    setResults({ ofn: null, ga: null });
    setLoading({ ofn: false, ga: false, comparison: false });
    setMessage("");
    onClose();
  };

  const getAlertSeverity = () => {
    if (message.includes("successfully")) return "success";
    if (message.includes("failed") || message.includes("error")) return "error";
    return "info";
  };

  return (
    <Dialog
      open={open}
      onClose={(event, reason) => {
        if (reason === "backdropClick" || reason === "escapeKeyDown") return;
        handleClose();
      }}
      maxWidth="sm"
      fullWidth
    >
      <DialogTitle sx={{ pb: 2 }}>
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="space-between"
        >
          <Typography variant="h5" fontWeight="600">
            Start New Comparison
          </Typography>
          <IconButton onClick={handleClose} size="small">
            <CloseIcon />
          </IconButton>
        </Stack>
      </DialogTitle>

      <DialogContent>
        <Stack spacing={2}>
          <FileUploadCard
            title="OFN File"
            file={files.ofn}
            status={getFileStatus("ofn")}
            onFileSelect={handleFileSelect("ofn")}
            onExtract={handleExtractOfn}
            loading={loading.ofn !== false}
          />

          <FileUploadCard
            title="GA File"
            file={files.ga}
            status={getFileStatus("ga")}
            onFileSelect={handleFileSelect("ga")}
            onExtract={handleExtractGa}
            loading={loading.ga !== false}
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
          startIcon={
            loading.comparison ? <CircularProgress size={16} /> : <StartIcon />
          }
          sx={{
            borderRadius: 2,
            px: 3,
            fontWeight: "600",
            background: !canStartComparison
              ? "grey.400"
              : "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
            "&:hover": {
              background: !canStartComparison
                ? "grey.400"
                : "linear-gradient(135deg, #2563eb 0%, #1e40af 100%)",
            },
          }}
        >
          {loading.comparison ? "Starting..." : "Start Comparison"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default UploadComparisonModal;
