// src/components/comparison/upload/UploadCard.jsx
import React from "react";
import { Card, CardContent, Box, Typography, LinearProgress, Chip } from "@mui/material";
import { CloudUpload, CheckCircle, Pending } from "@mui/icons-material";

const UploadCard = ({
  title,
  loading,
  extracted,
  isProcessing,
  children,
}) => (
  <Card
    elevation={2}
    sx={{
      flex: 1,
      borderRadius: 3,
      border: extracted ? '2px solid #4caf50' : '1px solid',
      borderColor: extracted ? 'success.main' : 'divider',
      transition: 'all 0.3s ease',
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 8px 25px rgba(0,0,0,0.12)',
      }
    }}
  >
    <CardContent sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <CloudUpload sx={{ mr: 1.5, color: 'primary.main' }} />
        <Typography variant="h6" sx={{ fontWeight: 600 }}>
          {title}
        </Typography>
        <Box sx={{ flex: 1 }} />
        {extracted ? (
          <Chip icon={<CheckCircle />} label="Completed" color="success" size="small" />
        ) : isProcessing ? (
          <Chip icon={<Pending />} label="Processing" color="warning" size="small" />
        ) : (
          <Chip label="Pending" color="default" size="small" variant="outlined" />
        )}
      </Box>

      {loading && (
        <LinearProgress
          sx={{
            mb: 2,
            borderRadius: 2,
            height: 6,
            '& .MuiLinearProgress-bar': { borderRadius: 2 }
          }}
        />
      )}

      {children}
    </CardContent>
  </Card>
);

export default UploadCard;
