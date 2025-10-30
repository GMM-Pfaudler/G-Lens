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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} /> 
        <Route path="/ofn-ga-comparison" element={<OfnGaComparison />} /> 
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
      </Routes>
    </Router>
  );
}
 
export default App;