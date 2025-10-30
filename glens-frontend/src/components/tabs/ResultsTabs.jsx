// components/tabs/ResultTabs.jsx
import React from "react";
import { Tabs, Tab, Box } from "@mui/material";
import { 
  Description, 
  Analytics, 
  CompareArrows,
  CheckCircle,
  RadioButtonUnchecked
} from "@mui/icons-material";

const ResultTabs = ({
  comparisonTab,
  setComparisonTab,
  comparisonLoading,
  ofnResult,
  gaResult,
  comparisonResult
}) => {
  const handleTabChange = (e, newValue) => setComparisonTab(newValue);

  const tabData = [
    { 
      label: "OFN Data", 
      icon: <Description fontSize="small" />,
      hasData: !!(ofnResult?.result || ofnResult)
    },
    { 
      label: "GA Data", 
      icon: <Analytics fontSize="small" />,
      hasData: !!(gaResult?.result || gaResult)
    },
    { 
      label: "Comparison", 
      icon: <CompareArrows fontSize="small" />,
      hasData: !!comparisonResult
    }
  ];

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider', px: 2 }}>
      <Tabs 
        value={comparisonTab} 
        onChange={handleTabChange} 
        disabled={comparisonLoading}
        sx={{
          '& .MuiTab-root': {
            minHeight: '60px',
            fontWeight: 600,
            fontSize: '0.9rem',
            textTransform: 'none',
            '&.Mui-selected': {
              color: 'primary.main',
            }
          },
          '& .MuiTabs-indicator': {
            backgroundColor: 'primary.main',
            height: 3
          }
        }}
      >
        {tabData.map((tab, index) => (
          <Tab 
            key={index}
            icon={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                {tab.icon}
                {tab.hasData ? (
                  <CheckCircle 
                    fontSize="small" 
                    sx={{ 
                      color: 'success.main',
                      fontSize: '18px'
                    }} 
                  />
                ) : (
                  <RadioButtonUnchecked 
                    fontSize="small" 
                    sx={{ 
                      color: 'grey.400',
                      fontSize: '18px'
                    }} 
                  />
                )}
              </Box>
            }
            iconPosition="start"
            label={tab.label}
          />
        ))}
      </Tabs>
    </Box>
  );
};

export default ResultTabs;