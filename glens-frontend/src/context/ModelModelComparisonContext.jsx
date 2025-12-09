import React, { createContext, useContext, useState } from "react";

const ModelModelComparisonContext = createContext();

export const ModelModelComparisonProvider = ({ children }) => {
  const [modelAFile, setModelAFile] = useState(null);
  const [modelBFile, setModelBFile] = useState(null);

  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const value = {
    modelAFile, setModelAFile,
    modelBFile, setModelBFile,
    comparisonResult, setComparisonResult,
    loading, setLoading,
  };

  return (
    <ModelModelComparisonContext.Provider value={value}>
      {children}
    </ModelModelComparisonContext.Provider>
  );
};

export const useModelModelComparison = () => useContext(ModelModelComparisonContext);
