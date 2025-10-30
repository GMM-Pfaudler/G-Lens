import React, { useState } from "react";
import { Stepper, Step, StepLabel, Box } from "@mui/material";
import UploadStep from "./steps/UploadStep";
import ComparisonStep from "./steps/ComparisonStep";
import { ComparisonProvider } from "../../../context/ComparisonContext";

const steps = ["Upload PDFs", "Comparison"];

const OfnGaStepper = () => {
  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => setActiveStep((prev) => prev + 1);
  const handleBack = () => setActiveStep((prev) => prev - 1);

  const renderStepContent = () => {
    switch (activeStep) {
      case 0:
        return <UploadStep handleNext={handleNext} />; // combined OFN + GA
      case 1:
        return <ComparisonStep handleBack={handleBack} />;
      default:x
        return null;
    }
  };

  return (
    <ComparisonProvider>
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
    </ComparisonProvider>
  );
};

export default OfnGaStepper;
