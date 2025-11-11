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
  Tooltip
} from "@mui/material";
import { 
  CheckCircle, 
  Cancel
} from "@mui/icons-material";

const ComparisonReportViewer = ({ data }) => {
  console.log("🧩 Received data in ComparisonReportViewer:", data);

  if (!data || data.length === 0) {
    return (
      <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, textAlign: 'center' }}>
        <Typography color="text.secondary">No comparison data available</Typography>
      </Paper>
    );
  }

  const getStatusIcon = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") {
      return <CheckCircle color="success" fontSize="small" />;
    } else {
      return <Cancel color="error" fontSize="small" />;
    }
  };

  const getStatusText = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") return "Matched";
    return "Not Matched";
  };

  const getStatusColor = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") return "success";
    return "error";
  };

  const formatKeyDisplay = (key) => {
    if (!key) return '';
    
    const parts = key.split(' -> ');
    
    // Single part
    if (parts.length === 1) {
      return (
        <Typography variant="body2" fontWeight="medium">
          {parts[0]}
        </Typography>
      );
    }
    
    // Two parts: "Section -> Field" becomes "Field (Section)"
    if (parts.length === 2) {
      return (
        <Typography variant="body2">
          <Box component="span" fontWeight="medium">
            {parts[1]}
          </Box>
          <Box component="span" sx={{ color: 'text.secondary', fontSize: '0.75rem', ml: 0.5 }}>
            ({parts[0]})
          </Box>
        </Typography>
      );
    }
    
    // Three parts: "Section -> Subsection -> Field" becomes "Subsection (Field)"
    if (parts.length === 3) {
      return (
        <Typography variant="body2">
          <Box component="span" fontWeight="medium">
            {parts[1]}
          </Box>
          <Box component="span" sx={{ color: 'text.secondary', fontSize: '0.75rem', ml: 0.5 }}>
            ({parts[2]})
          </Box>
        </Typography>
      );
    }
    
    // More than three parts: "A -> B -> C -> D" becomes "C (B D)"
    if (parts.length > 3) {
      const field = parts[parts.length - 1];
      const subsection = parts[parts.length - 2];
      const parent = parts[parts.length - 3];
      
      return (
        <Typography variant="body2">
          <Box component="span" fontWeight="medium">
            {subsection}
          </Box>
          <Box component="span" sx={{ color: 'text.secondary', fontSize: '0.75rem', ml: 0.5 }}>
            ({parent} {field})
          </Box>
        </Typography>
      );
    }
    
    return '';
  };

  return (
    <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, borderColor: 'primary.light' }}>
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: "bold", color: 'primary.main' }}>
          Comparison Report
        </Typography>
        <Chip 
          label={`${data.length} items`} 
          size="small" 
          color="primary"
          variant="outlined"
        />
      </Box>

      <Box sx={{ maxHeight: 570, overflowY: "auto" }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Key</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Standard GA Value</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Compared GA Value</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((item, idx) => {
              let parsedAnswer = {};
              try {
                parsedAnswer =
                  typeof item.answer === "string"
                    ? JSON.parse(item.answer)
                    : item.answer || {};
              } catch {
                parsedAnswer = {};
              }

              const matched = parsedAnswer.matched === "Yes";
              // Show closest_match when matched is "No", otherwise show matched_value
              const comparedValue = matched 
                ? parsedAnswer.matched_value 
                : parsedAnswer.closest_match || "N/A";

              return (
                <TableRow key={idx}>
                  <TableCell sx={{ fontWeight: 'medium' }}>
                    {formatKeyDisplay(item.display_key || "Unnamed Key")}
                  </TableCell>
                  <TableCell>
                    {item.display_value || "N/A"}
                  </TableCell>
                  <TableCell>
                    {comparedValue}
                  </TableCell>
                  <TableCell>
                    <Tooltip title={getStatusText(matched)} arrow>
                      <Chip 
                        icon={getStatusIcon(matched)}
                        label={getStatusText(matched)}
                        size="small"
                        color={getStatusColor(matched)}
                        variant="filled"
                        sx={{ fontWeight: 'medium' }}
                      />
                    </Tooltip>
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </Box>
    </Paper>
  );
};

export default ComparisonReportViewer;