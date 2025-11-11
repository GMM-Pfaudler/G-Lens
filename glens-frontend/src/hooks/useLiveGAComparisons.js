// src/hooks/useLiveGAComparisons.js
import { useEffect, useState, useRef } from "react";
import { fetchLiveGAComparisons } from "../services/gaComparisonService";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8006";
const WS_BASE = API_BASE.replace(/^http/, "ws");

export default function useLiveGAComparisons() {
  const [gaComparisons, setGAComparisons] = useState([]);
  const [loading, setLoading] = useState(true);
  const wsConnections = useRef({});
  const comparisonsRef = useRef([]);

  // keep ref updated whenever list changes
  useEffect(() => {
    comparisonsRef.current = gaComparisons;
  }, [gaComparisons]);

  // -------------------------------
  // 🔄 Fetch GA–GA list
  // -------------------------------
  const reload = async () => {
    try {
      setLoading(true);
      const data = await fetchLiveGAComparisons();
      const list = Array.isArray(data)
        ? data
        : data?.items || data?.data || data?.results || [];
      setGAComparisons(list);
      comparisonsRef.current = list;
      return list;
    } catch (err) {
      console.error("❌ Error loading GA–GA comparisons:", err);
      return comparisonsRef.current || [];
    } finally {
      setLoading(false);
    }
  };

  // -------------------------------
  // 🌐 WebSocket connection
  // -------------------------------
  const connectWebSocket = (jobId) => {
    if (!jobId || wsConnections.current[jobId]) return;

    const ws = new WebSocket(`${WS_BASE}/api/ga-ga-comparison/ws/${jobId}`);
    wsConnections.current[jobId] = ws;

    ws.onopen = () => console.log(`🟢 GA–GA WS connected: ${jobId}`);

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        console.log("📡 GA–GA WS update:", msg);

        setGAComparisons((prev) =>
          prev.map((item) =>
            item.job_id === jobId
              ? {
                  ...item,
                  status: msg.status || item.status,
                  progress:
                    msg.progress !== undefined
                      ? msg.progress
                      : item.progress ?? 0,
                  updated_at: new Date().toISOString(),
                }
              : item
          )
        );

        if (["completed", "error"].includes(msg.status)) reload();
      } catch (e) {
        console.error("⚠️ WS message parse error:", e);
      }
    };

    ws.onerror = (err) => console.error(`⚠️ GA–GA WS error: ${jobId}`, err);

    ws.onclose = () => {
      console.log(`🔴 GA–GA WS closed: ${jobId}`);
      delete wsConnections.current[jobId];
    };
  };

  // -------------------------------
  // 🧩 Initial load
  // -------------------------------
  useEffect(() => {
    reload();
    return () => {
      Object.values(wsConnections.current).forEach((ws) => ws.close());
      wsConnections.current = {};
    };
  }, []);

  // -------------------------------
  // 📡 Auto-connect to active jobs
  // -------------------------------
  useEffect(() => {
    const activeJobs = gaComparisons.filter((c) =>
      ["pending", "running"].includes(c.status)
    );
    activeJobs.forEach((job) => connectWebSocket(job.job_id));
  }, [gaComparisons]);

  // -------------------------------
  // 🔔 SSE: DB updates + pending poll
  // -------------------------------
  useEffect(() => {
    let intervalId = null;

    const startPendingPoll = async () => {
      if (intervalId) return;
      console.log("⏳ GA–GA pending poll (5s)...");
      intervalId = setInterval(async () => {
        try {
          const list = await reload();
          const stillPending = list.some((c) => c.status === "pending");
          if (!stillPending) {
            clearInterval(intervalId);
            intervalId = null;
          }
        } catch (e) {
          console.error("⚠️ Poll error:", e);
        }
      }, 5000);
    };

    const stopPendingPoll = () => {
      if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
      }
    };

    let eventSource;
    try {
      eventSource = new EventSource(`${API_BASE}/api/sse/ga-ga-db-updates`);
      console.log("🟢 GA–GA SSE connected");
    } catch (err) {
      console.error("🔴 GA–GA SSE connection failed:", err);
      eventSource = null;
    }

    if (!eventSource) return () => {};

    eventSource.onmessage = async (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.event === "ga_ga_update") {
          console.log("📡 GA–GA SSE update:", msg.data);
          const list = await reload();
          const hasPending = list.some((c) => c.status === "pending");
          if (hasPending) startPendingPoll();
          else stopPendingPoll();
        }
      } catch (err) {
        console.error("⚠️ SSE parse error:", err);
      }
    };

    eventSource.onerror = (err) => {
      console.error("🔴 SSE error:", err);
      if (eventSource) eventSource.close();
      stopPendingPoll();
    };

    return () => {
      if (eventSource) eventSource.close();
      stopPendingPoll();
    };
  }, []);

  // ✅ Return usable values
  return { gaComparisons, loading, reload };
}
