import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { Box } from "@mui/material";
import { ComparisonProvider } from "../context/ComparisonContext.jsx";
import GaGaResultHeader from "../components/gavsgacomparison/GaGaResultHeader.jsx";
import GAGaComparisonTable from "../components/gavsgacomparison/GaGaComparisonTable.jsx";
import GaVsGaComparisonModal from "../components/gavsgacomparison/GaGaUploadComparisonModal.jsx";
import useLiveGAComparisons from "../hooks/useLiveGAComparisons.js";

const GaGaComparison = () => {
  const { gaComparisons, loading, reload } = useLiveGAComparisons();
  const [uploadModalOpen, setUploadModalOpen] = useState(false);

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "GA vs GA", href: "/operations/ga-ga-comparison", active: true },
      ]}
    >
      <ComparisonProvider>
        <Box p={3}>
          <GaGaResultHeader onStart={() => setUploadModalOpen(true)} />
          <GAGaComparisonTable
            comparisons={gaComparisons}
            loading={loading}
            onReload={reload}
          />
          <GaVsGaComparisonModal
            open={uploadModalOpen}
            onClose={() => setUploadModalOpen(false)}
            onSuccess={reload}
          />
        </Box>
      </ComparisonProvider>
    </MainLayout>
  );
};

export default GaGaComparison;
