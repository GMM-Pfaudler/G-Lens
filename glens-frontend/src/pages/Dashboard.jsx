import React from "react";
import { Container, Typography, Box, Grid, Paper, Chip, Button } from "@mui/material";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import OperationCard from "../components/OperationCard";
import StatCard from "../components/StatCard";
import ActivityCard from "../components/ActivityCard";
import { useActivityLogs } from "../hooks/useActivityLogs";
import formatUserName from "../utils/formatUserName";

const operations = [
  { 
    label: "OFN vs GA", 
    path: "/ofn-ga-comparison",
    description: "Compare OFN with GA",
    status: "active"
  },
  { 
    label: "GA vs GA", 
    path: "/ga-ga-comparison",
    description: "Version comparison",
    status: "active"
  },
  { 
    label: "BOM Comparison", 
    path: "/full-bom-comparison",
    description: "Dual BOM analysis",
    status: "beta",
    isNew: true
  },
  { 
    label: "Model BOM vs Ref. BOM", 
    path: "/model-bom-comparison",
    description: "Cross-format check",
    status: "active"
  },
  { 
    label: "GA vs GA (Pixel)", 
    path: "/image-comparison",
    description: "Pixel-level analysis",
    status: "beta"
  },
];

const stats = [
  { title: "Pending Comparisons", value: 12 },
  { title: "Completed Comparisons", value: 34 },
  { title: "Alerts / Notifications", value: 5 },
];

const Dashboard = () => {
  const navigate = useNavigate();
  const { logs, loading, error } = useActivityLogs(6); // ✅ fetch 6 logs
  const userId = localStorage.getItem("user_id");
  const displayName = formatUserName(userId);
  console.log("Activity Logs →", logs, "Loading:", loading, "Error:", error);

  return (
    <>
      <Navbar />
      <Container maxWidth="xl" sx={{ py: 4 }}>
        {/* Enhanced Header */}
        <Paper 
          elevation={0}
          sx={{ 
            background: "linear-gradient(135deg, #f8fafc 0%, #ffffff 100%)",
            p: 4, 
            mb: 4,
            borderRadius: 3,
            border: "1px solid #e2e8f0"
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <Box>
              {/* Add welcome message here */}
              <Typography variant="subtitle2" color="primary" sx={{ mb: 1, fontWeight: 'medium' }}>
                Welcome back, {displayName} 👋
              </Typography>
              <Typography variant="h4" sx={{ fontWeight: "bold", mb: 1 }}>
                GL Drawing Verification Portal
              </Typography>
              <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 2 }}>
                Streamline your drawing comparison and verification workflow
              </Typography>
              <Chip 
                label={`${operations.length} verification tools available`} 
                variant="outlined"
                color="primary"
              />
            </Box>
            <Button 
              variant="outlined" 
              size="small"
              onClick={() => navigate('/documentation')}
              sx={{
                '&:hover': {
                  backgroundColor: 'transparent',
                  borderColor: '#2563eb',
                  color: '#2563eb',
                  transform: 'translateY(-1px)',
                  boxShadow: '0 2px 8px rgba(37, 99, 235, 0.2)'
                },
                transition: 'all 0.2s ease'
              }}
            >
              View Guide
            </Button>
          </Box>
        </Paper>

        {/* Main Content Grid */}
        <Grid container spacing={3}> {/* Reduced from 4 to 3 for better spacing */}
          
          {/* Left Column - Operations & Stats */}
          <Grid item xs={12} lg={8}>
            {/* Operations Section */}
            <Paper 
              variant="outlined" 
              sx={{ 
                p: 3, 
                mb: 3, // Reduced from 4 to 3
                borderRadius: 3
              }}
            >
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h5" sx={{ fontWeight: "bold" }}>
                  Available Operations
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {operations.filter(op => op.isNew).length} new
                </Typography>
              </Box>
              
              <Grid container spacing={2}>
                {operations.map((op) => (
                  <Grid item xs={12} sm={6} key={op.path}>
                    <OperationCard 
                      label={op.label}
                      description={op.description}
                      status={op.status}
                      isNew={op.isNew}
                      onClick={() => navigate(op.path)} 
                    />
                  </Grid>
                ))}
              </Grid>
            </Paper>

            {/* Stats Section */}
            <Paper 
              variant="outlined" 
              sx={{ 
                p: 3, 
                borderRadius: 3 
              }}
            >
              <Typography variant="h5" sx={{ fontWeight: "bold", mb: 3 }}>
                Quick Stats
              </Typography>
              <Grid container spacing={2}> {/* Reduced from 3 to 2 */}
                {stats.map((stat, index) => (
                  <Grid item xs={12} sm={4} key={index}>
                    <StatCard 
                      title={stat.title} 
                      value={stat.value} 
                    />
                  </Grid>
                ))}
              </Grid>
            </Paper>
          </Grid>

          {/* Right Column - Recent Activity */}
          <Grid item xs={12} lg={4} sx={{ maxWidth: 330 }}>
            <Paper 
              variant="outlined"
              sx={{ 
                p: 3, 
                position: 'sticky', 
                top: 100,
                height: "100%",
                borderRadius: 3
              }}
            >
              {/* Header */}
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                <Typography variant="h5" sx={{ fontWeight: "bold" }}>
                  Recent Activity
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {logs?.length || 0} items
                </Typography>
              </Box>

              {/* Activity List */}
              <Box sx={{ maxHeight: 470, overflowY: 'auto', pr: 1, pt: 1 }}>
                {loading ? (
                  <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
                    Loading recent activity...
                  </Typography>
                ) : error ? (
                  <Typography variant="body2" color="error" sx={{ textAlign: 'center', py: 4 }}>
                    Failed to load activity logs
                  </Typography>
                ) : logs && logs.length > 0 ? (
                  logs.map((log) => (
                    <ActivityCard
                      key={log.id}
                      title={
                        log.status === "completed"
                          ? "✅ Comparison Completed"
                          : log.status === "started"
                          ? "🚀 Comparison Started"
                          : "ℹ️ Information"
                      }
                      description={log.message}
                      time={new Date(log.created_at).toLocaleString("en-IN", {
                        hour: "2-digit",
                        minute: "2-digit",
                        day: "2-digit",
                        month: "short",
                        year: "numeric",
                      })}
                    />
                  ))
                ) : (
                  <Box sx={{ textAlign: 'center', py: 4 }}>
                    <Typography variant="body2" color="text.secondary">
                      No recent activity
                    </Typography>
                  </Box>
                )}
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </>
  );
};

export default Dashboard; 