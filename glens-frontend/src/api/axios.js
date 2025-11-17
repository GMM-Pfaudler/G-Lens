// src/api/axios.js
import axios from "axios";
import { toast } from "react-toastify";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8006";

const api = axios.create({
  baseURL: API_BASE_URL,
});

let isLoggingOut = false; // prevent multiple redirects

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && !isLoggingOut) {
      isLoggingOut = true;
      console.warn("⛔ Token expired or invalid");

      // Clear storage
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_id");
      localStorage.removeItem("role");

      // Show toast
      toast.error("Your session has expired. Please log in again.", { autoClose: 2000 });

      // Redirect after short delay (to your backend or login route)
      setTimeout(() => {
        window.location.href = `${API_BASE_URL}`;
        isLoggingOut = false;
      }, 3000);
    }
    return Promise.reject(error);
  }
);

export default api;
