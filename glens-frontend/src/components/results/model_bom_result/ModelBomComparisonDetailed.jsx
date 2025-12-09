// src/components/results/ModelBomComparisonDetailed.jsx
import React from "react";

const ModelBomComparisonDetailed = ({ items = [], category }) => {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No records found in {category}.
      </div>
    );
  }

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-all bg-white">
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-b">
        <div>
          <h3 className="text-sm font-semibold text-gray-800">{category}</h3>
          <p className="text-xs text-gray-500">{items.length} item(s) found</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-100 text-xs text-gray-600 uppercase">
            <tr>
              {[
                "Keywords",
                "Status",
                "Drawing No.",
                "Model Qty",
                "Ref Qty",
                "Model Revision",
                "Ref Revision",
                category === "PARTIAL MISMATCH"?("Mismatch Fields"):null
              ].map((head) => (
                <th key={head} className="px-4 py-3 text-left">
                  {head}
                </th>
              ))}
            </tr>
          </thead>

          <tbody className="bg-white divide-y divide-gray-100">
            {items.map((item, idx) => {
              const details = item["Comparison Details"] || {};
              const mismatchedFields = Object.entries(details)
                .filter(([_, field]) => field.Match === false)
                .map(([field]) => field);

              return (
                <tr key={idx} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-900">{item.KEYWORDS}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        item["Comparison Status"] === "Match"
                          ? "bg-green-100 text-green-800"
                          : item["Comparison Status"] === "Mismatch"
                          ? "bg-yellow-100 text-yellow-800"
                          : item["Comparison Status"] === "Potential Replacement"
                          ? "bg-blue-100 text-blue-800"
                          : item["Comparison Status"] === "Missing in Ref BOM"
                          ? "bg-red-100 text-red-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {item["Comparison Status"]}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-700">
                    {details?.["DRG. NO. / DIMENSION"]?.["Model BOM"] ||
                      details?.["DRG. NO. / DIMENSION"]?.["Ref BOM"] ||
                      "-"}
                  </td>
                  <td className="px-4 py-3">{details?.QTY?.["Model BOM"] ?? "-"}</td>
                  <td className="px-4 py-3">{details?.QTY?.["Ref BOM"] ?? "-"}</td>
                  <td className="px-4 py-3">{details?.["REVISION NUMBER"]?.["Model BOM"] ?? "-"}</td>
                  <td className="px-4 py-3">{details?.["REVISION NUMBER"]?.["Ref BOM"] ?? "-"}</td>
                  <td className="px-4 py-3 text-xs">
                    {category === "PARTIAL MISMATCH"?(mismatchedFields.length === 0 ? (
                      <span className="text-green-600">All match</span>
                    ) : (
                      <span className="text-red-600">{mismatchedFields.join(", ")}</span>
                    )): null}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelBomComparisonDetailed;
