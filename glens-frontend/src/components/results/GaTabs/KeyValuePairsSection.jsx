import React from "react";
import { Box, Typography } from "@mui/material";
import GenericTable from "../../table/GenericTable";

const KeyValuePairsSection = ({ keyValueData }) => {
  // Flatten the nested structure and handle the data
  const formatKeyValueData = () => {
    if (!keyValueData) return [];
    
    // Handle the nested structure where the actual data is inside "KEY-VALUE PAIRS"
    const actualData = keyValueData["KEY-VALUE PAIRS"] || keyValueData;
    
    if (!actualData || typeof actualData !== 'object') return [];
    
    return Object.entries(actualData)
      .filter(([key, value]) => {
        // Filter out keys that are mostly numbers/random characters
        return !isNonsenseKey(key);
      })
      .map(([key, value]) => {
        // Handle nested objects in values (like CORROSION ALLOWANCE)
        let formattedValue = value;
        
        if (value && typeof value === 'object' && !Array.isArray(value)) {
          // Convert nested objects to readable string
          formattedValue = Object.entries(value)
            .map(([nestedKey, nestedValue]) => `${nestedKey}: ${nestedValue}`)
            .join('; ');
        }
        
        return {
          key: formatKeyName(key),
          value: formattedValue
        };
      });
  };

  // Check if key is mostly numbers/random characters (nonsense)
  const isNonsenseKey = (key) => {
    const cleanKey = key.trim();
    
    // If key is mostly numbers, spaces, and random characters
    const numberAndRandomRatio = (cleanKey.match(/[\d\sNWR]/g) || []).length / cleanKey.length;
    
    // Conditions for nonsense keys:
    return (
      // Mostly numbers and random chars (more than 70%)
      numberAndRandomRatio > 0.7 ||
      // Contains specific patterns like "90 425 230..."
      /^\d+(\s+\d+)+$/.test(cleanKey) ||
      // Contains patterns like "N2 N8 N10..."
      /^[NWR]\d+(\s+[NWR]\d+)*$/.test(cleanKey) ||
      // Mixed numbers and N/R/W patterns
      /^(\d+|[NWR]\d+)(\s+(\d+|[NWR]\d+))*$/.test(cleanKey) ||
      // Very long strings of numbers and letters
      cleanKey.length > 50 && numberAndRandomRatio > 0.5
    );
  };

  const formatKeyName = (key) => {
    // Clean up key names - remove extra spaces and format
    return key
      .trim()
      .replace(/\s+/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  const tableData = formatKeyValueData();

  if (tableData.length === 0) {
    return (
      <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Typography color="text.secondary">No specification data available</Typography>
      </Box>
    );
  }

  const columns = [
    { key: "key", label: "Specification" },
    { key: "value", label: "Value" },
  ];

  return (
    <GenericTable
      data={tableData}
      columns={columns}
      title="Technical Specifications"
    />
  );
};

export default KeyValuePairsSection;