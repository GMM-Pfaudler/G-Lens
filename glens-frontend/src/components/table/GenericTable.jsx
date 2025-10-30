// components/GenericTable.jsx
import React from "react";
import { 
  Table, 
  TableHead, 
  TableRow, 
  TableCell, 
  TableBody,
  TableContainer,
  Typography,
  Box
} from "@mui/material";
import CellRenderer from "./CellRenderer";

const GenericTable = ({ 
  data, 
  columns, 
  title,
  stickyHeader = true 
}) => {
  if (!data || data.length === 0) {
    return (
      <Typography color="text.secondary" sx={{ textAlign: 'center', py: 4 }}>
        No data available
      </Typography>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {title && (
        <Typography variant="subtitle1" sx={{ fontWeight: "bold", mb: 1, color: 'primary.main', flexShrink: 0 }}>
          {title}
        </Typography>
      )}
      <TableContainer sx={{ flex: 1, overflow: 'auto' }}>
        <Table size="small" sx={{ border: "1px solid #e0e0e0" }} stickyHeader={stickyHeader}>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell key={column.key} sx={{ fontWeight: "bold", backgroundColor: '#f5f5f5' }}>
                  {column.label}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row, index) => (
              <TableRow key={index}>
                {columns.map((column) => (
                  <TableCell key={column.key}>
                    <CellRenderer value={row[column.key]} />
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default GenericTable;