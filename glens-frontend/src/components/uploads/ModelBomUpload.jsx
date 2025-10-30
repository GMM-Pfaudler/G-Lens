import React from "react";
import { useModelBomComparison } from "../../context/ModelBomComparisonContext";

const ModelBomUpload = () => {
  const {
    modelFile,
    setModelFile,
    refFile,
    setRefFile,
    loading,
  } = useModelBomComparison();

  const handleModelFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setModelFile(file);
    }
  };

  const handleRefFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setRefFile(file);
    }
  };

  const clearModelFile = () => {
    setModelFile(null);
    // Clear the file input
    const fileInput = document.getElementById('model-file-input');
    if (fileInput) fileInput.value = '';
  };

  const clearRefFile = () => {
    setRefFile(null);
    // Clear the file input
    const fileInput = document.getElementById('ref-file-input');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="space-y-6">
      {/* File Upload Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Model BOM File Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              Model BOM File <span className="text-red-500">*</span>
            </label>
            {modelFile && (
              <button
                onClick={clearModelFile}
                className="text-red-500 hover:text-red-700 hover:underline text-sm font-medium transition-all duration-200"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="model-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="model-file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleModelFileChange}
                className="hidden"
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {modelFile ? (
                  <div className={`text-green-600 font-medium transition-all duration-300 ${modelFile ? "animate-pulse" : ""}`}>
                    ✓ {modelFile.name}
                  </div>
                ) : (
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      Click to upload
                    </div>
                    <div className="text-xs text-gray-500">
                      .xlsx or .xls files
                    </div>
                  </div>
                )}
              </div>
            </label>
          </div>
        </div>

        {/* Reference BOM File Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              Reference BOM File <span className="text-red-500">*</span>
            </label>
            {refFile && (
              <button
                onClick={clearRefFile}
                className="text-red-500 hover:text-red-700 text-sm font-medium"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="ref-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="ref-file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleRefFileChange}
                className="hidden"
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {refFile ? (
                  <div className="text-green-600 font-medium">
                    ✓ {refFile.name}
                  </div>
                ) : (
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      Click to upload
                    </div>
                    <div className="text-xs text-gray-500">
                      .xlsx or .xls files
                    </div>
                  </div>
                )}
              </div>
            </label>
          </div>
        </div>
      </div>

      {/* Status Indicators */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-blue-700">
            <strong>Ready to compare:</strong>{" "}
            {modelFile && refFile ? (
              <span className="text-green-600">Both files uploaded</span>
            ) : (
              <span className="text-orange-600">Waiting for files</span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm">
            <span className={modelFile ? "text-green-600" : "text-gray-400"}>
              Model BOM: {modelFile ? "✓" : "✗"}
            </span>
            <span className={refFile ? "text-green-600" : "text-gray-400"}>
              Reference BOM: {refFile ? "✓" : "✗"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelBomUpload;