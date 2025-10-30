// src/pages/GaGaComparison.jsx
import React from "react";
import MainLayout from "../layouts/MainLayout";
import GaGaStepper from "../components/stepper/GaGaStepper/GaGaStepper";
import { ComparisonProvider } from "../context/ComparisonContext"; // local provider

const GaGaComparison = () => {
  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "GA vs GA", href: "/operations/ga-ga-comparison", active: true }
      ]}
    >
      {/* Wrap only this stepper with its own provider */}
      <ComparisonProvider>
        <GaGaStepper />
      </ComparisonProvider>
    </MainLayout>
  );
};

export default GaGaComparison;
