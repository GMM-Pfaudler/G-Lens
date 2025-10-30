import React, { useState } from "react";
import { Box, Typography, Tabs, Tab } from "@mui/material";
import GenericTable from "../../table/GenericTable";

const MaterialConstructionSection = ({ materialData }) => {
  const [activeTab, setActiveTab] = useState(0);

  const formatSectionName = (name) => {
    // Simple formatting - capitalize first letter, rest as-is
    return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
  };

  const formatTableData = (sectionName, sectionData) => {
    return Object.entries(sectionData).map(([material, specification]) => ({
      material: material,
      specification: specification
    }));
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  // Filter out empty sections and create tabs
  const sections = Object.entries(materialData || {})
    .filter(([sectionName, sectionData]) => 
      sectionData && typeof sectionData === 'object' && Object.keys(sectionData).length > 0
    )
    .map(([sectionName, sectionData]) => ({
      label: formatSectionName(sectionName),
      data: formatTableData(sectionName, sectionData)
    }));

  const tabStyles = {
    minHeight: '48px',
    textTransform: 'none',
    fontWeight: 'bold',
  };

  const tableColumns = [
    { key: "material", label: "Material" },
    { key: "specification", label: "Specification" },
  ];

  if (sections.length === 0) {
    return (
      <Box sx={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <Typography color="text.secondary">No material data available</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      flex: 1, 
      display: "flex", 
      flexDirection: "column",
      backgroundColor: '#fafafa',
      borderRadius: 1,
      overflow: 'hidden'
    }}>
      {/* Tabs Header */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: 'white' }}>
        <Tabs 
          value={activeTab} 
          onChange={handleTabChange}
          sx={{
            '& .MuiTab-root': tabStyles,
            '& .Mui-selected': {
              color: 'primary.main',
            }
          }}
        >
          {sections.map((section, index) => (
            <Tab 
              key={section.label}
              label={section.label}
              sx={tabStyles}
            />
          ))}
        </Tabs>
      </Box>

      {/* Tab Content */}
      <Box sx={{ flex: 1, overflow: 'auto', p: 1 }}>
        {sections[activeTab] && (
          <GenericTable
            data={sections[activeTab].data}
            columns={tableColumns}
            title={sections[activeTab].label}
          />
        )}
      </Box>
    </Box>
  );
};

export default MaterialConstructionSection;