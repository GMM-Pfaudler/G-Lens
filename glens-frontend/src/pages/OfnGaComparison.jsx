// src/pages/OfnGaComparison.jsx
import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { Box } from "@mui/material";
import { ComparisonProvider } from "../context/ComparisonContext.jsx";
import ComparisonResultHeader from "../components/comparison/ComparisonResultHeader.jsx";
import ComparisonTable from "../components/comparison/ComparisonTable.jsx";
import UploadComparisonModal from "../components/comparison/UploadComparisonModal.jsx";
import useLiveComparisons from "../hooks/useLiveComparisons.js";

const OfnGaComparison = () => {
  const { comparisons, loading, reload } = useLiveComparisons();
  const [uploadModalOpen, setUploadModalOpen] = useState(false);

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "OFN vs GA", href: "/operations/ofn-vs-ga", active: true },
      ]}
    >
      <ComparisonProvider>
        <Box p={3}>
          <ComparisonResultHeader onStart={() => setUploadModalOpen(true)} />
          <ComparisonTable
            comparisons={comparisons}
            loading={loading}
            onReload={reload}
          />
          <UploadComparisonModal
            open={uploadModalOpen}
            onClose={() => setUploadModalOpen(false)}
            onSuccess={reload}
          />
        </Box>
      </ComparisonProvider>
    </MainLayout>
  );
};

export default OfnGaComparison;
