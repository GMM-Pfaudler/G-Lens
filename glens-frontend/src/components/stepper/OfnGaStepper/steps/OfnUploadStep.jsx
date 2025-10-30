import React, { useEffect } from "react";
import { Paper, Typography, Box, Button } from "@mui/material";
import OfnUploader from "../../../uploads/OfnUploader";
import { useComparison } from "../../../../context/ComparisonContext";

const OfnUploadStep = ({ handleNext }) => {
  const {
    ofnFile,
    setOfnFile,
    ofnLoading,
    setOfnLoading,
    ofnExtracted,
    setOfnExtracted,
    ofnResult,
    setOfnResult
  } = useComparison();

  // -------------------------
  // Restore from localStorage on mount
  // -------------------------
  useEffect(() => {
    const savedOfnResult = localStorage.getItem("ofnResult");
    const savedOfnFileName = localStorage.getItem("ofnFileName");

    if (savedOfnResult) {
      setOfnResult(JSON.parse(savedOfnResult));
      setOfnExtracted(true);
    }

    if (savedOfnFileName) {
      setOfnFile({ name: savedOfnFileName }); // minimal info for display
    }
  }, []);

  // -------------------------
  // Persist result whenever it changes
  // -------------------------
  useEffect(() => {
    if (ofnResult) {
      localStorage.setItem("ofnResult", JSON.stringify(ofnResult));
      console.log("Saved ofnResult to localStorage:", ofnResult);
    }
  }, [ofnResult]);

  // -------------------------
  // Persist file name whenever it changes
  // -------------------------
  useEffect(() => {
    if (ofnFile) {
      localStorage.setItem("ofnFileName", ofnFile.name);
      console.log("Saved ofnFile name to localStorage:", ofnFile.name);
    }
  }, [ofnFile]);

  const nextDisabled = !ofnExtracted;

  return (
    <Paper variant="outlined" sx={{ p: 3, borderRadius: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2 }}>
        Upload OFN PDF
      </Typography>

      <OfnUploader />

      {ofnFile?.name && (
        <Typography variant="body2" sx={{ mt: 1 }}>
          Selected file: {ofnFile.name}
        </Typography>
      )}

      <Box sx={{ mt: 3 }}>
        <Button variant="contained" onClick={handleNext} disabled={nextDisabled}>
          Next
        </Button>
      </Box>
    </Paper>
  );
};

export default OfnUploadStep;
  