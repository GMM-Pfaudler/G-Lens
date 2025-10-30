import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";

export default function ActivityCard({ title, description, time }) {
  return (
    <Card
      variant="outlined"
      sx={{
        width: "100%",
        minHeight: 88, // Slightly increased for better proportion
        borderRadius: 3,
        borderColor: "#e2e8f0",
        backgroundColor: "#ffffff",
        mb: 2, // Increased from 2 to 2.5 for better separation
        "&:hover": {
          transform: "translateY(-2px)",
          boxShadow: "0 6px 16px rgba(37, 99, 235, 0.1)", // Slightly more pronounced shadow
          borderColor: "#2563eb",
        },
        transition: "all 0.2s ease-in-out", // Smoother transition
      }}
    >
      <CardContent sx={{ p: 2.5 }}> {/* Increased from 2 to 2.5 */}
        <Typography 
          variant="subtitle2" 
          sx={{ 
            fontWeight: 600, 
            mb: 1, // Increased from 0.5 to 1 for better separation
            fontSize: '0.9rem',
            lineHeight: 1.2
          }}
        >
          {title}
        </Typography>
        
        <Typography 
          variant="body2" 
          color="text.secondary"
          sx={{ 
            lineHeight: 1.4, // Slightly increased for better readability
            mb: time ? 1.5 : 0, // Increased from 1 to 1.5 when time is present
            fontSize: '0.8rem'
          }}
        >
          {description}
        </Typography>

        {time && (
          <Typography 
            variant="caption" 
            color="text.secondary"
            sx={{ 
              display: 'block',
              opacity: 0.8 // Slightly subtle for hierarchy
            }}
          >
            {time}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
}