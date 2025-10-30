// components/TabbedContainer.jsx
import React from "react";
import { Tabs, Tab, Box } from "@mui/material";

const TabbedContainer = ({ tabs, activeTab, onTabChange, children }) => {
  return (
    <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
      <Tabs 
        value={activeTab} 
        onChange={onTabChange}
        sx={{ borderBottom: 1, borderColor: 'divider', minHeight: '48px', flexShrink: 0 }}
      >
        {tabs.map((tab, index) => (
          <Tab 
            key={index} 
            label={tab.label}
            sx={{ 
              minWidth: 'auto',
              fontSize: '0.875rem',
              textTransform: 'none'
            }}
          />
        ))}
      </Tabs>

      <Box sx={{ flex: 1, py: 2, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        {children}
      </Box>
    </Box>
  );
};

export default TabbedContainer;