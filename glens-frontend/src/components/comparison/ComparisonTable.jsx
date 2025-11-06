// src/components/comparison/ComparisonTable.jsx
import React from "react";
import {
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Chip,
  Button,
  Typography,
  CircularProgress,
  Box,
} from "@mui/material";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8006";

const statusColors = {
  pending: "warning",
  running: "info",
  completed: "success",
  error: "error",
};

const ComparisonTable = ({ comparisons, loading }) => {
  if (loading)
    return (
      <Box display="flex" justifyContent="center" mt={4}>
        <CircularProgress />
      </Box>
    );

  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>ID</TableCell>
          <TableCell>OFN File</TableCell>
          <TableCell>GA File</TableCell>
          <TableCell>Status</TableCell>
          <TableCell>Result Path</TableCell>
          <TableCell>Actions</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {comparisons.length === 0 ? (
          <TableRow>
            <TableCell colSpan={6} align="center">
              No comparisons found
            </TableCell>
          </TableRow>
        ) : (
          comparisons.map((c) => (
            <TableRow key={c.id}>
              <TableCell>{c.id}</TableCell>
              <TableCell>{c.ofn_file_name}</TableCell>
              <TableCell>{c.ga_file_name}</TableCell>
              <TableCell>
                <Chip
                  label={c.status}
                  color={statusColors[c.status] || "default"}
                  variant="outlined"
                />
              </TableCell>
              <TableCell>{c.comparison_result_path || "-"}</TableCell>
              <TableCell>
                {c.status === "completed" ? (
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={() =>
                      window.open(`${API_BASE}/api/comparison/ofn-ga/result/${c.id}`, "_blank")
                    }
                  >
                    View Result
                  </Button>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    {c.status === "running" ? "Processing..." : "-"}
                  </Typography>
                )}
              </TableCell>
            </TableRow>
          ))
        )}
      </TableBody>
    </Table>
  );
};

export default ComparisonTable;
