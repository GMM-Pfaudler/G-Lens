import React, { useState } from "react";
import { Paper, Typography, Box, Chip } from "@mui/material";
import GenericTable from "../table/GenericTable";
import TabbedContainer from "../table/TabbedContainer";
import { formatHeader } from "../../utils/tableUtils";
import LiningNotesSection from "./GaTabs/LiningNotesSection";
import { formatAndSortPartList } from "../../utils/sortHelpers";
import KeyValuePairsSection from "./GaTabs/KeyValuePairsSection";
import DesignDataSection from "./GaTabs/DesignDataSection";
import MaterialConstructionSection from "./GaTabs/MaterialConstructionSection";
import { reverseAndFormatNozzleList } from "../../utils/nozzleHelpers";

const GaResultViewer = ({ data }) => {
  console.log("GA RESULT VIEWER RECEIVED:", data);
  const [activeTab, setActiveTab] = useState(0);

  if (!data) return null;

  const rootKey = Object.keys(data)[0];
  const sections = data[rootKey] || {};
  const tabs = prepareTabs(sections);

  const renderTabContent = (tab) => {
    const { label, value } = tab;

    // Special handling for Lining and Notes
    const normalizedLabel = tab.label.toLowerCase();
    if (normalizedLabel.includes("lining") && normalizedLabel.includes("notes")) {
      return (
        <LiningNotesSection 
          liningSpec={value["LINING SPECIFICATION"] || ""}
          generalNotes={value["GENERAL NOTES"] || []}
        />
      );
    }

    // Special handling for Material of Construction
    if (normalizedLabel.includes("material") && normalizedLabel.includes("construction")) {
      return (
        <MaterialConstructionSection materialData={value} />
      );
    }

    // Special handling for Design Data
    if (normalizedLabel.includes("design") && normalizedLabel.includes("data")) {
      if (Array.isArray(value)) {
        return (
          <DesignDataSection designData={value} />
        );
      }
    }

    // Special handling for Key-Value Pairs - rename to "Technical Specifications"
    if (normalizedLabel.includes("key") && normalizedLabel.includes("value") && normalizedLabel.includes("pairs")) {
      return (
        <KeyValuePairsSection keyValueData={value} />
      );
    }

    // Special handling for Part List - sort by part_no
    if (normalizedLabel.includes("part") && normalizedLabel.includes("list")) {
      if (Array.isArray(value)) {
        const formattedAndSortedParts = formatAndSortPartList(value);

        const columns = [
          { key: "part_no", label: "Part No" },
          { key: "qty", label: "Quantity" },
          { key: "description", label: "Description" },
          { key: "drawing_no", label: "Drawing No" },
        ];
        
        return (
          <GenericTable
            data={formattedAndSortedParts}
            columns={columns}
            title={formatHeader(label)}
          />
        );
      }
    }

    // Special handling for Nozzle Data - reverse order and format sizes
    if (normalizedLabel.includes("nozzle") && normalizedLabel.includes("data")) {
      if (Array.isArray(value)) {
        const reversedAndFormattedNozzles = reverseAndFormatNozzleList(value);

        const columns = value.length > 0 
          ? Object.keys(value[0]).map((key) => ({ key, label: formatHeader(key) }))
          : [];
        
        return (
          <GenericTable
            data={reversedAndFormattedNozzles}
            columns={columns}
            title={formatHeader(label)}
          />
        );
      }
    }

    // Empty check
    if (!value || 
        (Array.isArray(value) && value.length === 0) || 
        (typeof value === "object" && Object.keys(value).length === 0)) {
      return (
        <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Typography color="text.secondary">No data available</Typography>
        </Box>
      );
    }

    // Array → Table
    if (Array.isArray(value)) {
      const columns = value.length > 0 
        ? Object.keys(value[0]).map((key) => ({ key, label: formatHeader(key) }))
        : [];
      return (
        <GenericTable
          data={value}
          columns={columns}
          title={formatHeader(label)}
        />
      );
    }

    // Object → Key-Value table
    if (typeof value === "object") {
      const kvData = Object.entries(value).map(([k, v]) => ({ key: k, value: v }));
      const columns = [
        { key: "key", label: "Key" },
        { key: "value", label: "Value" },
      ];
      return (
        <GenericTable
          data={kvData}
          columns={columns}
          title={formatHeader(label)}
        />
      );
    }

    // Fallback
    return <Typography sx={{ p: 2 }}>{String(value)}</Typography>;
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2, // Reduced from p: 3
        borderRadius: 2,
        overflow: "hidden",
        height: "500px",
        display: "flex",
        flexDirection: "column",
        borderColor: 'primary.light'
      }}
    >
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: "bold", color: "primary.main" }}>
          📊 GA Data
        </Typography>
        <Chip 
          label={`${tabs.length}`} 
          size="small" 
          color="primary"
          variant="outlined"
        />
      </Box>

      {tabs.length > 0 ? (
        <TabbedContainer
          tabs={tabs}
          activeTab={activeTab}
          onTabChange={(e, newValue) => setActiveTab(newValue)}
          sx={{ flex: 1 }}
        >
          <Box sx={{ flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" }}>
            {tabs[activeTab] && renderTabContent(tabs[activeTab])}
          </Box>
        </TabbedContainer>
      ) : (
        <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <Typography color="text.secondary">No data available</Typography>
        </Box>
      )}
    </Paper>
  );
};

const prepareTabs = (sections) => {
  return Object.entries(sections).map(([label, value]) => ({
    label: formatHeader(label),
    value,
  }));
};

export default GaResultViewer;