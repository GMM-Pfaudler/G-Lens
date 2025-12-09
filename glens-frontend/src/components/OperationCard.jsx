import React from "react";
import { 
  Card, 
  CardActionArea, 
  CardContent, 
  Typography, 
  Box,
  Chip 
} from "@mui/material";
import { Description as DescriptionIcon } from "@mui/icons-material";

// Icon mapping for different operation types
const operationIcons = {
  "OFN vs GA": "📊",
  "GA vs GA": "⚖️", 
  "BOM Comparison": "📋",
  "Model BOM vs Ref. BOM": "🔍",
  "3D BOM Comparison": "🧊🔍",
  "GA vs GA (Pixel)": "🖼️",
};

export default function OperationCard({ 
  label, 
  onClick, 
  icon: Icon, 
  description,
  status = "active",
  isNew = false 
}) {
  const getStatusColor = () => {
    switch(status) {
      case 'active': return 'success';
      case 'beta': return 'warning';
      case 'maintenance': return 'default';
      default: return 'primary';
    }
  };

  const getIconContent = () => {
    if (Icon) return <Icon sx={{ fontSize: 36, color: "#2563eb", mb: 1 }} />;
    if (operationIcons[label]) {
      return (
        <Box sx={{ fontSize: "2.2rem", mb: 1, lineHeight: 1 }}>
          {operationIcons[label]}
        </Box>
      );
    }
    return <DescriptionIcon sx={{ fontSize: 48, color: "#2563eb", mb: 1 }} />;
  };

  return (
    <Card
      variant="outlined"
      sx={{
        textAlign: "center",
        borderRadius: 3,
        borderColor: "#e2e8f0",
        background: "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
        width: { xs: "48%", sm: 160, md: 150 },
        height: { xs: 120, sm: 160, md: 150 },
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "relative",
        overflow: "hidden",
        "&:hover": {
          transform: "translateY(-6px)",
          boxShadow: "0 12px 28px rgba(37, 99, 235, 0.15)",
          borderColor: "#2563eb",
          background: "linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%)",
        },
        transition: "all 0.3s ease-in-out",
        mx: "auto",
      }}
    >
      {/* New Badge */}
      {isNew && (
        <Chip 
          label="NEW" 
          color="primary" 
          size="small"
          sx={{ 
            position: "absolute", 
            top: 8, 
            right: 8, 
            height: 20,
            fontSize: '0.7rem',
            fontWeight: 'bold'
          }} 
        />
      )}
      
      {/* Status Badge */}
      {status !== 'active' && (
        <Chip 
          label={status.toUpperCase()} 
          color={getStatusColor()}
          size="small"
          variant="outlined"
          sx={{ 
            position: "absolute", 
            top: 8, 
            left: 8, 
            height: 20,
            fontSize: '0.65rem',
          }} 
        />
      )}

      <CardActionArea
        onClick={onClick}
        sx={{
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          p: 1,
        }}
      >
        <CardContent sx={{ p: "0 !important" }}>
          <Box sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            {/* Icon Section */}
            {getIconContent()}
            
            {/* Label Section */}
            <Typography 
              variant="subtitle1" 
              sx={{ 
                fontWeight: 600,
                fontSize: { xs: '0.8rem', sm: '0.9rem' },
                lineHeight: 1.2,
                mb: 0.5
              }}
            >
              {label}
            </Typography>
            
            {/* Description (only show on hover or always based on preference) */}
            {description && (
              <Typography 
                variant="caption" 
                color="text.secondary"
                sx={{ 
                  display: { xs: 'none', sm: 'block' },
                  lineHeight: 1.1,
                  opacity: 0.8
                }}
              >
                {description}
              </Typography>
            )}
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}