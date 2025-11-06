import React, { createContext, useContext, useState } from "react";

const ImageComparisonContext = createContext();

export const ImageComparisonProvider = ({ children }) => {
  const [pdf1, setPdf1] = useState(null);
  const [pdf2, setPdf2] = useState(null);
  const [imageBlob, setImageBlob] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("upload");

  const value = {
    pdf1,
    setPdf1,
    pdf2,
    setPdf2,
    imageBlob,
    setImageBlob,
    loading,
    setLoading,
    activeTab,
    setActiveTab,
  };

  return (
    <ImageComparisonContext.Provider value={value}>
      {children}
    </ImageComparisonContext.Provider>
  );
};

export const useImageComparison = () => useContext(ImageComparisonContext);
