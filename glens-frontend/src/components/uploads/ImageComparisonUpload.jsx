import React from "react";
import { Button } from "@mui/material";
import { Upload } from "lucide-react";
import { useImageComparison } from "../../context/ImageComparisonContext";

const ImageComparisonUpload = ({ onCompare }) => {
  const { pdf1, setPdf1, pdf2, setPdf2, loading} = useImageComparison();

  const handleFile1Change = (e) => {
    const file = e.target.files[0];
    setPdf1(file);
  };

  const handleFile2Change = (e) => {
    const file = e.target.files[0];
    setPdf2(file);
  };

  const clearFile1 = () => {
    setPdf1(null);
    const fileInput = document.getElementById('pdf1-file-input');
    if (fileInput) fileInput.value = '';
  };

  const clearFile2 = () => {
    setPdf2(null);
    const fileInput = document.getElementById('pdf2-file-input');
    if (fileInput) fileInput.value = '';
  };

  return (
    <div className="space-y-6">
      {/* File Upload Sections */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* GA Drawing 1 Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              GA Drawing 1 (PDF) <span className="text-red-500">*</span>
            </label>
            {pdf1 && (
              <button
                onClick={clearFile1}
                className="text-red-500 hover:text-red-700 hover:underline text-sm font-medium transition-all duration-200"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="pdf1-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="pdf1-file-input"
                type="file"
                accept="application/pdf"
                onChange={handleFile1Change}
                className="hidden"
                disabled={loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {pdf1 ? (
                  <div className={`text-green-600 font-medium transition-all duration-300 ${pdf1 ? "animate-pulse" : ""}`}>
                    ✓ {pdf1.name}
                  </div>
                ) : (
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      Click to upload
                    </div>
                    <div className="text-xs text-gray-500">
                      .pdf files
                    </div>
                  </div>
                )}
              </div>
            </label>
          </div>
        </div>

        {/* GA Drawing 2 Upload */}
        <div className="bg-white rounded-lg border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-3">
            <label className="block text-sm font-medium text-gray-700">
              GA Drawing 2 (PDF) <span className="text-red-500">*</span>
            </label>
            {pdf2 && (
              <button
                onClick={clearFile2}
                className="text-red-500 hover:text-red-700 text-sm font-medium"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="flex items-center gap-3">
            <label
              htmlFor="pdf2-file-input"
              className="flex-1 cursor-pointer bg-gray-50 hover:bg-blue-50 border-2 border-dashed border-gray-300 hover:border-blue-400 
             rounded-lg p-4 text-center transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-md"
            >
              <input
                id="pdf2-file-input"
                type="file"
                accept="application/pdf"
                onChange={handleFile2Change}
                className="hidden"
                disabled = {loading}
              />
              <div className="space-y-2">
                <div className="text-gray-600">
                  <svg className="mx-auto h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                  </svg>
                </div>
                {pdf2 ? (
                  <div className="text-green-600 font-medium">
                    ✓ {pdf2.name}
                  </div>
                ) : (
                  <div>
                    <div className="text-sm font-medium text-gray-900">
                      Click to upload
                    </div>
                    <div className="text-xs text-gray-500">
                      .pdf files
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
            {pdf1 && pdf2 ? (
              <span className="text-green-600">Both files uploaded</span>
            ) : (
              <span className="text-orange-600">Waiting for files</span>
            )}
          </div>
          <div className="flex items-center gap-4 text-sm">
            <span className={pdf1 ? "text-green-600" : "text-gray-400"}>
              Drawing 1: {pdf1 ? "✓" : "✗"}
            </span>
            <span className={pdf2 ? "text-green-600" : "text-gray-400"}>
              Drawing 2: {pdf2 ? "✓" : "✗"}
            </span>
          </div>
        </div>
      </div>

      {/* Compare Button */}
      <div className="flex justify-center">
        <Button
          onClick={onCompare}
          disabled={!pdf1 || !pdf2}
          variant="contained"
          className="flex items-center gap-2 px-6 py-2 rounded-lg font-medium normal-case shadow-sm hover:shadow transition-all disabled:bg-gray-400 disabled:cursor-not-allowed"
          startIcon={<Upload className="w-4 h-4" />}
        >
          Compare Drawings
        </Button>
      </div>
    </div>
  );
};

export default ImageComparisonUpload;