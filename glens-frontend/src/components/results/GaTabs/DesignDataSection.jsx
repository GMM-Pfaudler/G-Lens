import React from "react";
import { Box, Typography } from "@mui/material";
import GenericTable from "../../table/GenericTable";

const DesignDataSection = ({ designData }) => {
  if (!Array.isArray(designData) || designData.length === 0) {
    return (
      <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Typography color="text.secondary">No design data available</Typography>
      </Box>
    );
  }

  // Separate the design code (first item) from the rest
  const designCodeItem = designData[0];
  const tableData = designData.slice(1); // All items except the first one

  // Check if the first item is the design code with empty vessel values
  const isDesignCode = designCodeItem?.Parameter?.includes("DESIGN CODE") && 
                      !designCodeItem["INNER VESSEL"] && 
                      !designCodeItem.JACKET;

  // Clean up the design code text by removing \n and extra spaces
  const cleanDesignCode = (text) => {
    if (!text) return '';
    return text
      .replace(/\n/g, ' ') // Replace newlines with spaces
      .replace(/\s+/g, ' ') // Replace multiple spaces with single space
      .replace(/DESIGN CODE : /, '') // Remove "DESIGN CODE : " prefix
      .trim();
  };

  return (
    <Box sx={{ flex: 1, display: "flex", flexDirection: "column", minHeight: 0 }}>
      {/* Design Code Section (if exists) */}
      {isDesignCode && (
        <Box sx={{ flexShrink: 0, mb: 2 }}>
          <Typography 
            variant="subtitle1" 
            sx={{ 
              mb: 1,
              color: 'primary.main',
              fontWeight: 'bold'
            }}
          >
            Design Code
          </Typography>
          <Box sx={{ 
            backgroundColor: 'white',
            p: 2,
            borderRadius: 1,
            border: '1px solid #e0e0e0',
          }}>
            <Typography sx={{ 
              whiteSpace: "pre-wrap", 
              lineHeight: 1.5,
              fontSize: '0.875rem'
            }}>
              {cleanDesignCode(designCodeItem.Parameter)}
            </Typography>
          </Box>
        </Box>
      )}

      {/* Design Parameters Table - Scrollable container */}
      {tableData.length > 0 && (
        <Box sx={{ flex: 1, minHeight: 0, overflow: 'auto' }}>
          <GenericTable
            data={tableData}
            columns={[
              { key: "Parameter", label: "Parameter" },
              { key: "INNER VESSEL", label: "Inner Vessel" },
              { key: "JACKET", label: "Jacket" }
            ]}
            title={isDesignCode ? "Design Parameters" : "Design Data"}
          />
        </Box>
      )}

      {/* If no table data but only design code, show empty state for table */}
      {tableData.length === 0 && isDesignCode && (
        <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Typography color="text.secondary">No design parameters available</Typography>
        </Box>
      )}
    </Box>
  );
};

export default DesignDataSection;