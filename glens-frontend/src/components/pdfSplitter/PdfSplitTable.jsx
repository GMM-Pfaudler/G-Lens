import React, { useState } from "react";
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
} from "@mui/material";

import PdfDownloadModal from "./PdfDownloadModal";

const PdfSplitTable = ({ records = [], loading }) => {
  const [openModal, setOpenModal] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "20px" }}>
        <CircularProgress />
      </div>
    );
  }

  const safeRecords = Array.isArray(records) ? records : [];

  const handleOpenModal = (row) => {
    setSelectedRecord(row);
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
    setSelectedRecord(null);
  };

  return (
    <>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>#</TableCell>
              <TableCell>File</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Uploaded</TableCell>
              <TableCell>Download</TableCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {safeRecords.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  No records found.
                </TableCell>
              </TableRow>
            ) : (
              safeRecords.map((row, index) => (
                <TableRow key={row.id}>
                  {/* Serial Number */}
                  <TableCell>{index + 1}</TableCell>

                  <TableCell>{row.filename}</TableCell>

                  <TableCell>
                    <Chip
                      label={row.status}
                      color={
                        row.status === "success"
                          ? "success"
                          : row.status === "failed"
                          ? "error"
                          : "warning"
                      }
                    />
                  </TableCell>

                  <TableCell>
                    {row.uploaded_at
                      ? new Date(row.uploaded_at).toLocaleString()
                      : "-"}
                  </TableCell>

                  <TableCell>
                    <Button
                      variant="contained"
                      size="small"
                      onClick={() => handleOpenModal(row)}
                      disabled={!row.files || row.files.length === 0}
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

      {/* Download Modal */}
      <PdfDownloadModal
        open={openModal}
        onClose={handleCloseModal}
        record={selectedRecord}
      />
    </>
  );
};

export default PdfSplitTable;
