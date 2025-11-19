import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { Box } from "@mui/material";
import PdfSplitHeader from "../components/pdfSplitter/PdfSplitHeader";
import PdfSplitTable from "../components/pdfSplitter/PdfSplitTable";
import PdfUploadModal from "../components/pdfSplitter/PdfUploadModal";
import useLivePdfSplits from "../hooks/useLivePdfSplits";

const PdfSplitter = () => {
  const { splitRecords, loading, reload } = useLivePdfSplits();
  const [uploadModalOpen, setUploadModalOpen] = useState(false);

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "PDF Splitter", active: true },
      ]}
    >
      <Box p={3}>
        <PdfSplitHeader onStart={() => setUploadModalOpen(true)} />

        <PdfSplitTable
          records={splitRecords}
          loading={loading}
          onReload={reload}
        />

        <PdfUploadModal
          open={uploadModalOpen}
          onClose={() => setUploadModalOpen(false)}
          onSuccess={reload}
        />
      </Box>
    </MainLayout>
  );
};

export default PdfSplitter;
