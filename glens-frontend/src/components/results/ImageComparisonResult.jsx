import React, { useEffect, useState, useRef } from "react";
import Viewer from "viewerjs";
import "viewerjs/dist/viewer.css";
import { useImageComparison } from "../../context/ImageComparisonContext";
import { Button } from "@mui/material";
import { Download } from "lucide-react";

const ImageComparisonResult = () => {
  const { imageBlob } = useImageComparison();
  const [imageUrl, setImageUrl] = useState(null);
  const containerRef = useRef(null);
  const viewerRef = useRef(null);

  useEffect(() => {
    if (!imageBlob) return;

    const url = URL.createObjectURL(imageBlob);
    setImageUrl(url);

    return () => {
      URL.revokeObjectURL(url);
      if (viewerRef.current) {
        viewerRef.current.destroy();
        viewerRef.current = null;
      }
    };
  }, [imageBlob]);

  // Initialize viewer only once when image URL changes
  useEffect(() => {
    if (!imageUrl || !containerRef.current) return;

    // Destroy any previous instance
    if (viewerRef.current) viewerRef.current.destroy();

    // Initialize Viewer (popup mode)
    viewerRef.current = new Viewer(containerRef.current, {
      inline: false, // popup (lightbox style)
      toolbar: true,
      movable: true,
      zoomable: true,
      rotatable: true,
      scalable: true,
      fullscreen: true,
      transition: true,
      title: [2, (image, imageData) => image.alt || "Comparison Result"],
    });

    return () => {
      if (viewerRef.current) {
        viewerRef.current.destroy();
        viewerRef.current = null;
      }
    };
  }, [imageUrl]);

  if (!imageBlob) {
    return (
      <div className="text-center text-gray-500 py-10">
        No comparison result available yet.
      </div>
    );
  }

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = imageUrl;
    link.download = "comparison_result.png";
    link.click();
  };

  return (
    <div className="p-6 bg-white rounded-2xl shadow-md text-center">
      <h2 className="text-xl font-semibold mb-4">Comparison Result</h2>

      {/* Viewer.js container */}
      <div ref={containerRef}>
        {imageUrl && (
          <img
            src={imageUrl}
            alt="Comparison Result"
            style={{
              width: "300px", // 👈 small thumbnail
              height: "auto",
              border: "1px solid #aaa",
              borderRadius: "8px",
              cursor: "zoom-in", // indicate zoomable
              transition: "transform 0.2s ease",
              justifySelf:"center",
              marginBottom:"15px"
            }}
            onMouseOver={(e) => (e.currentTarget.style.transform = "scale(1.03)")}
            onMouseOut={(e) => (e.currentTarget.style.transform = "scale(1)")}
          />
        )}
      </div>

      <Button
        onClick={handleDownload}
        variant="contained"
        color="primary"
        startIcon={<Download className="w-4 h-4" />}
        className="mt-4"
      >
        Download Result
      </Button>
    </div>
  );
};

export default ImageComparisonResult;
