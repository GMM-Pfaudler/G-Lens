// src/components/tabs/GaGaResultTabs.jsx
import React from "react";
import { Tabs, Tab, Box } from "@mui/material";
import { 
  Description, 
  Analytics, 
  CompareArrows, 
  CheckCircle, 
  RadioButtonUnchecked 
} from "@mui/icons-material";

const GaGaResultTabs = ({
  activeTab,
  setActiveTab,
  comparisonLoading,
  firstGaResult,
  secondGaResult,
  comparisonResult
}) => {
  const handleTabChange = (e, newValue) => setActiveTab(newValue);

  const tabData = [
    { 
      label: "First GA", 
      icon: <Description fontSize="small" />, 
      hasData: !!(firstGaResult?.result || firstGaResult)
    },
    { 
      label: "Second GA", 
      icon: <Analytics fontSize="small" />, 
      hasData: !!(secondGaResult?.result || secondGaResult)
    },
    { 
      label: "Comparison", 
      icon: <CompareArrows fontSize="small" />, 
      hasData: !!comparisonResult
    }
  ];

  return (
    <Box sx={{ borderBottom: 1, borderColor: "divider", px: 2 }}>
      <Tabs
        value={activeTab}
        onChange={handleTabChange}
        disabled={comparisonLoading}
        sx={{
          "& .MuiTab-root": {
            minHeight: "60px",
            fontWeight: 600,
            fontSize: "0.9rem",
            textTransform: "none",
            "&.Mui-selected": { color: "primary.main" }
          },
          "& .MuiTabs-indicator": {
            backgroundColor: "primary.main",
            height: 3
          }
        }}
      >
        {tabData.map((tab, index) => (
          <Tab
            key={index}
            icon={
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {tab.icon}
                {tab.hasData ? (
                  <CheckCircle
                    fontSize="small"
                    sx={{ color: "success.main", fontSize: "18px" }}
                  />
                ) : (
                  <RadioButtonUnchecked
                    fontSize="small"
                    sx={{ color: "grey.400", fontSize: "18px" }}
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

export default GaGaResultTabs;
