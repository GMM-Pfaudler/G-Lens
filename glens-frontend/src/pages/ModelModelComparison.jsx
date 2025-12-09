import React, { useState } from "react";
import { useModelModelComparison } from "../context/ModelModelComparisonContext";
import ModelModelUpload from "../components/uploads/ModelModelUpload";
import ModelModelComparisonResult from "../components/results/ModelModelComparisonResult";
import MainLayout from "../layouts/MainLayout";
import { uploadAndCompareModelModel } from "../services/modelModelService";
import { exportModelModelComparisonToExcel } from "../utils/exportComparisonToExcel";
import { Button } from "@mui/material";

const ModelModelComparison = () => {
  const {
    modelAFile,
    modelBFile,
    comparisonResult,
    setComparisonResult,
    loading,
    setLoading,
  } = useModelModelComparison();

  const [activeTab, setActiveTab] = useState("upload");

  const handleCompare = async () => {
    if (!modelAFile || !modelBFile) {
      alert("Please upload both Model A BOM and Model B BOM files!");
      return;
    }

    setLoading(true);
    try {
      const result = await uploadAndCompareModelModel(modelAFile, modelBFile);
      setComparisonResult(result);
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
        { label: "Model v Model BOM Comparison", active: true },
      ]}
    >
      <div className="p-6 space-y-6">
        <h2 className="text-2xl font-semibold mb-4">Model BOM Vs Model BOM Comparison</h2>

        {/* Tabs Header - Consistent with Full BOM */}
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
            <Button onClick={() => exportModelModelComparisonToExcel(comparisonResult.comparison_result)}>
                Export to Excel
            </Button>
          {activeTab === "upload" && (
            <div className="space-y-4">
              <ModelModelUpload />
              <button
                onClick={handleCompare}
                disabled={loading}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-blue-400 disabled:cursor-not-allowed"
              >
                {loading ? "Comparing..." : "Start Comparison"}
              </button>
            </div>
          )}

          {activeTab === "results" && comparisonResult && (
            <div className="max-h-[75vh] overflow-auto">
              <ModelModelComparisonResult result={comparisonResult} />
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default ModelModelComparison;