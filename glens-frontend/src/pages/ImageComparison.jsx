import React from "react";
import ImageComparisonUpload from "../components/uploads/ImageComparisonUpload";
import ImageComparisonResult from "../components/results/ImageComparisonResult";
import { useImageComparison } from "../context/ImageComparisonContext";
import { compareDrawings } from "../services/imageComparisonService";
import MainLayout from "../layouts/MainLayout";

const ImageComparison = () => {
  const {
    pdf1,
    pdf2,
    setImageBlob,
    loading,
    setLoading,
    activeTab,
    setActiveTab,
  } = useImageComparison();

  const handleCompare = async () => {
    if (!pdf1 || !pdf2) {
      alert("Please upload both GA PDF files before comparing.");
      return;
    }

    try {
      setLoading(true);
      const blob = await compareDrawings(pdf1, pdf2);
      if (blob) {
        setImageBlob(blob);
        setActiveTab("result");
      } else {
        alert("No comparison image generated.");
      }
    } catch (err) {
      console.error("Error comparing drawings:", err);
      alert("An error occurred during comparison.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <MainLayout
    breadcrumbItems={[
        { label: "Dashboard", href: "/dashboard" },
        { label: "Image Comparison", href: "/operations/image-comparison(ga)", active: true }
      ]}
    >
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">
        GA vs GA Image Comparison
      </h1>

      {/* Tabs */}
      <div className="flex mb-6 border-b border-gray-300">
        <button
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === "upload"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500"
          }`}
          onClick={() => setActiveTab("upload")}
        >
          Upload
        </button>
        <button
          className={`px-4 py-2 text-sm font-medium ${
            activeTab === "result"
              ? "border-b-2 border-blue-600 text-blue-600"
              : "text-gray-500"
          }`}
          onClick={() => setActiveTab("result")}
        >
          Result
        </button>
      </div>

      {/* Tab Content */}
      {activeTab === "upload" && (
        <ImageComparisonUpload onCompare={handleCompare} />
      )}

      {activeTab === "result" && <ImageComparisonResult />}
      {loading && (
        <p className="text-center mt-4 text-blue-600 font-medium">
          Comparing drawings... please wait.
        </p>
      )}
    </div>
    </MainLayout>
  );
};

export default ImageComparison;
