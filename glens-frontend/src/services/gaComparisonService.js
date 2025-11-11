import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8006";

// Fetch GA–GA comparison history list
export const fetchLiveGAComparisons = async () => {
  const response = await axios.get(`${API_BASE_URL}/api/comparison/ga-ga/history`);
  return response.data;
};
