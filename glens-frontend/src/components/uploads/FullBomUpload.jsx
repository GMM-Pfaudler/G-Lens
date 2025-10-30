// src/components/uploads/FullBomUpload.jsx
import React from "react";
import { useFullBomComparison } from "../../context/FullBomComparisonContext";
import { Upload, Settings, FileText, X, Check } from "lucide-react";

const FullBomUpload = () => {
  const { fileA, setFileA, fileB, setFileB, bomLevel, setBomLevel } = useFullBomComparison();

  const handleFileChange = (setFileFunction, file) => {
    if (file && !file.name.match(/\.(xlsx|xls)$/i)) {
      alert("Please upload only Excel files (.xlsx, .xls)");
      return;
    }
    setFileFunction(file);
  };

  const removeFile = (setFileFunction) => {
    setFileFunction(null);
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-4 mb-6 transition-all duration-300 hover:shadow-sm">
      {/* Compact Header */}
      <div className="flex items-center gap-2 mb-4">
        <Upload className="w-4 h-4 text-blue-600 transition-transform duration-200 hover:scale-110" />
        <h3 className="text-sm font-semibold text-gray-900">BOM Comparison Files</h3>
      </div>

      {/* Compact Input Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* File A - Compact */}
        <div className="space-y-2">
          <label className="block text-xs font-medium text-gray-700">
            File A
          </label>
          <div className="relative group">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={(e) => handleFileChange(setFileA, e.target.files[0])}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10 text-xs"
            />
            <div className="border border-gray-300 rounded-md px-3 py-2 transition-all duration-200 bg-white text-xs group-hover:border-blue-400 group-hover:shadow-sm group-hover:bg-blue-50/30">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <FileText className={`w-3 h-3 transition-colors duration-200 ${fileA ? 'text-green-500' : 'text-gray-500 group-hover:text-blue-500'}`} />
                  <span className={`truncate transition-colors duration-200 ${fileA ? 'text-green-700 font-medium' : 'text-gray-600 group-hover:text-blue-700'}`}>
                    {fileA ? fileA.name : "Choose File A"}
                  </span>
                </div>
                {fileA ? (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(setFileA);
                    }}
                    className="flex-shrink-0 text-gray-400 hover:text-red-500 transition-colors duration-200 p-1 rounded hover:bg-red-50 ml-2"
                  >
                    <X className="w-3 h-3" />
                  </button>
                ) : (
                  <div className="w-3 h-3 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <Upload className="w-3 h-3 text-blue-400" />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* File B - Compact */}
        <div className="space-y-2">
          <label className="block text-xs font-medium text-gray-700">
            File B
          </label>
          <div className="relative group">
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={(e) => handleFileChange(setFileB, e.target.files[0])}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10 text-xs"
            />
            <div className="border border-gray-300 rounded-md px-3 py-2 transition-all duration-200 bg-white text-xs group-hover:border-green-400 group-hover:shadow-sm group-hover:bg-green-50/30">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 min-w-0 flex-1">
                  <FileText className={`w-3 h-3 transition-colors duration-200 ${fileB ? 'text-green-500' : 'text-gray-500 group-hover:text-green-500'}`} />
                  <span className={`truncate transition-colors duration-200 ${fileB ? 'text-green-700 font-medium' : 'text-gray-600 group-hover:text-green-700'}`}>
                    {fileB ? fileB.name : "Choose File B"}
                  </span>
                </div>
                {fileB ? (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(setFileB);
                    }}
                    className="flex-shrink-0 text-gray-400 hover:text-red-500 transition-colors duration-200 p-1 rounded hover:bg-red-50 ml-2"
                  >
                    <X className="w-3 h-3" />
                  </button>
                ) : (
                  <div className="w-3 h-3 flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    <Upload className="w-3 h-3 text-green-400" />
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* BOM Level - Compact */}
        <div className="space-y-2">
          <label className="block text-xs font-medium text-gray-700 flex items-center gap-1">
            <Settings className="w-3 h-3 transition-transform duration-200 hover:rotate-45" />
            BOM Level
          </label>
          <div className="relative">
            <input
              type="text"
              value={bomLevel}
              onChange={(e) => setBomLevel(e.target.value)}
              placeholder="e.g., 1, .2, ..3"
              className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm transition-all duration-200 bg-white placeholder-gray-400 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 hover:border-gray-400 hover:shadow-sm"
            />
            {bomLevel && (
              <div className="absolute right-2 top-1/2 transform -translate-y-1/2">
                <Check className="w-3 h-3 text-green-500 transition-all duration-300 animate-pulse" />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Minimal Status Indicator with Hover */}
      <div className="mt-3 flex items-center justify-between text-xs group/status">
        <div className="flex items-center gap-2 transition-all duration-200 group-hover/status:gap-3">
          <div className={`w-2 h-2 rounded-full transition-all duration-300 ${fileA && fileB ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></div>
          <span className="text-gray-600 transition-colors duration-200 group-hover/status:text-gray-800">
            {fileA && fileB ? 'Ready to compare' : 'Select both files'}
          </span>
        </div>
        <div className="text-gray-500 text-xs transition-all duration-200 group-hover/status:scale-105 group-hover/status:text-gray-700">
          {fileA && fileB ? (
            <span className="flex items-center gap-1 transition-all duration-300">
              <Check className="w-3 h-3 text-green-500 animate-bounce" />
              All files ready
            </span>
          ) : (
            `${fileA ? '✓ A' : '✗ A'} • ${fileB ? '✓ B' : '✗ B'}`
          )}
        </div>
      </div>
    </div>
  );
};

export default FullBomUpload;