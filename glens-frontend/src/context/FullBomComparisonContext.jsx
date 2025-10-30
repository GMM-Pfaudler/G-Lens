import React, { createContext, useContext, useState } from "react";

const FullBomComparisonContext = createContext();

export const FullBomComparisonProvider = ({ children }) => {
  const [fileA, setFileA] = useState(null);
  const [fileB, setFileB] = useState(null);
  const [bomLevel, setBomLevel] = useState("1");

  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const value = {
    fileA, setFileA,
    fileB, setFileB,
    bomLevel, setBomLevel,
    comparisonResult, setComparisonResult,
    loading, setLoading,
  };

  return (
    <FullBomComparisonContext.Provider value={value}>
      {children}
    </FullBomComparisonContext.Provider>
  );
};

export const useFullBomComparison = () => useContext(FullBomComparisonContext);
