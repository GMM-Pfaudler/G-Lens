import React from "react";

const ModelModelNewlyAdded = ({ items = [], category }) => {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No items found in {category}.
      </div>
    );
  }

  return (
    <div className="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-all bg-white">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 bg-gray-50 border-b">
        <div>
          <h3 className="text-sm font-semibold text-gray-800">{category}</h3>
          <p className="text-xs text-gray-500">{items.length} item(s) found</p>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          {category === "UNMATCHED / MISSING" ? (
          <thead className="bg-gray-100 text-xs text-gray-600 uppercase">
            <tr>
              <th className="px-4 py-3 text-left">Keywords / Part No.</th>
              <th className="px-4 py-3 text-left">Qty (Model A)</th>
              <th className="px-4 py-3 text-left">Description (Model A)</th>
              <th className="px-4 py-3 text-left">Drawing No. (Model A)</th>
              <th className="px-4 py-3 text-left">Revision (Model A)</th>
              <th className="px-4 py-3 text-left">Status</th>
            </tr>
          </thead>) : (
            <thead className="bg-gray-100 text-xs text-gray-600 uppercase">
            <tr>
              <th className="px-4 py-3 text-left">Keywords / Part No.</th>
              <th className="px-4 py-3 text-left">Qty (Model B)</th>
              <th className="px-4 py-3 text-left">Description (Model B)</th>
              <th className="px-4 py-3 text-left">Drawing No. (Model B)</th>
              <th className="px-4 py-3 text-left">Revision (Model B)</th>
              <th className="px-4 py-3 text-left">Status</th>
            </tr>
          </thead>
          )
          }
          <tbody className="bg-white divide-y divide-gray-100">
            {category === "UNMATCHED / MISSING" ?(items.map((item, idx) => {
              const details = item["Comparison Details"] || {};
              const kw = details["KEYWORDS"]?.["Model A BOM"] ?? item["KEYWORDS"] ?? "-";
              const qty = details["QTY"]?.["Model A BOM"] ?? "-";
              const desc = details["DESCRIPTION"]?.["Model A BOM"] ?? "-";
              const drg = details["DRG. NO. / DIMENSION"]?.["Model A BOM"] ?? "-";
              const rev = details["REVISION NUMBER"]?.["Model A BOM"] ?? "-";
              const status = item["Comparison Status"] ?? "Unknown";

              // Color badge logic (same as in detailed view)
              const getStatusStyle = (status) => {
                if (status.includes("New")) return "bg-blue-100 text-blue-800";
                if (status.includes("Missing")) return "bg-red-100 text-red-800";
                if (status.includes("Match")) return "bg-green-100 text-green-800";
                return "bg-gray-100 text-gray-800";
              };

              return (
                <tr key={idx} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-900 truncate max-w-xs" title={kw}>
                    {kw}
                  </td>
                  <td className="px-4 py-3">{qty}</td>
                  <td className="px-4 py-3 text-sm text-gray-700 truncate max-w-xl" title={desc}>
                    {desc}
                  </td>
                  <td className="px-4 py-3">{drg}</td>
                  <td className="px-4 py-3">{rev}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusStyle(
                        status
                      )}`}
                    >
                      {status}
                    </span>
                  </td>
                </tr>
              );
            })):(items.map((item, idx) => {
              const details = item["Comparison Details"] || {};
              const kw = details["KEYWORDS"]?.["Model B BOM"] ?? item["KEYWORDS"] ?? "-";
              const qty = details["QTY"]?.["Model B BOM"] ?? "-";
              const desc = details["DESCRIPTION"]?.["Model B BOM"] ?? "-";
              const drg = details["DRG. NO. / DIMENSION"]?.["Model B BOM"] ?? "-";
              const rev = details["REVISION NUMBER"]?.["Model B BOM"] ?? "-";
              const status = item["Comparison Status"] ?? "Unknown";

              // Color badge logic (same as in detailed view)
              const getStatusStyle = (status) => {
                if (status.includes("New")) return "bg-blue-100 text-blue-800";
                if (status.includes("Missing")) return "bg-red-100 text-red-800";
                if (status.includes("Match")) return "bg-green-100 text-green-800";
                return "bg-gray-100 text-gray-800";
              };

              return (
                <tr key={idx} className="hover:bg-blue-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-900 truncate max-w-xs" title={kw}>
                    {kw}
                  </td>
                  <td className="px-4 py-3">{qty}</td>
                  <td className="px-4 py-3 text-sm text-gray-700 truncate max-w-xl" title={desc}>
                    {desc}
                  </td>
                  <td className="px-4 py-3">{drg}</td>
                  <td className="px-4 py-3">{rev}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusStyle(
                        status
                      )}`}
                    >
                      {status}
                    </span>
                  </td>
                </tr>
              );
            }))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelModelNewlyAdded;
