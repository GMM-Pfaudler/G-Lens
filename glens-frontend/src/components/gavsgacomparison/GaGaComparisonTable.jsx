import React, { useState, useMemo } from "react";
import { useNavigate } from "react-router-dom";
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
  Card,
  CardContent,
  Stack,
  IconButton,
  Tooltip,
  Paper,
  TableSortLabel,
  TablePagination,
} from "@mui/material";
import {
  Visibility as ViewIcon,
  AccessTime as PendingIcon,
  PlayArrow as RunningIcon,
  CheckCircle as CompletedIcon,
  Error as ErrorIcon,
  Refresh as RefreshIcon,
  ArrowUpward as AscIcon,
  ArrowDownward as DescIcon,
} from "@mui/icons-material";

const statusConfig = {
  pending: {
    color: "warning",
    icon: <PendingIcon fontSize="small" />,
    label: "Pending",
  },
  running: {
    color: "info",
    icon: <RunningIcon fontSize="small" />,
    label: "Running",
  },
  completed: {
    color: "success",
    icon: <CompletedIcon fontSize="small" />,
    label: "Completed",
  },
  error: {
    color: "error",
    icon: <ErrorIcon fontSize="small" />,
    label: "Error",
  },
};

const GAGaComparisonTable = ({ comparisons, loading, onRefresh }) => {
  const [orderBy, setOrderBy] = useState("updated_at");
  const [order, setOrder] = useState("desc");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const navigate = useNavigate();

  const sortedComparisons = useMemo(() => {
    return [...comparisons].sort((a, b) => {
      let aValue = a[orderBy];
      let bValue = b[orderBy];

      if (orderBy === "updated_at" || orderBy === "created_at") {
        aValue = new Date(aValue).getTime();
        bValue = new Date(bValue).getTime();
      }

      if (typeof aValue === "string") {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }

      if (order === "desc") {
        return aValue < bValue ? 1 : aValue > bValue ? -1 : 0;
      } else {
        return aValue > bValue ? 1 : aValue < bValue ? -1 : 0;
      }
    });
  }, [comparisons, orderBy, order]);

  const paginatedComparisons = useMemo(() => {
    const start = page * rowsPerPage;
    const end = start + rowsPerPage;
    return sortedComparisons.slice(start, end);
  }, [sortedComparisons, page, rowsPerPage]);

  const handleSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleChangePage = (event, newPage) => setPage(newPage);
  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleViewResult = (id) => {
    navigate(`/comparison/ga-ga/result/${id}`);
  };

  const formatToIST = (dateString) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    const istOffset = 5.5 * 60 * 60 * 1000;
    const istTime = new Date(date.getTime() + istOffset);
    return istTime.toLocaleString("en-IN", {
      day: "2-digit",
      month: "short",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
        <Stack alignItems="center" spacing={2}>
          <CircularProgress size={40} />
          <Typography color="text.secondary">Loading comparisons...</Typography>
        </Stack>
      </Box>
    );
  }

  if (comparisons.length === 0) {
    return (
      <Card
        variant="outlined"
        sx={{
          background: "linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)",
          border: "1px solid",
          borderColor: "grey.200",
          borderRadius: 2,
        }}
      >
        <CardContent sx={{ textAlign: "center", py: 6 }}>
          <Typography variant="h6" color="grey.600" gutterBottom>
            No Comparisons Found
          </Typography>
          <Typography variant="body2" color="grey.500" mb={2}>
            Start a new comparison to see results here
          </Typography>
          <Button startIcon={<RefreshIcon />} onClick={onRefresh} variant="outlined" size="small">
            Refresh
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Paper
      elevation={0}
      sx={{
        border: "1px solid",
        borderColor: "grey.200",
        borderRadius: 2,
        overflow: "hidden",
      }}
    >
      <Box
        sx={{
          p: 2,
          borderBottom: "1px solid",
          borderColor: "grey.200",
          backgroundColor: "grey.50",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h6" fontWeight="600">
          GA→GA Comparison History ({comparisons.length} total)
        </Typography>
        <Tooltip title="Refresh comparisons">
          <IconButton
            onClick={onRefresh}
            size="small"
            sx={{
              backgroundColor: "white",
              "&:hover": { backgroundColor: "grey.100" },
            }}
          >
            <RefreshIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>

      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow sx={{ backgroundColor: "grey.50" }}>
            <TableCell sx={{ fontWeight: "600", py: 2 }}>GA Files</TableCell>
            <TableCell sx={{ fontWeight: "600", py: 2 }}>Status</TableCell>
            <TableCell sx={{ fontWeight: "600", py: 2 }}>
              <TableSortLabel
                active={orderBy === "updated_at"}
                direction={orderBy === "updated_at" ? order : "asc"}
                onClick={() => handleSort("updated_at")}
                IconComponent={order === "asc" ? AscIcon : DescIcon}
              >
                Last Updated (IST)
              </TableSortLabel>
            </TableCell>
            <TableCell sx={{ fontWeight: "600", py: 2 }} align="center">
              Actions
            </TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {paginatedComparisons.map((comparison) => (
            <TableRow
              key={comparison.id}
              sx={{
                "&:last-child td, &:last-child th": { border: 0 },
                "&:hover": { backgroundColor: "grey.50" },
                transition: "background-color 0.2s ease",
              }}
            >
              <TableCell sx={{ py: 2 }}>
                <Stack spacing={0.5}>
                  <Typography variant="body2" fontWeight="500">
                    GA1: {comparison.ga1_file_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    GA2: {comparison.ga2_file_name}
                  </Typography>
                </Stack>
              </TableCell>

              <TableCell sx={{ py: 2 }}>
                <Chip
                  icon={statusConfig[comparison.status]?.icon}
                  label={statusConfig[comparison.status]?.label || comparison.status}
                  color={statusConfig[comparison.status]?.color || "default"}
                  variant="filled"
                  size="small"
                  sx={{
                    fontWeight: "500",
                    borderRadius: 1,
                  }}
                />
              </TableCell>

              <TableCell sx={{ py: 2 }}>
                <Typography variant="body2">{formatToIST(comparison.updated_at)}</Typography>
                {comparison.status === "running" && (
                  <Typography
                    variant="caption"
                    color="text.secondary"
                    sx={{ fontStyle: "italic" }}
                  >
                    Live updating...
                  </Typography>
                )}
              </TableCell>

              <TableCell sx={{ py: 2 }} align="center">
                <Stack direction="row" spacing={1} justifyContent="center">
                  {comparison.status === "completed" && comparison.comparison_result_path && (
                    <Tooltip title="View Result">
                      <IconButton
                        size="small"
                        onClick={() => handleViewResult(comparison.id)}
                        sx={{
                          backgroundColor: "primary.50",
                          color: "primary.main",
                          "&:hover": {
                            backgroundColor: "primary.100",
                          },
                        }}
                      >
                        <ViewIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  )}

                  {comparison.status === "running" && <CircularProgress size={20} />}

                  {(comparison.status === "pending" || comparison.status === "error") && (
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ fontStyle: "italic" }}
                    >
                      {comparison.status === "error" ? "Failed" : "Waiting..."}
                    </Typography>
                  )}
                </Stack>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25, 50]}
        component="div"
        count={comparisons.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        sx={{
          borderTop: "1px solid",
          borderColor: "grey.200",
        }}
      />
    </Paper>
  );
};

export default GAGaComparisonTable;
