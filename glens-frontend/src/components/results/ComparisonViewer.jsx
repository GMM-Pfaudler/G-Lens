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
  Cancel,
  Help
} from "@mui/icons-material";

const ComparisonViewer = ({ data }) => {
  if (!data || !data.comparison_report) 
    return (
      <Paper variant="outlined" sx={{ p: 2, borderRadius: 2, textAlign: 'center' }}>
        <Typography color="text.secondary">No comparison data yet</Typography>
      </Paper>
    );

  const report = data.comparison_report || [];

  const getStatusIcon = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") {
      return <CheckCircle color="success" fontSize="small" />;
    } else if (matched === false || matched === "false" || matched === "No") {
      return <Cancel color="error" fontSize="small" />;
    } else {
      return <Help color="warning" fontSize="small" />;
    }
  };

  const getStatusText = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") return "Matched";
    if (matched === false || matched === "false" || matched === "No") return "Not Matched";
    return "Unknown";
  };

  const getStatusColor = (matched) => {
    if (matched === true || matched === "true" || matched === "Yes") return "success";
    if (matched === false || matched === "false" || matched === "No") return "error";
    return "warning";
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
          label={`${report.length} items`} 
          size="small" 
          color="primary"
          variant="outlined"
        />
      </Box>

      <Box sx={{ maxHeight: 600, overflowY: "auto" }}>
        <Table size="small" stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>OFN Key</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>OFN Value</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>GA Value</TableCell>
              <TableCell sx={{ fontWeight: 'bold', backgroundColor: 'grey.100' }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {report.map((item, idx) => {
              let answer = {};

              // ✅ Safely parse `answer` whether it's string or object
              if (typeof item.answer === "string") {
                try {
                  const jsonStr = item.answer.replace(/'/g, '"');
                  answer = JSON.parse(jsonStr);
                } catch (e) {
                  answer = { matched: "Unknown", matched_value: item.answer };
                }
              } else {
                answer = item.answer || {};
              }

              const matched = answer.matched;
              const gaValue = answer.matched_value || answer.closest_match || "";
              const statusText = getStatusText(matched);
              const statusColor = getStatusColor(matched);

              return (
                <TableRow key={idx}>
                  <TableCell sx={{ fontWeight: 'medium' }}>
                    {formatKeyDisplay(item.display_key || item.key)}
                  </TableCell>
                  <TableCell>
                    {item.display_value || item.expected_value}
                  </TableCell>
                  <TableCell>
                    {gaValue}
                  </TableCell>
                  <TableCell>
                    <Tooltip title={statusText} arrow>
                      <Chip 
                        icon={getStatusIcon(matched)}
                        label={statusText}
                        size="small"
                        color={statusColor}
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

export default ComparisonViewer;