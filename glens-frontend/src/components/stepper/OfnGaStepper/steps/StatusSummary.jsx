// src/components/comparison/upload/StatusSummary.jsx
import { Box, Typography } from "@mui/material";

const StatusSummary = ({ ofnExtracted, gaExtracted }) => {
  const nextDisabled = !(ofnExtracted && gaExtracted);
  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        p: 2,
        borderRadius: 2,
        backgroundColor: nextDisabled ? 'action.hover' : 'success.light',
        transition: 'all 0.3s ease',
        mb: 3
      }}
    >
      <Typography variant="body2" sx={{ fontWeight: 500 }}>
        {nextDisabled ? 'Upload and process both documents to continue' : 'All documents processed successfully!'}
      </Typography>
      <Typography variant="body2" sx={{ fontWeight: 600 }}>
        {ofnExtracted ? '✓ OFN Ready' : '⏳ OFN Pending'} • {gaExtracted ? '✓ GA Ready' : '⏳ GA Pending'}
      </Typography>
    </Box>
  );
};

export default StatusSummary;
