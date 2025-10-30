import React, { useState } from "react";
import { Paper, Typography, Box, Chip } from "@mui/material";
import GenericTable from "../table/GenericTable";
import TabbedContainer from "../table/TabbedContainer";
import { formatHeader, capitalize, getSectionIcon } from "../../utils/tableUtils";

const OfnResultViewer = ({ data }) => {
  const [activeTab, setActiveTab] = useState(0);

  if (!data) return null;

  const tabs = prepareTabs(data);

  const renderTabContent = (tab) => {
    switch (tab.type) {
      case "metadata":
        return (
          <GenericTable
            data={tab.data.map(([field, value]) => ({ field, value }))}
            columns={[
              { key: "field", label: "Field" },
              { key: "value", label: "Value" }
            ]}
          />
        );

      case "table":
        const { columns, rows, section } = tab.data;
        return (
          <GenericTable
            data={rows}
            columns={columns.map(col => ({
              key: col,
              label: formatHeader(col)
            }))}
            title={formatHeader(section)}
          />
        );

      default:
        return null;
    }
  };

  return (
    <Paper variant="outlined" sx={{ 
      p: 2, // Reduced from p: 3
      borderRadius: 2, 
      overflow: "hidden",
      height: "500px",
      display: 'flex',
      flexDirection: 'column',
      borderColor: 'primary.light'
    }}>
      {/* Compact Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: "bold", color: 'primary.main' }}>
          📊 OFN Data
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
          <Box sx={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
            {tabs[activeTab] && renderTabContent(tabs[activeTab])}
          </Box>
        </TabbedContainer>
      ) : (
        <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Typography color="text.secondary">No data available</Typography>
        </Box>
      )}
    </Paper>
  );
};

// Helper functions (can be moved to tableUtils.js)
const prepareTabs = (data) => {
  const tabs = [];

  // Metadata tab
  const metadataEntries = Object.entries(data).filter(([key]) => key !== "tables");
  if (metadataEntries.length > 0) {
    tabs.push({
      label: "📄 Metadata",
      type: "metadata", 
      data: metadataEntries
    });
  }

  // Table tabs
  if (data.tables && Array.isArray(data.tables)) {
    data.tables.forEach((table) => {
      const sectionKey = table.section;
      const rowsKey = Object.keys(table).find((k) => k.endsWith("_details"));
      const rows = rowsKey ? table[rowsKey] : [];
      
      if (rows.length > 0) {
        const icon = getSectionIcon(sectionKey);
        tabs.push({
          label: `${icon} ${capitalize(sectionKey)}`,
          type: "table",
          data: {
            section: sectionKey,
            columns: Object.keys(rows[0]),
            rows: rows
          }
        });
      }
    });
  }

  return tabs;
};

export default OfnResultViewer;