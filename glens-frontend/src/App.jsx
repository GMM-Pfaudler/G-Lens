import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard"; // will create later
import OfnGaComparison from './pages/OfnGaComparison';
import GaGaComparison from './pages/GaGaComparison';
import FullBomComparison from './pages/FullBomComparison';
import { FullBomComparisonProvider } from './context/FullBomComparisonContext';
import ModelBomComparison from './pages/ModelBomComparison';
import { ModelBomComparisonProvider } from './context/ModelBomComparisonContext';
import ImageComparison from './pages/ImageComparison';
import { ImageComparisonProvider } from './context/ImageComparisonContext';
import ComparisonResultPage from './pages/history_pages/ComparisonResultPage';
import ComparisonHistoryPage from './pages/history_pages/ComparisonHistoryPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />

        {/* 🧩 OFN-GA Comparison Module */}
        <Route path="/ofn-ga-comparison" element={<OfnGaComparison />} />
        <Route path="/ofn-ga-comparison/history" element={<ComparisonHistoryPage />} />
        <Route path="/ofn-ga-comparison/result/:id" element={<ComparisonResultPage />} /> 

        <Route path="/ga-ga-comparison" element={<GaGaComparison />} />
        <Route
          path="/full-bom-comparison"
          element={
            <FullBomComparisonProvider>
              <FullBomComparison />
            </FullBomComparisonProvider>
          }
        />
        <Route
          path="/model-bom-comparison"
          element={
            <ModelBomComparisonProvider>
              <ModelBomComparison />
            </ModelBomComparisonProvider>
          }
        />
        <Route path="/image-comparison" element={
          <ImageComparisonProvider>
            <ImageComparison />
          </ImageComparisonProvider>
          } />

      </Routes>
    </Router>
  );
}
 
export default App;