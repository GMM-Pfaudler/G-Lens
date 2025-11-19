import React, { useState } from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  CircularProgress,
} from "@mui/material";
import { UploadFile, CloudUpload } from "@mui/icons-material";
import { uploadPdfForSplit } from "../../services/pdfService";

const PdfUploadModal = ({ open, onClose, onSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Select a PDF");

    setLoading(true);
    try {
      const result = await uploadPdfForSplit(file);
      if (onSuccess) onSuccess(result);
      onClose();
      setFile(null); // Reset file on success
    } catch (err) {
      console.error(err);
      alert("Failed to upload");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setFile(null);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ 
        backgroundColor: "#f8fafc",
        borderBottom: "1px solid #e2e8f0"
      }}>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <CloudUpload color="primary" />
          <Typography variant="h6" fontWeight="bold">
            Upload PDF
          </Typography>
        </Box>
      </DialogTitle>

      <DialogContent dividers sx={{ p: 3 }}>
        <Box
          sx={{
            border: "2px dashed #e2e8f0",
            borderRadius: 2,
            p: 4,
            textAlign: "center",
            backgroundColor: "#fafbfc",
            transition: "all 0.3s ease",
            "&:hover": {
              borderColor: "#0e2980",
              backgroundColor: "#f0f7ff"
            }
          }}
        >
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files[0])}
            style={{ display: "none" }}
            id="pdf-upload-input"
          />
          <label htmlFor="pdf-upload-input">
            <Button
              component="span"
              variant="outlined"
              startIcon={<UploadFile />}
              sx={{
                borderColor: "#0e2980",
                color: "#0e2980",
                mb: 2,
                '&:hover': {
                  borderColor: "#1a3a9e",
                  backgroundColor: "#f0f7ff"
                }
              }}
            >
              Choose PDF File
            </Button>
          </label>
          {file && (
            <Typography variant="body2" sx={{ mt: 2, color: "success.main" }}>
              Selected: {file.name}
            </Typography>
          )}
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
            Select a PDF file to split into multiple parts
          </Typography>
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 2, gap: 1 }}>
        <Button 
          onClick={handleClose}
          sx={{ color: "text.secondary" }}
        >
          Cancel
        </Button>
        <Button 
          variant="contained" 
          disabled={loading || !file}
          onClick={handleUpload}
          startIcon={loading ? <CircularProgress size={16} /> : null}
          sx={{
            backgroundColor: "#0e2980",
            '&:hover': {
              backgroundColor: "#1a3a9e",
            },
            '&:disabled': {
              backgroundColor: '#e2e8f0'
            }
          }}
        >
          {loading ? "Uploading..." : "Upload PDF"}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default PdfUploadModal;