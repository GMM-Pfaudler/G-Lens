// src/components/uploads/FullBomUpload.jsx
import React from "react";
import { useFullBomComparison } from "../../context/FullBomComparisonContext";

const FullBomUpload = () => {
  const { fileA, setFileA, fileB, setFileB, bomLevel, setBomLevel, loading, setLoading } = useFullBomComparison();

  const handleFileAChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileA(file);
    }
  };

  const handleFileBChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileB(file);
    }
  };

  const clearFileA = () => {
    setFileA(null);
    const fileInput = document.getElementById('file-a-input');
    if (fileInput) fileInput.value = '';
  };

  const clearFileB = () => {
    setFileB(null);
    const fileInput = document.getElementById('file-b-input');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="space-y-6">
      {/* File Upload Sections */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* File A Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              File A <span className="text-red-500">*</span>
            </label>
            {fileA && (
              <button
                onClick={clearFileA}
                className="text-red-500 hover:text-red-700 hover:underline text-sm font-medium transition-all duration-200"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="file-a-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="file-a-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileAChange}
                className="hidden"
                disabled = {loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {fileA ? (
                  <div className={`text-green-600 font-medium transition-all duration-300 ${fileA ? "animate-pulse" : ""}`}>
                    ✓ {fileA.name}
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

        {/* File B Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              File B <span className="text-red-500">*</span>
            </label>
            {fileB && (
              <button
                onClick={clearFileB}
                className="text-red-500 hover:text-red-700 hover:underline text-sm font-medium transition-all duration-200"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="file-b-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-green-50 border-2 border-dashed border-gray-300 hover:border-green-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="file-b-input"
                type="file"
                accept=".xlsx,.xls"
                onChange={handleFileBChange}
                className="hidden"
                disabled = {loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {fileB ? (
                  <div className="text-green-600 font-medium">
                    ✓ {fileB.name}
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

        {/* BOM Level Input */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              BOM Level
            </label>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="flex-1">
              <input
                type="text"
                value={bomLevel}
                onChange={(e) => setBomLevel(e.target.value)}
                placeholder="e.g., 1, .2, ..3"
                className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm transition-all duration-200 bg-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-gray-400 hover:shadow-sm"
              />
              <div className="text-xs text-gray-500 mt-1">
                Optional: Specify BOM level format
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Status Indicators */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center justify-between">
          <div className="text-sm text-blue-700">
            <strong>Ready to compare:</strong>{" "}
            {fileA && fileB ? (
              <span className="text-green-600">Both files uploaded</span>
            ) : (
              <span className="text-orange-600">Waiting for files</span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm">
            <span className={fileA ? "text-green-600" : "text-gray-400"}>
              File A: {fileA ? "✓" : "✗"}
            </span>
            <span className={fileB ? "text-green-600" : "text-gray-400"}>
              File B: {fileB ? "✓" : "✗"}
            </span>
            <span className="text-gray-400">
              BOM Level: {bomLevel ? "✓" : "Optional"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FullBomUpload;