import React, { useState, useRef } from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, LinearProgress, Typography, Box } from "@mui/material";
import axios from "axios";
import { extractOfn } from "../../services/ofnService";

const UploadComparisonModal = ({ open, onClose }) => {
  const API_URL = import.meta.env.VITE_API_URL;

  // Files
  const [ofnFile, setOfnFile] = useState(null);
  const [gaFile, setGaFile] = useState(null);

  // Statuses & results
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [ofnResult, setOfnResult] = useState(null);
  const [gaResult, setGaResult] = useState(null);
  const [gaJobId, setGaJobId] = useState(null);

  // WebSocket refs
  const wsGaRef = useRef(null);
  const wsCompRef = useRef(null);

  /** --- Handlers --- */
  const handleOfnSelect = (e) => setOfnFile(e.target.files[0]);
  const handleGaSelect = (e) => setGaFile(e.target.files[0]);

  const handleExtractOfn = async () => {
    if (!ofnFile) return alert("Select OFN file");
    setLoading(true);
    setMessage("Extracting OFN...");
    try {
      const data = await extractOfn(ofnFile);
      setOfnResult(data);
      setMessage("OFN extracted!");
    } catch {
      setMessage("OFN extraction failed");
    } finally {
      setLoading(false);
    }
  };

  const handleExtractGa = async () => {
    if (!gaFile) return alert("Select GA file");
    setLoading(true);
    setMessage("Uploading GA & extracting...");
    try {
      const formData = new FormData();
      formData.append("file", gaFile);
      const res = await axios.post(`${API_URL}/api/ga/extract`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const jobId = res.data.job_id;
      setGaJobId(jobId);

      // GA WebSocket
      const ws = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/ga/ws/ga/${jobId}`);
      wsGaRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setGaResult((prev) => ({ ...prev, ...data.result }));
        setMessage(`GA: ${data.status}, progress: ${data.progress || 0}%`);
        if (data.status === "error") ws.close();
      };
      ws.onclose = () => console.log("GA WS closed");
    } catch (err) {
      console.error(err);
      setMessage("GA extraction failed");
    } finally {
      setLoading(false);
    }
  };

  const handleStartComparison = async () => {
    if (!ofnResult || !gaResult) return alert("Extract both OFN & GA first");
    setLoading(true);
    setMessage("Starting comparison...");
    try {
      const userId = localStorage.getItem("user_id");
      const formData = new FormData();
      formData.append("ofn_json", new Blob([JSON.stringify(ofnResult)], { type: "application/json" }), "ofn.json");
      formData.append("ga_json", new Blob([JSON.stringify(gaResult)], { type: "application/json" }), "ga.json");

      const res = await axios.post(`${API_URL}/api/comparison/ofn-ga/start?user_id=${userId}`, formData);
      const { job_id } = res.data;

      const ws = new WebSocket(`${API_URL.replace(/^http/, "ws")}/api/comparison/ofn-ga/ws/${job_id}`);
      wsCompRef.current = ws;

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessage(`Comparison: ${data.status}, progress: ${data.progress || 0}%`);
        if (data.status === "completed" || data.status === "error") ws.close();
      };
      ws.onclose = () => console.log("Comparison WS closed");
    } catch (err) {
      console.error(err);
      setMessage("Comparison start failed");
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    wsGaRef.current?.close();
    wsCompRef.current?.close();
    setOfnFile(null);
    setGaFile(null);
    setOfnResult(null);
    setGaResult(null);
    setMessage("");
    setLoading(false);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>OFN vs GA Comparison Debug</DialogTitle>
      <DialogContent>
        <Box mb={2}>
          <input type="file" accept=".pdf" onChange={handleOfnSelect} />
          <Button onClick={handleExtractOfn} disabled={loading || !ofnFile}>Extract OFN</Button>
        </Box>
        <Box mb={2}>
          <input type="file" accept=".pdf" onChange={handleGaSelect} />
          <Button onClick={handleExtractGa} disabled={loading || !gaFile}>Extract GA</Button>
        </Box>
        <Box mb={2}>
          <Button onClick={handleStartComparison} disabled={loading || !ofnResult || !gaResult}>Start Comparison</Button>
        </Box>
        {loading && <LinearProgress />}
        <Typography mt={2}>{message}</Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={loading}>Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default UploadComparisonModal;
