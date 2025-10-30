// utils/renderUtils.jsx
import { Box, Typography } from "@mui/material";
import { formatHeader, renderSimpleValue } from "./tableUtils";

export const safeRender = (val) => {
  if (val === null || val === undefined) return "-";
  if (typeof val === "object") {
    return (
      <Box sx={{ pl: 1 }}>
        {Object.entries(val).map(([nestedKey, nestedValue]) => (
          <Typography key={nestedKey} variant="body2" sx={{ fontSize: '0.8rem', lineHeight: 1.4 }}>
            • <b>{formatHeader(nestedKey)}:</b> {renderSimpleValue(nestedValue)}
          </Typography>
        ))}
      </Box>
    );
  }
  return renderSimpleValue(val);
};