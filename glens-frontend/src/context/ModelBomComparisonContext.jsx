import React, { createContext, useContext, useState } from "react";

const ModelBomComparisonContext = createContext();

export const ModelBomComparisonProvider = ({ children }) => {
  const [modelFile, setModelFile] = useState(null);
  const [refFile, setRefFile] = useState(null);

  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const value = {
    modelFile, setModelFile,
    refFile, setRefFile,
    comparisonResult, setComparisonResult,
    loading, setLoading,
  };

  return (
    <ModelBomComparisonContext.Provider value={value}>
      {children}
    </ModelBomComparisonContext.Provider>
  );
};

export const useModelBomComparison = () => useContext(ModelBomComparisonContext);
