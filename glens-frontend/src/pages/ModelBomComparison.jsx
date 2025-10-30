import React, { useState } from "react";
import { useModelBomComparison } from "../context/ModelBomComparisonContext";
import ModelBomUpload from "../components/uploads/ModelBomUpload";
import ModelBomComparisonResult from "../components/results/ModelBomComparisonResult";
import MainLayout from "../layouts/MainLayout";
import { uploadAndCompareModelBom } from "../services/modelBomService";
import { exportComparisonToExcel } from "../utils/exportComparisonToExcel";
import { Button } from "@mui/material";

const ModelBomComparison = () => {
  const {
    modelFile,
    refFile,
    comparisonResult,
    setComparisonResult,
    loading,
    setLoading,
  } = useModelBomComparison();

  const [activeTab, setActiveTab] = useState("upload");

  const handleCompare = async () => {
    if (!modelFile || !refFile) {
      alert("Please upload both Model BOM and Reference BOM files!");
      return;
    }

    setLoading(true);
    try {
      const result = await uploadAndCompareModelBom(modelFile, refFile);
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
        { label: "Model BOM Comparison", active: true },
      ]}
    >
      <div className="p-6 space-y-6">
        <h2 className="text-2xl font-semibold mb-4">Model BOM Comparison</h2>

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
            <Button onClick={() => exportComparisonToExcel(comparisonResult.comparison_result)}>
                Export to Excel
            </Button>
          {activeTab === "upload" && (
            <div className="space-y-4">
              <ModelBomUpload />
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
              <ModelBomComparisonResult result={comparisonResult} />
            </div>
          )}
        </div>
      </div>
    </MainLayout>
  );
};

export default ModelBomComparison;