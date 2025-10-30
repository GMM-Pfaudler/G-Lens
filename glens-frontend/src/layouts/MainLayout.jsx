// src/layouts/MainLayout.jsx
import React from "react";
import { 
  Container, 
  Typography, 
  Box, 
  alpha,
  useTheme,
  Breadcrumbs,
  Link
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import HomeIcon from '@mui/icons-material/Home';
import Navbar from "../components/Navbar";

const MainLayout = ({ children, breadcrumbItems }) => {
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();

  // Generate breadcrumbs from current route if not provided
  const generateBreadcrumbs = () => {
    if (breadcrumbItems) return breadcrumbItems;
    
    const paths = location.pathname.split('/').filter(path => path);
    const breadcrumbs = [];
    
    // Add home breadcrumb
    if (paths.length > 0) {
      breadcrumbs.push({
        label: "Home",
        href: "/",
        icon: <HomeIcon sx={{ fontSize: 16 }} />,
        active: false
      });
    }
    
    // Build breadcrumb items from route
    paths.forEach((path, index) => {
      const href = '/' + paths.slice(0, index + 1).join('/');
      const isLast = index === paths.length - 1;
      
      breadcrumbs.push({
        label: path.charAt(0).toUpperCase() + path.slice(1).replace(/-/g, ' '),
        href: href,
        active: isLast
      });
    });
    
    return breadcrumbs;
  };

  const breadcrumbs = generateBreadcrumbs();

  return (
    <>
      <Navbar />
      <Container 
        maxWidth="xl" 
        sx={{ 
          py: 2,
          px: { xs: 2, sm: 3, md: 4 },
          height: 'calc(100vh - 64px)',
          overflow:"hidden"
        }}
      >
        {/* Enhanced Breadcrumb Navigation */}
        {breadcrumbs.length > 0 && (
          <Box sx={{ 
            mb: 2.5,
            position: 'relative',
            overflow:"hidden"
          }}>
            {/* Background with subtle gradient */}
            <Box
              sx={{
                position: 'absolute',
                top: 0,
                left: -16,
                right: -16,
                height: '100%',
                background: `linear-gradient(90deg, ${alpha(theme.palette.primary.main, 0.02)} 0%, transparent 100%)`,
                borderBottom: `1px solid ${alpha(theme.palette.primary.main, 0.08)}`,
                zIndex: 0
              }}
            />
            
            <Breadcrumbs 
              aria-label="breadcrumb"
              separator={<NavigateNextIcon sx={{ fontSize: 16, color: alpha(theme.palette.text.primary, 0.4) }} />}
              sx={{ 
                position: 'relative',
                zIndex: 1,
                py: 1.5,
                px: 2,
                '& .MuiBreadcrumbs-ol': {
                  alignItems: 'center',
                  flexWrap: 'wrap',
                  gap: 0.3
                },
                '& .MuiBreadcrumbs-li': {
                  display: 'flex',
                  alignItems: 'center'
                }
              }}
            >
              {breadcrumbs.map((item, index) => 
                item.active ? (
                  // Current page - most prominent
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 0.5,
                      px: 1.8,
                      py: 0.8,
                      borderRadius: 3,
                      background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                      color: 'white',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      boxShadow: `0 3px 12px ${alpha(theme.palette.primary.main, 0.4)}`,
                      transform: 'scale(1.05)',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    {item.icon}
                    {item.label}
                  </Box>
                ) : (
                  // Clickable breadcrumb items - subtle hover
                  <Link
                    key={index}
                    component="button"
                    underline="none"
                    sx={{ 
                      display: 'flex',
                      alignItems: 'center',
                      gap: 0.5,
                      px: 1.5,
                      py: 0.6,
                      borderRadius: 2,
                      fontSize: '0.82rem',
                      fontWeight: 500,
                      color: theme.palette.text.secondary,
                      background: alpha(theme.palette.primary.main, 0),
                      transition: 'all 0.2s ease',
                      border: `1px solid transparent`,
                      '&:hover': {
                        color: theme.palette.primary.main,
                        background: alpha(theme.palette.primary.main, 0.04),
                        border: `1px solid ${alpha(theme.palette.primary.main, 0.15)}`,
                        // Subtle hover effect - no scaling or major visual changes
                        boxShadow: `0 1px 4px ${alpha(theme.palette.primary.main, 0.1)}`
                      }
                    }}
                    onClick={() => navigate(item.href)}
                  >
                    {item.icon}
                    {item.label}
                  </Link>
                )
              )}
            </Breadcrumbs>

            {/* Progress indicator for deep navigation */}
            {breadcrumbs.length > 2 && (
              <Box sx={{ 
                width: '100%', 
                height: 2, 
                background: alpha(theme.palette.primary.main, 0.08),
                borderRadius: 1,
                mt: 0.5,
                position: 'relative',
                overflow: 'hidden'
              }}>
                <Box 
                  sx={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    height: '100%',
                    width: `${(breadcrumbs.findIndex(item => item.active) / (breadcrumbs.length - 1)) * 100}%`,
                    background: `linear-gradient(90deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.light} 100%)`,
                    borderRadius: 1,
                    transition: 'width 0.3s ease'
                  }}
                />
              </Box>
            )}
          </Box>
        )}

        {/* Page Content */}
        <Box sx={{ 
          '& > *:first-of-type': {
            mt: 0
          },
          overflow: 'auto', 
        }}>
          {children}
        </Box>
      </Container>
    </>
  );
};

export default MainLayout;