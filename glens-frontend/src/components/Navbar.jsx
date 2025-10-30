import { useState } from "react";
import { AppBar, Toolbar, Typography, Box, Menu, MenuItem, Drawer, IconButton,List, ListItem,ListItemText} from "@mui/material";
import gmmLogo from "../assets/gmmLogo.png";
import { useNavigate } from "react-router-dom";
import ConfirmDialog from "./ConfirmDialog";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import { useLocation } from "react-router-dom";
import MenuIcon from "@mui/icons-material/Menu";
import CloseIcon from "@mui/icons-material/Close";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const toggleMobileDrawer = (open) => () => setMobileOpen(open);
  const [confirmOpen, setConfirmOpen] = useState(false);

  // Active page conditions
  const isHomeActive = location.pathname === "/dashboard" || location.pathname === "/";
  const isOperationsActive = [
    "/ofn-ga-comparison",
    "/ga-ga-comparison", 
    "/full-bom-comparison",
    "/model-bom-comparison",
    "/ga-vs-ga-pixel"
  ].some(route => location.pathname.includes(route));

  // Operations menu
  const [anchorEl, setAnchorEl] = useState(null);
  const openMenu = Boolean(anchorEl);

  const handleMenuClick = (event) => setAnchorEl(event.currentTarget);
  const handleMenuClose = () => setAnchorEl(null);
  const handleNavigate = (path) => {
    navigate(path);
    handleMenuClose();
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <>
      <AppBar
        position="static"
        sx={{
          backgroundColor: "#b3d1eb",
          color: "#0e2980",
          height: "88px",
          justifyContent: "center",
          boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
          transition: "all 0.3s ease-in-out", // Smooth transitions for entire navbar
        }}
      >
        <Toolbar sx={{ position: "relative", height: "100%" }}>
          {/* Logo left with hover animation */}
          <Box 
            sx={{ 
              display: "flex", 
              alignItems: "center", 
              height: "100%",
              transition: "transform 0.3s ease",
              "&:hover": {
                transform: "scale(1.05)",
              }
            }}
          >
            <img 
              src={gmmLogo} 
              alt="Logo" 
              style={{ 
                height: "70%", 
                width: "auto",
                transition: "transform 0.3s ease",
                cursor: "pointer"
              }}
              onClick={() => navigate("/dashboard")}
            />
          </Box>

          {/* Title center */}
          <Typography
            variant="h5"
            component="div"
            sx={{
              fontWeight: "bold",
              fontSize: "1.75rem",
              position: "absolute",
              left: "50%",
              top: "50%",
              transform: "translate(-50%, -50%)",
              transition: "all 0.3s ease",
              display: { xs: "none", md: "block" }, 
              "&:hover": {
                textShadow: "0 0 10px rgba(14, 41, 128, 0.3)",
              }
            }}
          >
            AI Powered GL Drawing Verification
          </Typography>

          <IconButton
            edge="start"
            sx={{ display: { xs: "flex", md: "none" }, marginLeft: "auto" }}
            onClick={toggleMobileDrawer(true)}
          >
            <MenuIcon />
          </IconButton>

          {/* Nav links + Logout right */}
          <Box sx={{ marginLeft: "auto", alignItems: "center", gap: 3,display: { xs: "none", md: "flex" } }}>
            <Typography
              variant="body1"
              sx={{ 
                cursor: "pointer", 
                fontWeight: isHomeActive ? 700 : 600, // Bold when active
                padding: "8px 16px",
                backgroundColor: isHomeActive ? "rgba(255, 255, 255, 0.3)" : "transparent",
                borderLeft: isHomeActive ? "4px solid #0e2980" : "4px solid transparent",
                borderRadius: "8px",
                transition: "all 0.3s ease",
                "&:hover": {
                  backgroundColor: isHomeActive ? "rgba(255, 255, 255, 0.4)" : "rgba(255, 255, 255, 0.2)",
                  transform: "translateY(-2px)",
                  boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
                }
              }}
              onClick={() => navigate("/dashboard")}
            >
              Home
            </Typography>

            <Typography
              variant="body1"
              sx={{ 
                cursor: "pointer", 
                display: "flex", 
                alignItems: "center", 
                gap: 0.5, 
                fontWeight: isOperationsActive ? 700 : 600,
                padding: "8px 16px",
                backgroundColor: isOperationsActive ? "rgba(255, 255, 255, 0.3)" : "transparent",
                borderLeft: isOperationsActive ? "4px solid #0e2980" : "4px solid transparent",
                borderRadius: "8px",
                transition: "all 0.3s ease",
                "&:hover": {
                  backgroundColor: isOperationsActive ? "rgba(255, 255, 255, 0.4)" : "rgba(255, 255, 255, 0.2)",
                  transform: "translateY(-2px)",
                  boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)",
                  "& .MuiSvgIcon-root": {
                    transform: "rotate(180deg)",
                  }
                }
              }}
              onClick={handleMenuClick}
            >
              Operations <ArrowDropDownIcon 
                fontSize="small" 
                sx={{ transition: "transform 0.3s ease" }}
              />
            </Typography>

            <Menu 
              anchorEl={anchorEl} 
              open={openMenu} 
              onClose={handleMenuClose}
              sx={{
                "& .MuiPaper-root": {
                  borderRadius: "12px",
                  marginTop: "8px",
                  boxShadow: "0 10px 30px rgba(0, 0, 0, 0.15)",
                  transition: "all 0.3s ease",
                }
              }}
            >
              {[
                { path: "/ofn-ga-comparison", label: "OFN vs GA" },
                { path: "/ga-ga-comparison", label: "GA vs GA" },
                { path: "/full-bom-comparison", label: "Excel BOM vs Excel BOM" },
                { path: "/model-bom-comparison", label: "Excel BOM vs Model BOM" },
                { path: "/ga-vs-ga-pixel", label: "GA vs GA (Pixel)" },
              ].map((item) => (
                <MenuItem 
                  key={item.path}
                  onClick={() => handleNavigate(item.path)}
                  sx={{
                    transition: "all 0.2s ease",
                    
                    "&:hover": {
                      backgroundColor: "rgba(179, 209, 235, 0.3)",
                      transform: "translateX(4px)",
                    }
                  }}
                >
                  {item.label}
                </MenuItem>
              ))}
            </Menu>

            <Typography
              variant="body1"
              sx={{ 
                cursor: "pointer", 
                fontWeight: 600, 
                color: "error.main",
                padding: "8px 16px",
                borderRadius: "8px",
                transition: "all 0.3s ease",
                "&:hover": {
                  backgroundColor: "rgba(211, 47, 47, 0.1)",
                  transform: "translateY(-2px)",
                  boxShadow: "0 4px 12px rgba(211, 47, 47, 0.2)",
                }
              }}
              onClick={() => setConfirmOpen(true)}
            >
              Logout
            </Typography>
          </Box>
        </Toolbar>
      </AppBar>
      <Drawer
        anchor="right"
        open={mobileOpen}
        onClose={toggleMobileDrawer(false)}
        sx={{ 
          "& .MuiDrawer-paper": { 
            width: 280,
            backgroundColor: "#b3d1eb",
          } 
        }}
      >
        <Box sx={{ p: 2, borderBottom: "1px solid rgba(14, 41, 128, 0.1)" }}>
          <Typography variant="h6" fontWeight="bold" color="#0e2980">
            Menu
          </Typography>
            </Box>
            <List>
              <ListItem button onClick={() => { navigate("/dashboard"); setMobileOpen(false); }}
                sx={{
                  backgroundColor: isHomeActive ? "rgba(255, 255, 255, 0.3)" : "transparent",
                  borderLeft: isHomeActive ? "4px solid #0e2980" : "none",
                }}>
                <ListItemText primary="Home" />
              </ListItem>
              <ListItem button onClick={() => { handleNavigate("/ofn-ga-comparison"); setMobileOpen(false); }}>
                <ListItemText primary="OFN vs GA" />
              </ListItem>
              <ListItem button onClick={() => { handleNavigate("/ga-ga-comparison"); setMobileOpen(false); }}>
                <ListItemText primary="GA vs GA" />
              </ListItem>
              <ListItem button onClick={() => { handleNavigate("/full-bom-comparison"); setMobileOpen(false); }}>
                <ListItemText primary="Excel BOM vs Excel BOM" />
              </ListItem>
              <ListItem button onClick={() => { handleNavigate("/model-bom-comparison"); setMobileOpen(false); }}>
                <ListItemText primary="Excel BOM vs Model BOM" />
              </ListItem>
              <ListItem button onClick={() => { handleNavigate("/ga-vs-ga-pixel"); setMobileOpen(false); }}>
                <ListItemText primary="GA vs GA (Pixel)" />
              </ListItem>
              <ListItem button onClick={() => { setConfirmOpen(true); setMobileOpen(false); }}>
                <ListItemText primary="Logout" sx={{ color: "error.main" }} />
              </ListItem>
            </List>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", p: 2, borderBottom: "1px solid rgba(14, 41, 128, 0.1)" }}>
              <Typography variant="h6" fontWeight="bold" color="#0e2980">
                Close
              </Typography>
              <IconButton onClick={toggleMobileDrawer(false)}>
                <CloseIcon />
              </IconButton>
            </Box>
      </Drawer>

      <ConfirmDialog
        open={confirmOpen}
        title="Confirm Logout"
        message="Are you sure you want to logout?"
        onClose={() => setConfirmOpen(false)}
        onConfirm={handleLogout}
        confirmText="Logout"
        cancelText="Cancel"
      />
    </>
  );
}
