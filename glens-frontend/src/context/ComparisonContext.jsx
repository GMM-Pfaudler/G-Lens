import React, { createContext, useContext, useState } from "react";

// Create the context
const ComparisonContext = createContext();

// Provider component (wraps around your app)
export const ComparisonProvider = ({ children }) => {
  // --- OFN States ---
  const [ofnFile, setOfnFile] = useState(null);
  const [ofnResult, setOfnResult] = useState(null);
  const [ofnExtracted, setOfnExtracted] = useState(false);
  const [ofnLoading, setOfnLoading] = useState(false);

  // --- GA States ---
  const [gaFile, setGaFile] = useState(null);
  const [gaResult, setGaResult] = useState(null);
  const [gaJobId, setGaJobId] = useState(null);
  const [gaExtracted, setGaExtracted] = useState(false);

  // First GA
  const [firstGaFile, setFirstGaFile] = useState(null);
  const [firstGaResult, setFirstGaResult] = useState(null);
  const [firstGaJobId, setFirstGaJobId] = useState(null);
  const [firstGaExtracted, setFirstGaExtracted] = useState(false);

  // Second GA
  const [secondGaFile, setSecondGaFile] = useState(null);
  const [secondGaResult, setSecondGaResult] = useState(null);
  const [secondGaJobId, setSecondGaJobId] = useState(null);
  const [secondGaExtracted, setSecondGaExtracted] = useState(false);


  // --- Comparison States ---
  const [comparisonResult, setComparisonResult] = useState(null);
  const [comparisonLoading, setComparisonLoading] = useState(false);
  const [comparisonTab, setComparisonTab] = useState(0);

  // Group everything into a single shared object
  const value = {
    // OFN
    ofnFile, setOfnFile,
    ofnResult, setOfnResult,
    ofnExtracted, setOfnExtracted,
    ofnLoading,setOfnLoading,

    // GA
    gaFile, setGaFile,
    gaResult, setGaResult,
    gaJobId, setGaJobId,
    gaExtracted, setGaExtracted,

    // First GA (GA vs GA)
    firstGaFile, setFirstGaFile,
    firstGaResult, setFirstGaResult,
    firstGaJobId, setFirstGaJobId,
    firstGaExtracted, setFirstGaExtracted,

    // Second GA (GA vs GA)
    secondGaFile, setSecondGaFile,
    secondGaResult, setSecondGaResult,
    secondGaJobId, setSecondGaJobId,
    secondGaExtracted, setSecondGaExtracted,

    // Comparison
    comparisonResult, setComparisonResult,
    comparisonLoading, setComparisonLoading,
    comparisonTab, setComparisonTab,
  };

  return (
    <ComparisonContext.Provider value={value}>
      {children}
    </ComparisonContext.Provider>
  );
};

// Custom hook for using context
export const useComparison = () => useContext(ComparisonContext);
