import React from "react";
import { 
  Card, 
  CardContent, 
  Typography, 
  Box 
} from "@mui/material";
import { 
  PendingActions, 
  CheckCircle, 
  Notifications 
} from "@mui/icons-material";

export default function StatCard({ title, value, color }) {
  // Simple icon mapping - consistent with OperationCard approach
  const getIcon = () => {
    switch (title) {
      case "Pending Comparisons":
        return <PendingActions sx={{ fontSize: 40, color: "#f59e0b" }} />;
      case "Completed Comparisons":
        return <CheckCircle sx={{ fontSize: 40, color: "#10b981" }} />;
      case "Alerts / Notifications":
        return <Notifications sx={{ fontSize: 40, color: "#ef4444" }} />;
      default:
        return <Notifications sx={{ fontSize: 40, color: "#2563eb" }} />;
    }
  };

  // Consistent background colors with OperationCard
  const getCardStyle = () => {
    const styles = {
      "Pending Comparisons": {
        bgColor: "#fffbeb", // Light amber
        borderColor: "#f59e0b"
      },
      "Completed Comparisons": {
        bgColor: "#f0fdf4", // Light green
        borderColor: "#10b981"
      },
      "Alerts / Notifications": {
        bgColor: "#fef2f2", // Light red
        borderColor: "#ef4444"
      }
    };

    return styles[title] || {
      bgColor: color || "#f8fafc",
      borderColor: "#2563eb"
    };
  };

  const cardStyle = getCardStyle();

  return (
    <Card
      variant="outlined"
      sx={{
        textAlign: "center",
        borderRadius: 3, // Consistent with OperationCard
        borderColor: "#e2e8f0",
        background: `linear-gradient(135deg, ${cardStyle.bgColor} 0%, #ffffff 100%)`,
        width: { xs: "100%", sm: 180, md: 160 }, // Similar sizing to OperationCard
        height: { xs: 120, sm: 140, md: 160 },
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        "&:hover": {
          transform: "translateY(-4px)", // Consistent hover effect
          boxShadow: "0 8px 24px rgba(0,0,0,0.12)",
          borderColor: cardStyle.borderColor,
        },
        transition: "all 0.3s ease-in-out",
        mx: "auto",
      }}
    >
      <CardContent sx={{ p: 2, width: "100%" }}>
        {/* Icon - consistent sizing approach */}
        <Box sx={{ mb: 1 }}>
          {getIcon()}
        </Box>
        
        {/* Value - prominent display */}
        <Typography 
          variant="h4" 
          sx={{ 
            fontWeight: "bold", 
            color: cardStyle.borderColor,
            mb: 0.5
          }}
        >
          {value}
        </Typography>
        
        {/* Title - consistent typography with OperationCard */}
        <Typography 
          variant="subtitle2" 
          sx={{ 
            fontWeight: 600, 
            color: "text.secondary",
            fontSize: '0.8rem',
            lineHeight: 1.2
          }}
        >
          {title}
        </Typography>
      </CardContent>
    </Card>
  );
}