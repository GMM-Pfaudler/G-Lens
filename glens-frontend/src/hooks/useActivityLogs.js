import { useState, useEffect } from "react";
import axios from "axios";

/**
 * Custom hook to fetch recent activity logs from the backend.
 * @param {number} limit - Number of recent logs to fetch (default: 6)
 * @returns {Object} { logs, loading, error }
 */
export const useActivityLogs = (limit = 6) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8006";

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      setError(null);

      try {
        const url = `${API_BASE}/activity-log/recent`;
        console.log("Fetching Activity Logs from:", url, "with limit:", limit);

        const response = await axios.get(url, { params: { limit } });

        console.log("Activity Logs API response:", response.data);

        if (response.data && Array.isArray(response.data.logs)) {
          setLogs(response.data.logs);
        } else {
          setLogs([]);
          console.warn("Activity Logs API returned unexpected data format:", response.data);
        }
      } catch (err) {
        console.error("Error fetching activity logs:", err);
        setError(err.response?.data?.detail || err.message || "Failed to fetch logs");
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, [limit]);

  return { logs, loading, error };
};
