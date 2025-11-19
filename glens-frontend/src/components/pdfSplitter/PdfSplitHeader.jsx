import React from "react";
import { Box, Button, Typography } from "@mui/material";
import UploadFileIcon from "@mui/icons-material/UploadFile";

const PdfSplitHeader = ({ onStart }) => {
  return (
    <Box
      mb={3}
      display="flex"
      justifyContent="space-between"
      alignItems="center"
    >
      <Typography variant="h5" fontWeight="bold" color="#0e2980">
        PDF Splitter
      </Typography>

      <Button
        variant="contained"
        startIcon={<UploadFileIcon />}
        onClick={onStart}
        sx={{
          backgroundColor: "#0e2980",
          '&:hover': {
            backgroundColor: "#1a3a9e",
            transform: 'translateY(-1px)',
          },
          transition: 'all 0.2s ease',
        }}
      >
        Upload PDF
      </Button>
    </Box>
  );
};

export default PdfSplitHeader;