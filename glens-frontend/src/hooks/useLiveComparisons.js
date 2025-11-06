// src/hooks/useLiveComparisons.js
import { useEffect, useState, useRef } from "react";
import { fetchLiveComparisons } from "../services/liveComparisonService";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8006";
const WS_BASE = API_BASE.replace("http", "ws");

export default function useLiveComparisons() {
  const [comparisons, setComparisons] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsConnections = useRef({});

  const reload = async () => {
    try {
      const data = await fetchLiveComparisons();
      const list = Array.isArray(data)
        ? data
        : data?.items || data?.data || data?.results || [];
      setComparisons(list);
    } catch (err) {
      console.error("❌ Error loading data:", err);
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = (jobId) => {
    if (wsConnections.current[jobId]) return;
    const ws = new WebSocket(`${WS_BASE}/ws/${jobId}`);

    ws.onopen = () => console.log(`🟢 WS connected: ${jobId}`);

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        setComparisons((prev) =>
          prev.map((item) =>
            item.job_id === jobId
              ? { ...item, status: msg.status, progress: msg.progress ?? item.progress }
              : item
          )
        );
        if (msg.status === "completed" || msg.status === "error") reload();
      } catch (e) {
        console.error("⚠️ WS message parse error:", e);
      }
    };

    ws.onclose = () => {
      console.log(`🔴 WS closed: ${jobId}`);
      delete wsConnections.current[jobId];
    };

    wsConnections.current[jobId] = ws;
  };

  useEffect(() => {
    reload();
    return () => Object.values(wsConnections.current).forEach((ws) => ws.close());
  }, []);

  useEffect(() => {
    const active = comparisons.filter(
      (c) => c.status === "running" || c.status === "pending"
    );
    active.forEach((job) => job.job_id && connectWebSocket(job.job_id));
  }, [comparisons]);

  return { comparisons, loading, reload };
}
