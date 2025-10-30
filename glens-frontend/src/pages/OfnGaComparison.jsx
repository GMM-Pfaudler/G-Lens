// src/pages/OfnGaComparison.jsx
import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import OfnGaStepper from "../components/stepper/OfnGaStepper/OfnGaStepper"
import { ComparisonProvider } from '../context/ComparisonContext.jsx'
import { Compare } from "@mui/icons-material";

const OfnGaComparison = () => {
  const [ofnResult, setOfnResult] = useState(null);
  const [gaResult, setGaResult] = useState(null);

  return (
    <MainLayout 
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "OFN vs GA", href: "/operations/ofn-vs-ga", active: true }
      ]}
    >
      <ComparisonProvider>
        <OfnGaStepper
          ofnResult={ofnResult}
          setOfnResult={setOfnResult}
          gaResult={gaResult}
          setGaResult={setGaResult}
        />
      </ComparisonProvider>
    </MainLayout>
  );
};

export default OfnGaComparison;
