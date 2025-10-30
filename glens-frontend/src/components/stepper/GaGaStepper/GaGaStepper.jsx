// src/components/stepper/GaGaStepper/GaGaStepper.jsx
import React, { useState } from "react";
import { Stepper, Step, StepLabel, Box } from "@mui/material";
import UploadStep from "./steps/UploadStep"; // GA vs GA upload step
import ComparisonStep from "./steps/ComparisonStep";

const steps = ["Upload GA Files", "Comparison"];

const GaGaStepper = () => {
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return <UploadStep handleNext={handleNext} />; // two GA uploads
      case 1:
        return <ComparisonStep handleBack={handleBack} />;
      default:
        return null;
    }
  };

  return (
    <Box>
      <Stepper activeStep={activeStep} alternativeLabel sx={{ mb: 3 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <Box>{renderStepContent()}</Box>
    </Box>
  );
};

export default GaGaStepper;
