import React, { useState, useMemo, useEffect } from "react";
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
  TextField, // ✅ Search
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
  pending: { color: "warning", icon: <PendingIcon fontSize="small" />, label: "Pending" },
  running: { color: "info", icon: <RunningIcon fontSize="small" />, label: "Running" },
  completed: { color: "success", icon: <CompletedIcon fontSize="small" />, label: "Completed" },
  error: { color: "error", icon: <ErrorIcon fontSize="small" />, label: "Error" },
};

const GAGaComparisonTable = ({ comparisons, loading, onRefresh }) => {
  const role = localStorage.getItem("role");
  const isAdmin = role === "admin";

  const [searchQuery, setSearchQuery] = useState("");
  const [orderBy, setOrderBy] = useState("updated_at");
  const [order, setOrder] = useState("desc");
  const [page, setPage] = useState(0);

  useEffect(() => {
    setPage(0);
  }, [searchQuery]);

  const navigate = useNavigate();

  // Filter comparisons based on search and admin
  const filteredComparisons = useMemo(() => {
    if (!searchQuery.trim()) return comparisons;

    return comparisons.filter((item) => {
      const query = searchQuery.toLowerCase();

      const matchesFiles =
        item.ga1_file_name.toLowerCase().includes(query) ||
        item.ga2_file_name.toLowerCase().includes(query);

      const matchesStatus = item.status.toLowerCase().includes(query);

      const matchesUserId = isAdmin && item.user_id?.toLowerCase().includes(query);

      return matchesFiles || matchesStatus || matchesUserId;
    });
  }, [searchQuery, comparisons, isAdmin]);

  // Sorting
  const sortedComparisons = useMemo(() => {
    return [...filteredComparisons].sort((a, b) => {
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

      return order === "desc" ? (aValue < bValue ? 1 : -1) : aValue > bValue ? 1 : -1;
    });
  }, [filteredComparisons, orderBy, order]);

  // Pagination
  const paginatedComparisons = useMemo(() => {
    const start = page * 5;
    return sortedComparisons.slice(start, start + 5);
  }, [sortedComparisons, page]);

  const handleSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
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
      {/* Header + Search + Refresh */}
      <Box
        sx={{
          p: 2,
          borderBottom: "1px solid",
          borderColor: "grey.200",
          backgroundColor: "grey.50",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 2,
        }}
      >
        <Typography variant="h6" fontWeight="600">
          GA→GA Comparison History ({filteredComparisons.length} results)
        </Typography>

        <Stack direction="row" spacing={1} alignItems="center">
          <TextField
            size="small"
            placeholder={isAdmin ? "Search (files, status, user_id)" : "Search (files, status)"}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ width: 250 }}
          />
          <Tooltip title="Refresh comparisons">
            <IconButton
              onClick={onRefresh}
              size="small"
              sx={{ backgroundColor: "white", "&:hover": { backgroundColor: "grey.100" } }}
            >
              <RefreshIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Stack>
      </Box>

      <Table sx={{ minWidth: 650 }}>
        <TableHead>
          <TableRow sx={{ backgroundColor: "grey.50" }}>
            <TableCell sx={{ fontWeight: "600", py: 2 }}>GA Files</TableCell>
            {isAdmin && <TableCell sx={{ fontWeight: "600", py: 2 }}>User ID</TableCell>}
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
            <TableRow key={comparison.id}>
              <TableCell>
                <Stack spacing={0.5}>
                  <Typography variant="body2" fontWeight="500">
                    GA1: {comparison.ga1_file_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    GA2: {comparison.ga2_file_name}
                  </Typography>
                </Stack>
              </TableCell>

              {isAdmin && <TableCell>{comparison.user_id}</TableCell>}

              <TableCell>
                <Chip
                  icon={statusConfig[comparison.status]?.icon}
                  label={statusConfig[comparison.status]?.label || comparison.status}
                  color={statusConfig[comparison.status]?.color || "default"}
                  size="small"
                />
              </TableCell>

              <TableCell>
                <Typography variant="body2">{formatToIST(comparison.updated_at)}</Typography>
                {comparison.status === "running" && (
                  <Typography variant="caption" color="text.secondary" sx={{ fontStyle: "italic" }}>
                    Live updating...
                  </Typography>
                )}
              </TableCell>

              <TableCell align="center">
                {comparison.status === "completed" && comparison.comparison_result_path && (
                  <Tooltip title="View Result">
                    <IconButton size="small" onClick={() => handleViewResult(comparison.id)}>
                      <ViewIcon fontSize="small" />
                    </IconButton>
                  </Tooltip>
                )}
                {comparison.status === "running" && <CircularProgress size={20} />}
                {(comparison.status === "pending" || comparison.status === "error") && (
                  <Typography variant="body2" color="text.secondary" sx={{ fontStyle: "italic" }}>
                    {comparison.status === "error" ? "Failed" : "Waiting..."}
                  </Typography>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <TablePagination
        component="div"
        count={filteredComparisons.length}
        rowsPerPage={5}
        page={page}
        onPageChange={(e, p) => setPage(p)}
        rowsPerPageOptions={[]}
        sx={{ borderTop: "1px solid", borderColor: "grey.200" }}
      />
    </Paper>
  );
};

export default GAGaComparisonTable;
