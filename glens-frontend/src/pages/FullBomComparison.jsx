// src/pages/FullBomComparison.jsx
import React, { useState } from "react";
import MainLayout from "../layouts/MainLayout";
import { useFullBomComparison } from "../context/FullBomComparisonContext";
import FullBomUpload from "../components/uploads/FullBomUpload";
import FullBomComparisonResult from "../components/results/FullBomComparisonResult";
import { compareFullBOM } from "../services/fullBomService";

const FullBomComparison = () => {
  const {
    fileA,
    fileB,
    bomLevel,
    comparisonResult,
    setComparisonResult,
    loading,
    setLoading,
  } = useFullBomComparison();

  const [activeTab, setActiveTab] = useState("upload");

  const handleCompare = async () => {
    if (!fileA || !fileB || !bomLevel) {
      alert("Please upload both files and enter a BOM level!");
      return;
    }

    setLoading(true);
    try {
      const result = await compareFullBOM(fileA, fileB, bomLevel);
      setComparisonResult(result.result);
      setActiveTab("results");
    } catch (err) {
      console.error(err);
      alert("Comparison failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout
      breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "Full BOM Comparison", active: true },
      ]}
    >
      <div className="p-6 space-y-6">
        <h2 className="text-2xl font-semibold mb-4">Full BOM Comparison</h2>

        {/* Tabs Header */}
        <div className="flex border-b border-gray-200 mb-4">
          <button
            onClick={() => setActiveTab("upload")}
            className={`px-6 py-2 text-sm font-medium border-b-2 transition-all duration-150 ${
              activeTab === "upload"
                ? "border-blue-600 text-blue-600"
                : "border-transparent text-gray-600 hover:text-blue-600"
            }`}
          >
            Upload Files
          </button>

          {comparisonResult && (
            <button
              onClick={() => setActiveTab("results")}
              className={`px-6 py-2 text-sm font-medium border-b-2 transition-all duration-150 ${
                activeTab === "results"
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-600 hover:text-blue-600"
              }`}
            >
              Results
            </button>
          )}
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4">
          {activeTab === "upload" && (
            <div className="space-y-4">
              <FullBomUpload />
              <button
                onClick={handleCompare}
                disabled={loading}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                {loading ? "Comparing..." : "Start Comparison"}
              </button>
            </div>
          )}

          {activeTab === "results" && comparisonResult && (
            <div className="max-h-[75vh] overflow-auto">
              <FullBomComparisonResult />
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default FullBomComparison;
