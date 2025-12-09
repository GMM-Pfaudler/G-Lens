import React from "react";
import { Container, Typography, Box, Grid, Paper, Chip, Button } from "@mui/material";
import Navbar from "../components/Navbar";
import { useNavigate } from "react-router-dom";
import OperationCard from "../components/OperationCard";
import StatCard from "../components/StatCard";
import ActivityCard from "../components/ActivityCard";
import { useActivityLogs } from "../hooks/useActivityLogs";
import formatUserName from "../utils/formatUserName";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";

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
    description: "LN BOM vs LN BOM",
    status: "active",
  },
  { 
    label: "Model BOM vs Ref. BOM", 
    path: "/model-bom-comparison",
    description: "3D Model BOM vs LN BOM",
    status: "active"
  },
  { 
    label: "3D BOM Comparison", 
    path: "/3d-bom-comparison",
    description: "3D Model BOM vs 3D Model BOM",
    status: "active",
    isNew: true
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

  // Menu State
  const [menuAnchor, setMenuAnchor] = React.useState(null);
  const openMenu = (e) => setMenuAnchor(e.currentTarget);
  const closeMenu = () => setMenuAnchor(null);

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
          <IconButton
              onClick={openMenu}
              sx={{
                border: "1px solid",
                borderColor: "divider",
                borderRadius: 2,
                padding: "8px",
                backgroundColor: "background.paper",
                boxShadow: "0 1px 3px rgba(0, 0, 0, 0.1)",
                transition: "all 0.3s ease",
                '&:hover': {
                  backgroundColor: '#b3d1eb',
                  borderColor: '#0e2980',
                  transform: 'translateY(-2px)',
                  boxShadow: `
                    0 4px 12px rgba(0, 0, 0, 0.1),
                    0 0 0 1px rgba(14, 41, 128, 0.1)
                  `
                }
              }}
            >
              <MenuIcon 
                sx={{ 
                  color: "#0e2980",
                  fontSize: "1.25rem",
                  transition: "transform 0.3s ease"
                }} 
              />
            </IconButton>

            <Menu
              anchorEl={menuAnchor}
              open={Boolean(menuAnchor)}
              onClose={closeMenu}
              sx={{
                '& .MuiPaper-root': {
                  borderRadius: "12px",
                  marginTop: "8px",
                  boxShadow: "0 10px 30px rgba(0, 0, 0, 0.15)",
                  border: "1px solid",
                  borderColor: "rgba(14, 41, 128, 0.1)",
                  minWidth: 200,
                  overflow: 'visible',
                  '&::before': {
                    content: '""',
                    position: 'absolute',
                    top: -8,
                    right: 14,
                    width: 16,
                    height: 16,
                    backgroundColor: 'background.paper',
                    borderLeft: '1px solid',
                    borderTop: '1px solid',
                    borderColor: "rgba(14, 41, 128, 0.1)",
                    transform: 'rotate(45deg)'
                  }
                }
              }}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            >
              <MenuItem
                onClick={() => {
                  closeMenu();
                  navigate('/documentation');
                }}
                sx={{
                  padding: "12px 16px",
                  transition: "all 0.2s ease",
                  '&:hover': {
                    backgroundColor: "rgba(179, 209, 235, 0.3)",
                    transform: "translateX(4px)",
                  },
                  '&:first-of-type': {
                    borderTopLeftRadius: 8,
                    borderTopRightRadius: 8
                  }
                }}
              >
                📚 View Guide
              </MenuItem>

              <MenuItem
                onClick={() => {
                  closeMenu();
                  navigate('/pdf-splitter');
                }}
                sx={{
                  padding: "12px 16px",
                  transition: "all 0.2s ease",
                  '&:hover': {
                    backgroundColor: "rgba(179, 209, 235, 0.3)",
                    transform: "translateX(4px)",
                  },
                  '&:last-of-type': {
                    borderBottomLeftRadius: 8,
                    borderBottomRightRadius: 8
                  }
                }}
              >
                ✂️ PDF Splitter Tool
              </MenuItem>
            </Menu>
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
          <Grid item xs={12} lg={4} sx={{ maxWidth: 430 }}>
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