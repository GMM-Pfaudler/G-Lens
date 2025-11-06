import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  CircularProgress,
  Box,
  Typography,
  Paper,
  Button,
  Divider,
} from "@mui/material";
import { ArrowBack } from "@mui/icons-material";
import ComparisonViewer from "../../components/results/ComparisonViewer";
import MainLayout from "../../layouts/MainLayout";

const API_URL = import.meta.env.VITE_API_URL;

const ComparisonResultPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const res = await fetch(`${API_URL}/api/comparison/ofn-ga/result/${id}`);
        if (!res.ok) throw new Error("Failed to fetch result");
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error("Error fetching comparison result:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchResult();
  }, [id]);

  if (loading) {
    return (
      <MainLayout
        breadcrumbItems={[
          { label: "Dashboard", href: "/dashboard" },
          { label: "OFN-GA Comparison", href: "/ofn-ga-comparison" },
          { label: "Result", active: true },
        ]}
      >
        <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
          <CircularProgress />
        </Box>
      </MainLayout>
    );
  }

  if (!data) {
    return (
      <MainLayout
        breadcrumbItems={[
          { label: "Dashboard", href: "/dashboard" },
          { label: "OFN-GA Comparison", href: "/ofn-ga-comparison" },
          { label: "Result", active: true },
        ]}
      >
        <Typography align="center" color="text.secondary" sx={{ py: 8 }}>
          No comparison data found.
        </Typography>
      </MainLayout>
    );
  }

  const { job_id, ofn_file_name, ga_file_name, status, result_date, result } = data;

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "OFN-GA Comparison", href: "/ofn-ga-comparison" },
        { label: "Result", active: true },
      ]}
    >
      <Paper
        elevation={0}
        sx={{
          p: 4,
          borderRadius: 4,
          background: "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
          border: "1px solid",
          borderColor: "divider",
          boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
        }}
      >
        {/* Header with Back Button */}
        <Box sx={{ display: "flex", alignItems: "center", mb: 2 }}>
          <Button
            startIcon={<ArrowBack />}
            onClick={() => navigate(-1)}
            sx={{ textTransform: "none", fontWeight: 600 }}
          >
            Back
          </Button>
          <Typography variant="h5" fontWeight={700} sx={{ ml: 2 }}>
            Comparison Result
          </Typography>
        </Box>

        {/* Summary Info */}
        <Box sx={{ mb: 2 }}>
          <Typography variant="body1">
            <strong>Job ID:</strong> {job_id}
          </Typography>
          <Typography variant="body1">
            <strong>OFN File:</strong> {ofn_file_name}
          </Typography>
          <Typography variant="body1">
            <strong>GA File:</strong> {ga_file_name}
          </Typography>
          <Typography variant="body1">
            <strong>Status:</strong> {status}
          </Typography>
          <Typography variant="body1">
            <strong>Result Date:</strong>{" "}
            {new Date(result_date).toLocaleString()}
          </Typography>
        </Box>

        <Divider sx={{ my: 2 }} />

        {/* Comparison Viewer */}
        <ComparisonViewer data={result} />
      </Paper>
    </MainLayout>
  );
};

export default ComparisonResultPage;
