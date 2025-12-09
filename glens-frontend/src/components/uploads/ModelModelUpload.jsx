import React from "react";
import { useModelModelComparison } from "../../context/ModelModelComparisonContext";

const ModelModelUpload = () => {
  const {
    modelAFile,
    setModelAFile,
    modelBFile,
    setModelBFile,
    loading,
  } = useModelModelComparison();

  const handleModelAFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setModelAFile(file);
    }
  };

  const handleModelBFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setModelBFile(file);
    }
  };

  const clearModelAFile = () => {
    setModelAFile(null);
    // Clear the file input
    const fileInput = document.getElementById('model-A-file-input');
    if (fileInput) fileInput.value = '';
  };

  const clearModelBFile = () => {
    setModelBFile(null);
    // Clear the file input
    const fileInput = document.getElementById('model-B-file-input');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="space-y-6">
      {/* File Upload Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Model A BOM File Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              Model A BOM File <span className="text-red-500">*</span>
            </label>
            {modelAFile && (
              <button
                onClick={clearModelAFile}
                className="text-red-500 hover:text-red-700 hover:underline text-sm font-medium transition-all duration-200"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="model-A-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="model-A-file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleModelAFileChange}
                className="hidden"
                disabled={loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {modelAFile ? (
                  <div className={`text-green-600 font-medium transition-all duration-300 ${modelAFile ? "animate-pulse" : ""}`}>
                    ✓ {modelAFile.name}
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

        {/* Model B BOM File Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              Model B BOM File <span className="text-red-500">*</span>
            </label>
            {modelBFile && (
              <button
                onClick={clearModelBFile}
                className="text-red-500 hover:text-red-700 text-sm font-medium"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="model-B-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="model-B-file-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleModelBFileChange}
                className="hidden"
                disabled={loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {modelBFile ? (
                  <div className="text-green-600 font-medium">
                    ✓ {modelBFile.name}
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
            {modelAFile && modelBFile ? (
              <span className="text-green-600">Both files uploaded</span>
            ) : (
              <span className="text-orange-600">Waiting for files</span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm">
            <span className={modelAFile ? "text-green-600" : "text-gray-400"}>
              Model A BOM: {modelAFile ? "✓" : "✗"}
            </span>
            <span className={modelBFile ? "text-green-600" : "text-gray-400"}>
              Model B BOM: {modelBFile ? "✓" : "✗"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ModelModelUpload;