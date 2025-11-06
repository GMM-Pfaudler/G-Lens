import React, { useState,useEffect } from "react";
import { TextField, Button, Container, Typography, Box,Paper } from "@mui/material";
import { Person, Lock, Visibility, VisibilityOff } from "@mui/icons-material";
import { InputAdornment } from "@mui/material";
import { Link } from "@mui/material";
import { useNavigate } from "react-router-dom";
import Logo from "../assets/gmm_Glens.png"
import { Snackbar, Alert } from "@mui/material";

const API_URL = import.meta.env.VITE_API_URL;

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [shake, setShake] = useState(false);
  const [toast, setToast] = useState({
  open: false, 
  severity: "success", // success | error | info | warning
  message: "",});
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => setMessage(""), 3000);
      return () => clearTimeout(timer);
    }
  }, [message]);


  const handleLogin = async () => {
    setIsLoading(true);
    const MIN_DELAY = 700; // ~0.7s for a natural feel
    const startTime = Date.now();

    try {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: username, password }),
      });

      const data = await res.json();
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, MIN_DELAY - elapsed);

      if (res.ok) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("role", data.role);
        localStorage.setItem("user_id", data.user_id);

        setTimeout(() => {
          setToast({
            open: true,
            severity: "success",
            message: "Login successful!",
          });
          navigate("/dashboard");
          setIsLoading(false);
        }, remaining);

      } else {
        setTimeout(() => {
          setToast({
            open: true,
            severity: "error",
            message: data.detail || "Login failed",
          });
          setIsLoading(false);
          setShake(true);
          setTimeout(() => setShake(false), 500);
        }, remaining);
      }

    } catch (error) {
      console.error(error);
      const elapsed = Date.now() - startTime;
      const remaining = Math.max(0, MIN_DELAY - elapsed);

      setTimeout(() => {
        setToast({
          open: true,
          severity: "error",
          message: "Something went wrong",
        });
        setIsLoading(false);
      }, remaining);
    }
  };

  // Keep this function as-is
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };


return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-blue-50 py-8 px-4" style={{
    // background: "linear-gradient(-45deg, #f0f9ff, #dbeafe, #bfdbfe, #93c5fd)",
    // background: "linear-gradient(-45deg, #fef3c7, #fed7aa, #fecaca, #ddd6fe, #bfdbfe, #a7f3d0, #d9f99d)",
    // background: "linear-gradient(-45deg, #0f172a, #1e293b, #334155, #475569)",
    // background: "linear-gradient(-45deg, #0369a1, #0c4a6e, #1e40af, #3730a3)",
    // background: "linear-gradient(-45deg, #1e3a8a, #1e40af, #312e81, #3730a3)",
    // background: "linear-gradient(-45deg, #0f172a, #1e293b, #334155, #475569)",
    background: "linear-gradient(-45deg, #667eea, #764ba2, #4f46e5, #06b6d4)", //Ocean Blue Gradient
    // background: "linear-gradient(-45deg, #f093fb, #f5576c, #dc2626, #ea580c)",  // Sunset warmth
    // background: "linear-gradient(-45deg, #4facfe, #00f2fe, #059669, #10b981)", // Forest Green
    // background: "linear-gradient(-45deg, #a78bfa, #c084fc, #db2777, #7c3aed)", // Purple Dream
    // background: "linear-gradient(-45deg, #ff9a9e, #fecfef, #d97706, #f59e0b)", //Golder hour
    // background: "linear-gradient(-45deg, #0f172a, #1e293b, #6366f1, #8b5cf6)", // Deep space
    // background: "linear-gradient(-45deg, #ff6b6b, #ffa8a8, #4ecdc4, #45b7d1)", // Coral Reef
    // background: "linear-gradient(-45deg, #a8e6cf, #dcedc1, #ffd3b6, #ffaaa5)", // Berry Smoothie
    // background: "linear-gradient(-45deg, #ff0080, #ff8c00, #40e0d0, #9370db)", // Electric Neon
    backgroundSize: "400% 400%",
    animation: "gradientMove 30s ease infinite",
  }}>
    {/* Particles */}
      {Array.from({ length: 30 }).map((_, i) => {
        const size = 2 + Math.random() * 3; // particle size
        const top = Math.random() * (100 - (size / window.innerHeight) * 100);
        const left = Math.random() * (100 - (size / window.innerWidth) * 100);
        const duration = 4 + Math.random() * 6; // animation duration
        const delay = Math.random() * 5; // animation delay

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              width: `${size}px`,
              height: `${size}px`,
              top: `${Math.min(top, 95)}%`,
              left: `${Math.min(left, 95)}%`,
              borderRadius: "50%",
              background: "radial-gradient(circle, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0) 70%)",
              filter: "blur(0.8px)",
              boxShadow: "0 0 6px rgba(255,255,255,0.8)",
              pointerEvents: "none",
              animation: `floatParticle ${duration}s ease-in-out infinite`,
              animationDelay: `${delay}s`,
            }}
          />
        );
      })}

      <Container maxWidth="sm">
        <Paper 
          elevation={12} 
          className={`p-8 rounded-xl shadow-xl border border-gray-100 ${shake ? 'shake-animation' : ''}`}
          sx={{ 
            background: 'rgba(255, 255, 255, 1)',
            backdropFilter: 'blur(10px)',
            borderRadius: '24px', // smooth corners
            border: '1px solid rgba(203, 213, 225, 0.5)', // light subtle border
            boxShadow: `0 20px 40px rgba(0,0,0,0.1),inset 0 1px 0 rgba(255,255,255,0.6),0 0 0 1px rgba(255,255,255,0.2)`, // soft floating shadow
            animation: 'fadeSlideUp 0.6s ease forwards',
            '@keyframes fadeSlideUp': {
              '0%': { opacity: 0, transform: 'translateY(20px)' },
              '100%': { opacity: 1, transform: 'translateY(0)' },
            },
            position: 'relative', // for particles
          }}
        >
          {/* Logo Section */}
          <Box className="flex justify-center mb-6">
            <img 
              src={Logo}
              alt="Company Logo" 
              className="h-28 w-auto transition-transform duration-300 hover:scale-105"
              style={{ animation: "float 3s ease-in-out infinite" }}
            />
          </Box>
          
          <Typography 
            variant="h4" 
            textAlign="center" 
            className="font-bold text-gray-800 mb-2"
            sx={{ 
              fontWeight: 700,
              background: 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}
          >
            Welcome Back
          </Typography>
          
          <Typography 
            variant="body2" 
            textAlign="center" 
            className="text-gray-500 mb-8"
          >Sign in to continue
          </Typography>
          
          <Box
          component="form"
            onSubmit={(e) => {
              e.preventDefault(); // prevents page reload
              handleLogin();
            }}
           sx={{ display: "flex", flexDirection: "column", gap: 2.5, mt:4}}>
            <TextField
            id="username-input"
            placeholder="Enter username"
            required
              label="Username"
              variant="outlined"
              fullWidth
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="username"
              onKeyPress={handleKeyPress}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Person className="text-blue-500" />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '12px',
                  transition: 'all 0.3s ease',
                  '&:hover fieldset': { borderColor: '#3b82f6' },
                  '&.Mui-focused fieldset': {
                    borderColor: '#3b82f6',
                    borderWidth: '2px',
                    boxShadow: '0 0 10px rgba(59, 130, 246, 0.3)',
                  },
                },
                '& label.Mui-focused': {
                  color: '#3b82f6',
                  transition: 'color 0.3s ease',
                },
              }}
              className="mb-2"
            />
            
           <TextField
           id="password-input"
           required
           placeholder="Enter Password"
              label="Password"
              variant="outlined"
              type="password" // keep as password
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyPress={handleKeyPress}
              autoComplete="current-password" // prevents browser autofill icons
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock className="text-blue-500" />
                  </InputAdornment>
                ),
                // Removed endAdornment (manual eye button)
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  borderRadius: '12px',
                  transition: 'all 0.3s ease',
                  '&:hover fieldset': {
                    borderColor: '#3b82f6',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#3b82f6',
                    borderWidth: '2px',
                    boxShadow: '0 0 8px rgba(59, 130, 246, 0.3)',
                  },
                },
                '& label.Mui-focused': { color: '#3b82f6' },
              }}
            />

            <Box className="flex justify-end mt-1">
              <Link 
                href="#" 
                variant="body2" 
                className="text-blue-600 hover:text-blue-800 transition-colors duration-200"
                sx={{ 
                  textDecoration: 'none',
                  '&:hover': {
                    textDecoration: 'underline'
                  }
                }}
              >
                Forgot password?
              </Link>
            </Box>
            
            <Button 
              variant="contained" 
              fullWidth 
              type="submit"
              size="large"
              disabled={isLoading}
              sx={{
                borderRadius: '12px',
                padding: '12px 0',
                fontSize: '1rem',
                fontWeight: 600,
                mt:2,
                textTransform: 'none',
                background: 'linear-gradient(135deg, #3b82f6 0%, #1e40af 100%)',
                boxShadow: '0 4px 6px rgba(37, 99, 235, 0.2)',
                marginTop: '8px',
                '&:hover': {
                  transform: 'scale(1.03)',
                  transition: 'all 0.3s ease',
                  boxShadow: '0 6px 8px rgba(37, 99, 235, 0.3)',
                  background: 'linear-gradient(135deg, #2563eb 0%, #1e3a8a 100%)',
                },
                '&:active': {
                  transform: 'scale(0.96)',
                  transition: 'transform 0.1s ease',
                },
                '&:disabled': {
                  background: 'linear-gradient(135deg, #93c5fd 0%, #60a5fa 100%)',
                }
              }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Signing in...
                </div>
              ) : (
                "Sign In"
              )}
            </Button>
            
            {message && (
              <Typography 
                color={message.includes("successful") ? "success" : "error"} 
                textAlign="center"
                className={`mt-2 p-2 rounded-lg bg-opacity-10 transition-all duration-500 ${
                  message ? "opacity-100" : "opacity-0"
                }`}
                sx={{
                  backgroundColor: message.includes("successful") ? 
                    'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                  fontWeight: 500
                }}
              >
                {message}
              </Typography>
            )}
          </Box>
        </Paper>
      </Container>
      <Snackbar
        open={toast.open}
        autoHideDuration={3000} // 3 seconds
        onClose={() => setToast({ ...toast, open: false })}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert 
          onClose={() => setToast({ ...toast, open: false })} 
          severity={toast.severity} 
          sx={{ width: "100%" }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Login;