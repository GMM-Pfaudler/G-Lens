// src/pages/ofn_ga_comparison/ComparisonHistoryPage.jsx
import React, { useEffect, useState } from "react";
import {
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Typography,
  CircularProgress,
  Box,
  IconButton,
  Tooltip,
} from "@mui/material";
import { History, Visibility } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import MainLayout from "../../layouts/MainLayout"; // ✅ Use your main layout

const API_URL = import.meta.env.VITE_API_URL;

const ComparisonHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch(`${API_URL}/api/comparison/ofn-ga/history`);
        if (!res.ok) throw new Error("Failed to fetch history");
        const data = await res.json();
        setHistory(data.items || []);
      } catch (err) {
        console.error("Error fetching comparison history:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  const handleViewResult = (id) => {
    navigate(`/ofn-ga-comparison/result/${id}`);
  };

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "OFN-GA Comparison", href: "/ofn-ga-comparison" },
        { label: "History", active: true },
      ]}
    >
      <div className="p-6 space-y-6">
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
          {/* 🔹 Header */}
          <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
            <History sx={{ mr: 1, color: "primary.main" }} />
            <Typography variant="h5" fontWeight={700}>
              Comparison History
            </Typography>
          </Box>

          {/* 🔹 Content */}
          {loading ? (
            <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
              <CircularProgress />
            </Box>
          ) : history.length === 0 ? (
            <Typography
              align="center"
              color="text.secondary"
              sx={{ py: 8, fontSize: "1.1rem" }}
            >
              No comparison history found.
            </Typography>
          ) : (
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>#</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Job ID</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>OFN File</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>GA File</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Result Date</TableCell>
                  <TableCell sx={{ fontWeight: 600 }} align="center">
                    Action
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {history.map((item, index) => (
                  <TableRow
                    key={item.id}
                    hover
                    sx={{
                      transition: "all 0.2s",
                      "&:hover": { backgroundColor: "action.hover" },
                    }}
                  >
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{item.job_id}</TableCell>
                    <TableCell>{item.ofn_file_name}</TableCell>
                    <TableCell>{item.ga_file_name}</TableCell>
                    <TableCell sx={{ textTransform: "capitalize" }}>
                      {item.status}
                    </TableCell>
                    <TableCell>
                      {new Date(item.result_date).toLocaleString()}
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="View Result">
                        <IconButton
                          color="primary"
                          onClick={() => handleViewResult(item.id)}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </Paper>
      </div>
    </MainLayout>
  );
};

export default ComparisonHistoryPage;
