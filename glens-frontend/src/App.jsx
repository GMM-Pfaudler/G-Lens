import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import OfnGaComparison from "./pages/OfnGaComparison";
import GaGaComparison from "./pages/GaGaComparison";
import FullBomComparison from "./pages/FullBomComparison";
import { FullBomComparisonProvider } from "./context/FullBomComparisonContext";
import ModelBomComparison from "./pages/ModelBomComparison";
import { ModelBomComparisonProvider } from "./context/ModelBomComparisonContext";
import ImageComparison from "./pages/ImageComparison";
import { ImageComparisonProvider } from "./context/ImageComparisonContext";
import ComparisonResultPage from "./pages/history_pages/ComparisonResultPage";
import ComparisonHistoryPage from "./pages/history_pages/ComparisonHistoryPage";
import OfnGaResultPage from "./pages/comparison/ofnGa/ResultPage.jsx";
import GaGaResultPage from "./pages/comparison/gaGa/GaGaResultPage.jsx";

function App() {
  return (
    <Router>
      <>
        {/* ✅ Toastify container (works globally) */}
        <ToastContainer
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop={true}
          closeOnClick
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="colored"
        />

        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />

          {/* 🧩 OFN-GA Comparison Module */}
          <Route path="/ofn-ga-comparison" element={<OfnGaComparison />} />
          <Route path="/ofn-ga-comparison/history" element={<ComparisonHistoryPage />} />
          <Route path="/ofn-ga-comparison/result/:id" element={<ComparisonResultPage />} />

          {/* 🧩 GA–GA Comparison Module */}
          <Route path="/ga-ga-comparison" element={<GaGaComparison />} />
          <Route path="/comparison/ga-ga/result/:id" element={<GaGaResultPage />} />

          {/* 🧩 Full BOM Comparison */}
          <Route
            path="/full-bom-comparison"
            element={
              <FullBomComparisonProvider>
                <FullBomComparison />
              </FullBomComparisonProvider>
            }
          />

          {/* 🧩 Model vs BOM Comparison */}
          <Route
            path="/model-bom-comparison"
            element={
              <ModelBomComparisonProvider>
                <ModelBomComparison />
              </ModelBomComparisonProvider>
            }
          />

          {/* 🧩 Image Comparison */}
          <Route
            path="/image-comparison"
            element={
              <ImageComparisonProvider>
                <ImageComparison />
              </ImageComparisonProvider>
            }
          />

          <Route path="/comparison/ofn-ga/result/:id" element={<OfnGaResultPage />} />
        </Routes>
      </>
    </Router>
  );
}

export default App;
