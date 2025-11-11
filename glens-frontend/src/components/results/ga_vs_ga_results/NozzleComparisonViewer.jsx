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
  ExpandMore,
  ExpandLess
} from "@mui/icons-material";

const NozzleComparisonViewer = ({ data }) => {
  console.log("🧩 Received nozzle data:", data);

  if (!data || data.length === 0) {
    return (
      <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, textAlign: 'center' }}>
        <Typography color="text.secondary">No nozzle comparison data available</Typography>
      </Paper>
    );
  }

  const [expandedRows, setExpandedRows] = React.useState({});

  const handleExpandClick = (ref) => {
    setExpandedRows(prev => ({
      ...prev,
      [ref]: !prev[ref]
    }));
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "match":
        return <CheckCircle color="success" fontSize="small" />;
      case "mismatch":
        return <Cancel color="error" fontSize="small" />;
      case "missing_in_target":
        return <RemoveCircle color="warning" fontSize="small" />;
      case "extra_in_target":
        return <AddCircle color="info" fontSize="small" />;
      default:
        return <Warning color="warning" fontSize="small" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "match":
        return "Matched";
      case "mismatch":
        return "Mismatched";
      case "missing_in_target":
        return "Missing in Target";
      case "extra_in_target":
        return "Extra in Target";
      default:
        return "Unknown";
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "match":
        return "success";
      case "mismatch":
        return "error";
      case "missing_in_target":
        return "warning";
      case "extra_in_target":
        return "info";
      default:
        return "default";
    }
  };

  const getMatchCount = (nozzle) => {
    if (nozzle.status === "match") {
      return Object.keys(nozzle.full_match_fields || {}).length;
    }
    return Object.keys(nozzle.differences || {}).length;
  };

  const getDetailsTitle = (nozzle) => {
    switch (nozzle.status) {
      case "match":
        return "Matched Fields";
      case "mismatch":
        return "Differences";
      case "missing_in_target":
        return "Missing Fields (Present in Standard, Missing in Target)";
      case "extra_in_target":
        return "Extra Fields (Present in Target, Missing in Standard)";
      default:
        return "Details";
    }
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, borderColor: 'primary.light' }}>
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: "bold", color: 'primary.main' }}>
          Nozzle Comparison Report
        </Typography>
        <Chip 
          label={`${data.length} nozzles`} 
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
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Ref.</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Details Summary</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Field Count</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((nozzle, idx) => {
              const isExpanded = expandedRows[nozzle["ref."]] || false;
              const fieldCount = getMatchCount(nozzle);
              
              return (
                <React.Fragment key={idx}>
                  <TableRow>
                    <TableCell>
                      <IconButton
                        size="small"
                        onClick={() => handleExpandClick(nozzle["ref."])}
                        sx={{ p: 0 }}
                      >
                        {isExpanded ? <ExpandLess /> : <ExpandMore />}
                      </IconButton>
                    </TableCell>
                    <TableCell sx={{ fontWeight: 'medium' }}>
                      {nozzle["ref."]}
                    </TableCell>
                    <TableCell>
                      <Tooltip title={getStatusText(nozzle.status)} arrow>
                        <Chip 
                          icon={getStatusIcon(nozzle.status)}
                          label={getStatusText(nozzle.status)}
                          size="small"
                          color={getStatusColor(nozzle.status)}
                          variant="filled"
                          sx={{ fontWeight: 'medium' }}
                        />
                      </Tooltip>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {nozzle.status === "match" 
                          ? `${fieldCount} fields matched` 
                          : nozzle.status === "mismatch"
                          ? `${fieldCount} differences found`
                          : nozzle.status === "missing_in_target"
                          ? "Nozzle missing in target document"
                          : "Extra nozzle in target document"
                        }
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={`${fieldCount} fields`}
                        size="small"
                        variant="outlined"
                        color="primary"
                      />
                    </TableCell>
                  </TableRow>
                  
                  {/* Expandable details row */}
                  <TableRow>
                    <TableCell colSpan={5} sx={{ p: 0, border: 0 }}>
                      <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                        <Box sx={{ p: 2, backgroundColor: 'grey.50', borderTop: '1px solid', borderColor: 'grey.200' }}>
                          <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                            {getDetailsTitle(nozzle)}
                          </Typography>
                          
                          <Table size="small">
                            <TableHead>
                              <TableRow>
                                <TableCell sx={{ fontWeight: 'bold' }}>Field</TableCell>
                                <TableCell sx={{ fontWeight: 'bold' }}>Standard Value</TableCell>
                                <TableCell sx={{ fontWeight: 'bold' }}>Target Value</TableCell>
                              </TableRow>
                            </TableHead>
                            <TableBody>
                              {nozzle.status === "match" ? (
                                // Show matched fields
                                Object.entries(nozzle.full_match_fields || {}).map(([field, values], fieldIdx) => (
                                  <TableRow key={fieldIdx}>
                                    <TableCell sx={{ fontWeight: 'medium' }}>{field}</TableCell>
                                    <TableCell>{values.standard_value}</TableCell>
                                    <TableCell>{values.target_value}</TableCell>
                                  </TableRow>
                                ))
                              ) : (
                                // Show differences for mismatch, missing, or extra
                                Object.entries(nozzle.differences || {}).map(([field, values], fieldIdx) => (
                                  <TableRow key={fieldIdx}>
                                    <TableCell sx={{ fontWeight: 'medium' }}>{field}</TableCell>
                                    <TableCell>
                                      {values.standard_value !== null ? values.standard_value : (
                                        <Typography variant="body2" color="text.secondary" fontStyle="italic">
                                          Not available
                                        </Typography>
                                      )}
                                    </TableCell>
                                    <TableCell>
                                      {values.target_value !== null ? values.target_value : (
                                        <Typography variant="body2" color="text.secondary" fontStyle="italic">
                                          Not available
                                        </Typography>
                                      )}
                                    </TableCell>
                                  </TableRow>
                                ))
                              )}
                            </TableBody>
                          </Table>
                        </Box>
                      </Collapse>
                    </TableCell>
                  </TableRow>
                </React.Fragment>
              );
            })}
          </TableBody>
        </Table>
      </Box>
    </Paper>
  );
};

export default NozzleComparisonViewer;