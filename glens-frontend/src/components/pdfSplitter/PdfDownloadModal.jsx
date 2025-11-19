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
} from "@mui/material";

const PdfDownloadModal = ({ open, onClose, record }) => {
  if (!record) return null;

  const files = record.files || []; // file objects from your API

  const API_BASE = import.meta.env.VITE_API_URL;

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Download Parts for {record.filename}</DialogTitle>

      <DialogContent dividers>
        <List>
          {files.length > 0 ? (
            files.map((file, index) => {
              // Extract actual file name from full Windows path
              const fileName = file.download_url.split(/[/\\]/).pop();

              return (
                <ListItem key={index} divider>
                  <ListItemText primary={fileName} />

                  <Button
                    variant="outlined"
                    size="small"
                    href={`${API_BASE}/pdf-splitter/download?file_path=${encodeURIComponent(
                        file.download_url
                    )}`}
                    target="_blank"
                    >
                    Download
                    </Button>
                </ListItem>
              );
            })
          ) : (
            <p>No files available.</p>
          )}
        </List>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PdfDownloadModal;
