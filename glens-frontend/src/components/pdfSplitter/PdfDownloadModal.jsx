import React from "react";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemText,
  Box,
  Typography,
  Chip,
} from "@mui/material";
import { Download, InsertDriveFile } from "@mui/icons-material";

const PdfDownloadModal = ({ open, onClose, record }) => {
  if (!record) return null;

  const files = record.files || [];
  const API_BASE = import.meta.env.VITE_API_URL;

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle sx={{ 
        backgroundColor: "#f8fafc",
        borderBottom: "1px solid #e2e8f0"
      }}>
        <Typography variant="h6" fontWeight="bold">
          Download Parts
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {record.filename}
        </Typography>
      </DialogTitle>

      <DialogContent dividers sx={{ p: 0 }}>
        {files.length > 0 ? (
          <List>
            {files.map((file, index) => {
              const fileName = file.download_url.split(/[/\\]/).pop();
              
              return (
                <ListItem 
                  key={index} 
                  divider
                  sx={{
                    '&:hover': {
                      backgroundColor: '#f8fafc'
                    }
                  }}
                >
                  <InsertDriveFile sx={{ color: "#0e2980", mr: 2 }} />
                  
                  <ListItemText 
                    primary={
                      <Typography variant="body1" sx={{ fontWeight: 500 }}>
                        {fileName}
                      </Typography>
                    }
                    secondary={`Part ${index + 1}`}
                  />

                  <Chip 
                    label={`Part ${index + 1}`}
                    size="small"
                    variant="outlined"
                    sx={{ mr: 2, borderColor: "#0e2980", color: "#0e2980" }}
                  />

                  <Button
                    variant="contained"
                    size="small"
                    startIcon={<Download />}
                    href={`${API_BASE}/pdf-splitter/download?file_path=${encodeURIComponent(
                      file.download_url
                    )}`}
                    target="_blank"
                    sx={{
                      backgroundColor: "#0e2980",
                      '&:hover': {
                        backgroundColor: "#1a3a9e",
                      }
                    }}
                  >
                    Download
                  </Button>
                </ListItem>
              );
            })}
          </List>
        ) : (
          <Box sx={{ textAlign: "center", p: 4 }}>
            <Typography color="text.secondary">
              No files available for download
            </Typography>
          </Box>
        )}
      </DialogContent>

      <DialogActions sx={{ p: 2 }}>
        <Button 
          onClick={onClose}
          sx={{ color: "text.secondary" }}
        >
          Close
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default PdfDownloadModal;