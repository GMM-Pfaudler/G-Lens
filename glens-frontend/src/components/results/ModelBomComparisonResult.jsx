import React, { useState } from "react";
import ModelBomNewlyAdded from "../results/model_bom_result/ModelBomNewlyAdded";
import ModelBomComparisonDetailed from "../results/model_bom_result/ModelBomComparisonDetailed";
import ModelBomToCreateNew from "../results/model_bom_result/ModelBomToCreateNew";

const ModelBomComparisonResult = ({ result }) => {
  const [activeTab, setActiveTab] = useState("TO CREATE NEW");
  const [activeSubTab, setActiveSubTab] = useState("FULLY MATCHED");

  if (!result) {
    return <div className="text-center py-8 text-gray-500">No comparison results available.</div>;
  }

  const processedResults = { ...result.comparison_result };

  // 🧩 Separate FULLY MATCHED and PARTIAL MISMATCH
  if (processedResults.MATCHED) {
    const matched = [];
    const mismatched = [];
    processedResults.MATCHED.forEach((item) =>
      item["Comparison Status"] === "Match" ? matched.push(item) : mismatched.push(item)
    );
    processedResults.MATCHED = {
      "FULLY MATCHED": matched,
      "PARTIAL MISMATCH": mismatched,
    };
  }

  const tabs = Object.keys(result.comparison_result || {});
  const hasSubTabs = activeTab === "MATCHED";

  const renderContent = (tab) => {
    if (tab === "NEWLY ADDED" || tab === "UNMATCHED / MISSING")
      return <ModelBomNewlyAdded items={processedResults[tab]} category={tab} />;

    if (tab === "TO CREATE NEW" || tab === "EMPTY OR DASHED")
      return <ModelBomToCreateNew items={processedResults[tab]} category={tab} />;

    if (tab === "MATCHED") {
      const subItems = processedResults.MATCHED[activeSubTab] || [];
      return (
        <ModelBomComparisonDetailed
          items={subItems}
          category={activeSubTab}
        />
      );
    }

    return (
      <ModelBomComparisonDetailed
        items={processedResults[tab]}
        category={tab}
      />
    );
  };

  return (
    <div className="h-[60vh] flex flex-col bg-white rounded-lg border shadow-sm">
      {/* Header */}
      <div className="p-5 border-b bg-gray-50 rounded-t-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-sm">
          <div><b>Model File:</b> {result.model_bom_file}</div>
          <div><b>Reference File:</b> {result.ref_bom_file}</div>
          <div><b>Status:</b> <span className="text-green-700 font-medium">✔ Success</span></div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {Object.entries(result.result_summary || {}).map(([k, v]) => (
            <span key={k} className="px-3 py-1 bg-blue-50 border rounded-md text-xs text-blue-800">
              {k}: {v}
            </span>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b flex space-x-6 px-4 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => {
              setActiveTab(tab);
              if (tab === "MATCHED") setActiveSubTab("FULLY MATCHED");
            }}
            className={`py-4 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
              activeTab === tab
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab} (
            {Array.isArray(result.comparison_result[tab])
              ? result.comparison_result[tab].length
              : Object.values(processedResults.MATCHED || {})
                  .reduce((a, b) => a + b.length, 0)})
          </button>
        ))}
      </div>

      {/* Subtabs for MATCHED */}
      {hasSubTabs && (
        <div className="bg-gray-100 border-b flex gap-3 px-4 py-2">
          {Object.keys(processedResults.MATCHED).map((sub) => (
            <button
              key={sub}
              onClick={() => setActiveSubTab(sub)}
              className={`px-3 py-1 rounded-md text-xs font-medium transition ${
                activeSubTab === sub
                  ? "bg-blue-500 text-white shadow-sm"
                  : "text-gray-700 hover:bg-blue-50"
              }`}
            >
              {sub} ({processedResults.MATCHED[sub].length})
            </button>
          ))}
        </div>
      )}

      {/* Render Selected */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {renderContent(activeTab)}
      </div>
    </div>
  );
};

export default ModelBomComparisonResult;
