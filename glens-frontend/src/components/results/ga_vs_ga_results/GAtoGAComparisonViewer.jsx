import React, { useState } from "react";
import { Box, Tabs, Tab } from "@mui/material";
import ComparisonReportViewer from "./ComparisonReportViewer";
import NozzleComparisonViewer from "./NozzleComparisonViewer";
import PartListComparisonViewer from "./PartListComparisonViewer";

const GAtoGAComparisonViewer = ({ data }) => {
  const [activeTab, setActiveTab] = useState(0);

  if (!data) return null; // Do not render if no data

  const sections = [
    { label: "Comparison Report", component: <ComparisonReportViewer data={data.comparison_report} /> },
    { label: "Nozzle Comparison", component: <NozzleComparisonViewer data={data.nozzle_comparison_result} /> },
    { label: "Part List Comparison", component: <PartListComparisonViewer data={data.part_list_comparison_result} /> },
  ];

  return (
    <Box>
      <Tabs value={activeTab} onChange={(e, newValue) => setActiveTab(newValue)}>
        {sections.map((s, idx) => (
          <Tab key={idx} label={s.label} />
        ))}
      </Tabs>
      <Box sx={{ mt: 2 }}>
        {sections[activeTab].component}
      </Box>
    </Box>
  );
};

export default GAtoGAComparisonViewer;
