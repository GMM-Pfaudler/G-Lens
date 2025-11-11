import React from "react";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableRow, 
  Paper, 
  Typography, 
  Box, 
  Chip,
  Tooltip,
  Collapse,
  IconButton
} from "@mui/material";
import { 
  CheckCircle, 
  Cancel,
  Warning,
  AddCircle,
  RemoveCircle,
  SwapHoriz,
  ExpandMore,
  ExpandLess
} from "@mui/icons-material";

const PartListComparisonViewer = ({ data }) => {
  console.log("🧩 Received part list data:", data);

  if (!data || data.length === 0) {
    return (
      <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, textAlign: 'center' }}>
        <Typography color="text.secondary">No part list comparison data available</Typography>
      </Paper>
    );
  }

  const [expandedRows, setExpandedRows] = React.useState({});

  const handleExpandClick = (drawingNo) => {
    setExpandedRows(prev => ({
      ...prev,
      [drawingNo]: !prev[drawingNo]
    }));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "match":
        return <CheckCircle color="success" fontSize="small" />;
      case "qty_mismatch":
      case "mismatch":
        return <Cancel color="error" fontSize="small" />;
      case "missing_in_target":
        return <RemoveCircle color="warning" fontSize="small" />;
      case "extra_in_target":
        return <AddCircle color="info" fontSize="small" />;
      case "possibly_replaced_by":
        return <SwapHoriz color="warning" fontSize="small" />;
      default:
        return <Warning color="warning" fontSize="small" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "match":
        return "Matched";
      case "qty_mismatch":
        return "Quantity Mismatch";
      case "mismatch":
        return "Mismatched";
      case "missing_in_target":
        return "Missing in Target";
      case "extra_in_target":
        return "Extra in Target";
      case "possibly_replaced_by":
        return "Possibly Replaced";
      default:
        return "Unknown";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "match":
        return "success";
      case "qty_mismatch":
      case "mismatch":
        return "error";
      case "missing_in_target":
        return "warning";
      case "extra_in_target":
        return "info";
      case "possibly_replaced_by":
        return "warning";
      default:
        return "default";
    }
  };

  const getSummaryText = (part) => {
    switch (part.status) {
      case "match":
        return "Part matches exactly";
      case "qty_mismatch":
        return "Quantity differs between documents";
      case "mismatch":
        return "Part has differences";
      case "missing_in_target":
        return "Part missing in target document";
      case "extra_in_target":
        return "Extra part in target document";
      case "possibly_replaced_by":
        return "Part possibly replaced by different drawing";
      default:
        return "Unknown status";
    }
  };

  const shouldShowExpand = (part) => {
    return part.status === "possibly_replaced_by" || 
           part.status === "qty_mismatch" || 
           part.status === "mismatch";
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, borderColor: 'primary.light' }}>
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: "bold", color: 'primary.main' }}>
          Part List Comparison Report
        </Typography>
        <Chip 
          label={`${data.length} parts`} 
          size="small" 
          color="primary"
          variant="outlined"
        />
      </Box>

      <Box sx={{ maxHeight: 570, overflowY: "auto" }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100', width: '60px' }}></TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Drawing No.</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Description</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Qty (Std)</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Qty (Target)</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((part, idx) => {
              const isExpanded = expandedRows[part.drawing_no] || false;
              const showExpand = shouldShowExpand(part);
              
              return (
                <React.Fragment key={idx}>
                  <TableRow>
                    <TableCell>
                      {showExpand && (
                        <IconButton
                          size="small"
                          onClick={() => handleExpandClick(part.drawing_no)}
                          sx={{ p: 0 }}
                        >
                          {isExpanded ? <ExpandLess /> : <ExpandMore />}
                        </IconButton>
                      )}
                    </TableCell>
                    <TableCell sx={{ fontWeight: 'medium' }}>
                      {part.drawing_no}
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {part.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={part.standard_qty || "N/A"}
                        size="small"
                        variant="outlined"
                        color={part.standard_qty ? "primary" : "default"}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={part.target_qty || "N/A"}
                        size="small"
                        variant="outlined"
                        color={part.target_qty ? "primary" : "default"}
                      />
                    </TableCell>
                    <TableCell>
                      <Tooltip title={getSummaryText(part)} arrow>
                        <Chip 
                          icon={getStatusIcon(part.status)}
                          label={getStatusText(part.status)}
                          size="small"
                          color={getStatusColor(part.status)}
                          variant="filled"
                          sx={{ fontWeight: 'medium' }}
                        />
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                  
                  {/* Expandable details */}
                  {showExpand && (
                    <TableRow>
                      <TableCell colSpan={6} sx={{ p: 0, border: 0 }}>
                        <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                          <Box sx={{ p: 2, backgroundColor: 'grey.50', borderTop: '1px solid', borderColor: 'grey.200' }}>
                            <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                              {part.status === "possibly_replaced_by" 
                                ? "Replacement Candidate" 
                                : part.status === "qty_mismatch"
                                ? "Quantity Mismatch Details"
                                : "Difference Details"
                              }
                            </Typography>
                            
                            {part.status === "possibly_replaced_by" && part.replacement_candidate ? (
                              <Table size="small">
                                <TableHead>
                                  <TableRow>
                                    <TableCell sx={{ fontWeight: 'bold' }}>Type</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold' }}>Drawing No.</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold' }}>Description</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold' }}>Quantity</TableCell>
                                  </TableRow>
                                </TableHead>
                                <TableBody>
                                  <TableRow>
                                    <TableCell sx={{ fontWeight: 'medium' }}>Original Part</TableCell>
                                    <TableCell>{part.drawing_no}</TableCell>
                                    <TableCell>{part.description}</TableCell>
                                    <TableCell>
                                      <Chip 
                                        label={part.standard_qty || "N/A"}
                                        size="small"
                                        variant="outlined"
                                      />
                                    </TableCell>
                                  </TableRow>
                                  <TableRow>
                                    <TableCell sx={{ fontWeight: 'medium' }}>Replacement Candidate</TableCell>
                                    <TableCell>{part.replacement_candidate.drawing_no}</TableCell>
                                    <TableCell>{part.replacement_candidate.description}</TableCell>
                                    <TableCell>
                                      <Chip 
                                        label={part.target_qty || "N/A"}
                                        size="small"
                                        variant="outlined"
                                      />
                                    </TableCell>
                                  </TableRow>
                                </TableBody>
                              </Table>
                            ) : (part.status === "qty_mismatch" || part.status === "mismatch") ? (
                              <Box>
                                <Typography variant="body2" sx={{ mb: 1 }}>
                                  <strong>Standard Document:</strong> {part.standard_qty} units
                                </Typography>
                                <Typography variant="body2">
                                  <strong>Target Document:</strong> {part.target_qty} units
                                </Typography>
                                {part.status === "qty_mismatch" && (
                                  <Typography variant="body2" color="error" sx={{ mt: 1, fontStyle: 'italic' }}>
                                    Quantity differs between documents
                                  </Typography>
                                )}
                              </Box>
                            ) : null}
                          </Box>
                        </Collapse>
                      </TableCell>
                    </TableRow>
                  )}
                </React.Fragment>
              );
            })}
          </TableBody>
        </Table>
      </Box>
    </Paper>
  );
};

export default PartListComparisonViewer;