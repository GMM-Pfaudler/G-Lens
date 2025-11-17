// import axios from "axios";
import api from "../api/axios";

// const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8006";

export const fetchLiveComparisons = async () => {
  const token = localStorage.getItem("token");

  const response = await api.get(`/api/comparison/ofn-ga/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};
