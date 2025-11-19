import React from "react";
import { Box, Typography, Paper, Container } from "@mui/material";
import { Construction } from "@mui/icons-material";
import MainLayout from "../layouts/MainLayout";

const Documentation = () => {
  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "Documentation", active: true },
      ]}
    >
      <Container maxWidth="sm" sx={{ mt: 8, mb: 8 }}>
        <Paper
          elevation={0}
          sx={{
            p: 6,
            borderRadius: 3,
            textAlign: "center",
            border: "1px solid #e2e8f0",
            background: "linear-gradient(135deg, #f8fafc 0%, #ffffff 100%)",
          }}
        >
          <Construction
            sx={{
              fontSize: 64,
              color: "#b3d1eb",
              mb: 3,
            }}
          />
          
          <Typography 
            variant="h4" 
            sx={{ 
              fontWeight: "bold", 
              mb: 2,
              color: "#0e2980"
            }}
          >
            Documentation Coming Soon
          </Typography>

          <Typography 
            variant="body1" 
            color="text.secondary" 
            sx={{ 
              mb: 4,
              lineHeight: 1.6
            }}
          >
            We're working hard to create comprehensive documentation, 
            user guides, and tutorials for all GLens features.
            <br />
            Check back soon for updates!
          </Typography>

          <Box
            sx={{
              display: "inline-flex",
              alignItems: "center",
              gap: 1,
              px: 3,
              py: 1,
              backgroundColor: "#f0f7ff",
              borderRadius: 2,
              border: "1px solid #b3d1eb"
            }}
          >
            <Box
              sx={{
                width: 8,
                height: 8,
                borderRadius: "50%",
                backgroundColor: "#0e2980",
                animation: "pulse 2s infinite"
              }}
            />
            <Typography variant="body2" sx={{ color: "#0e2980", fontWeight: 500 }}>
              Under Development
            </Typography>
          </Box>
        </Paper>
      </Container>

      <style jsx>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.5; }
          100% { opacity: 1; }
        }
      `}</style>
    </MainLayout>
  );
};

export default Documentation;