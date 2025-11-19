import React, { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  CircularProgress,
  Button,
  Box,
} from "@mui/material";
import { Download, Visibility } from "@mui/icons-material";
import PdfDownloadModal from "./PdfDownloadModal";

const PdfSplitTable = ({ records = [], loading }) => {
  const [openModal, setOpenModal] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);

  const safeRecords = Array.isArray(records) ? records : [];

  const sortedRecords = useMemo(() => {
    return [...safeRecords].sort((a, b) => {
      const timeA = new Date(a.uploaded_at).getTime();
      const timeB = new Date(b.uploaded_at).getTime();
      return timeB - timeA;
    });
  }, [safeRecords]);

  const handleOpenModal = (row) => {
    setSelectedRecord(row);
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
    setSelectedRecord(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", p: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <>
      <TableContainer
        component={Paper}
        sx={{
          maxHeight: 650,
          overflowY: "auto",
          border: "1px solid #e2e8f0",
          borderRadius: 2,
        }}
      >
        <Table stickyHeader>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f8fafc" }}>#</TableCell>
              <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f8fafc" }}>File Name</TableCell>
              <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f8fafc" }}>Status</TableCell>
              <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f8fafc" }}>Uploaded At</TableCell>
              <TableCell sx={{ fontWeight: "bold", backgroundColor: "#f8fafc" }}>Actions</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {sortedRecords.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center" sx={{ py: 4 }}>
                  <Box sx={{ color: "text.secondary" }}>
                    No records found
                  </Box>
                </TableCell>
              </TableRow>
            ) : (
              sortedRecords.map((row, index) => (
                <TableRow 
                  key={row.id}
                  sx={{ 
                    '&:hover': { 
                      backgroundColor: '#f8fafc' 
                    } 
                  }}
                >
                  <TableCell sx={{ fontWeight: "medium" }}>{index + 1}</TableCell>

                  <TableCell sx={{ 
                    maxWidth: 200,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap"
                  }}>
                    {row.filename}
                  </TableCell>

                  <TableCell>
                    <Chip
                      label={row.status}
                      size="small"
                      color={
                        row.status === "success"
                          ? "success"
                          : row.status === "failed"
                          ? "error"
                          : "warning"
                      }
                      sx={{ 
                        fontWeight: "bold",
                        textTransform: "capitalize"
                      }}
                    />
                  </TableCell>

                  <TableCell>
                    {row.uploaded_at
                      ? new Date(row.uploaded_at + "Z").toLocaleString("en-IN", {
                          timeZone: "Asia/Kolkata",
                          day: "2-digit",
                          month: "short",
                          year: "numeric",
                          hour: "2-digit",
                          minute: "2-digit",
                        })
                      : "-"}
                  </TableCell>

                  <TableCell>
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<Visibility />}
                      onClick={() => handleOpenModal(row)}
                      disabled={!row.files || row.files.length === 0}
                      sx={{
                        borderRadius: 1,
                        textTransform: "none",
                        borderColor: "#0e2980",
                        color: "#0e2980",
                        '&:hover': {
                          backgroundColor: "#f0f7ff",
                          borderColor: "#0e2980"
                        }
                      }}
                    >
                      View Parts
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <PdfDownloadModal
        open={openModal}
        onClose={handleCloseModal}
        record={selectedRecord}
      />
    </>
  );
};

export default PdfSplitTable;