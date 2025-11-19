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
      <Typography variant="h5" fontWeight="bold">
        PDF Splitter
      </Typography>

      <Button
        variant="contained"
        startIcon={<UploadFileIcon />}
        onClick={onStart}
      >
        Upload PDF
      </Button>
    </Box>
  );
};

export default PdfSplitHeader;
