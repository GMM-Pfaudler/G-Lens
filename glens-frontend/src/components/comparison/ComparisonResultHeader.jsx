import React from "react";
import { Box, Typography, Chip, Button, Stack } from "@mui/material";
import { AccessTime, CheckCircle, ErrorOutline, Add } from "@mui/icons-material";

const statusColors = {
  pending: "warning",
  running: "info",
  completed: "success",
  error: "error",
};

const ComparisonResultHeader = ({ latestComparison, onViewResult, onStart }) => {
  if (!latestComparison) {
    // If no comparison yet, show only the "Start New Comparison" button
    return (
      <Box
        sx={{
          p: 2,
          mb: 3,
          border: "1px solid",
          borderColor: "grey.300",
          borderRadius: 2,
          backgroundColor: "grey.50",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="subtitle1" fontWeight="bold">
          No comparisons yet
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={onStart}
        >
          Start New Comparison
        </Button>
      </Box>
    );
  }

  const { ofn_file_name, ga_file_name, status, comparison_result_path, updated_at } =
    latestComparison;

  const icon =
    status === "completed" ? (
      <CheckCircle color="success" fontSize="small" />
    ) : status === "error" ? (
      <ErrorOutline color="error" fontSize="small" />
    ) : (
      <AccessTime color="action" fontSize="small" />
    );

  return (
    <Box
      sx={{
        p: 2,
        mb: 3,
        border: "1px solid",
        borderColor: "grey.300",
        borderRadius: 2,
        backgroundColor: "grey.50",
      }}
    >
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="subtitle1" fontWeight="bold">
            Latest Comparison
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {ofn_file_name} ⟶ {ga_file_name}
          </Typography>

          <Stack direction="row" alignItems="center" spacing={1} mt={1}>
            {icon}
            <Chip
              label={status}
              color={statusColors[status] || "default"}
              size="small"
              variant="outlined"
            />
            {updated_at && (
              <Typography variant="caption" color="text.secondary">
                Updated: {new Date(updated_at).toLocaleString()}
              </Typography>
            )}
          </Stack>
        </Box>

        <Stack direction="row" spacing={1}>
          {status === "completed" && comparison_result_path && (
            <Button
              variant="outlined"
              color="primary"
              size="small"
              onClick={() => onViewResult(comparison_result_path)}
            >
              View Result
            </Button>
          )}

          <Button
            variant="contained"
            color="primary"
            size="small"
            startIcon={<Add />}
            onClick={onStart}
          >
            Start New Comparison
          </Button>
        </Stack>
      </Stack>
    </Box>
  );
};

export default ComparisonResultHeader;
