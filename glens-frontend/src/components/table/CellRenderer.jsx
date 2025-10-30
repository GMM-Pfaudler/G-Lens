import React from "react";
import { Box, Typography } from "@mui/material";

const CellRenderer = ({ value }) => {
  if (value === null || value === undefined) return "-";
  
  if (typeof value === "object" && !Array.isArray(value)) {
    return (
      <Box sx={{ py: 0.5 }}>
        {formatNestedObject(value)}
      </Box>
    );
  }
  
  return renderSimpleValue(value);
};

const formatNestedObject = (obj, level = 0) => {
  return Object.entries(obj).map(([key, val]) => {
    const formattedKey = formatHeader(key);
    
    if (typeof val === "object" && val !== null && !Array.isArray(val)) {
      return (
        <Box key={key} sx={{ mb: 0.5 }}>
          <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
            {formattedKey}:
          </Typography>
          <Box sx={{ pl: 2, borderLeft: '2px solid #e0e0e0' }}>
            {formatNestedObject(val, level + 1)}
          </Box>
        </Box>
      );
    }
    
    return (
      <Typography key={key} variant="body2" sx={{ mb: 0.5, lineHeight: 1.4 }}>
        <Box component="span" sx={{ fontWeight: 'bold' }}>
          {formattedKey}:
        </Box>
        <Box component="span" sx={{ ml: 1 }}>
          {val}
        </Box>
      </Typography>
    );
  });
};

const renderSimpleValue = (val) => {
  if (val === null || val === undefined) return "-";
  
  if (typeof val === "string" && val.includes('\n')) {
    return (
      <Box>
        {val.split('\n').map((line, i) => (
          <Typography key={i} variant="body2" sx={{ lineHeight: 1.4 }}>
            {line}
          </Typography>
        ))}
      </Box>
    );
  }
  
  return (
    <Typography variant="body2" sx={{ lineHeight: 1.4 }}>
      {String(val)}
    </Typography>
  );
};

const formatHeader = (header) => {
  return header
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/\./g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
    .trim();
};

export default CellRenderer;