import { useState, useEffect } from "react";
import api from "../api/axios";

/**
 * Custom hook to fetch recent activity logs from the backend.
 * @param {number} limit - Number of recent logs to fetch (default: 6)
 * @returns {Object} { logs, loading, error }
 */
export const useActivityLogs = (limit = 6) => {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      setError(null);

      try {
        console.log("Fetching Activity Logs with limit:", limit);

        // ✅ Using the global API instance — automatically handles baseURL + auth header
        const response = await api.get("/activity-log/recent", { params: { limit } });

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
