import React from "react";

const ModelBomNewlyAdded = ({ items = [], category}) => {
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
              <th className="px-4 py-3 text-left">Qty (Ref)</th>
              <th className="px-4 py-3 text-left">Description (Ref)</th>
              <th className="px-4 py-3 text-left">Drawing No. (Ref)</th>
              <th className="px-4 py-3 text-left">Revision (Ref)</th>
              <th className="px-4 py-3 text-left">Status</th>
            </tr>
          </thead>) : (
            <thead className="bg-gray-100 text-xs text-gray-600 uppercase">
            <tr>
              <th className="px-4 py-3 text-left">Keywords / Part No.</th>
              <th className="px-4 py-3 text-left">Qty (Model)</th>
              <th className="px-4 py-3 text-left">Description (Model)</th>
              <th className="px-4 py-3 text-left">Drawing No. (Model)</th>
              <th className="px-4 py-3 text-left">Revision (Model)</th>
              <th className="px-4 py-3 text-left">Status</th>
            </tr>
          </thead>
          )
          }
          <tbody className="bg-white divide-y divide-gray-100">
            {category === "NEWLY ADDED" ?(items.map((item, idx) => {
              const details = item["Comparison Details"] || {};
              const kw = details["KEYWORDS"]?.["Ref BOM"] ?? item["KEYWORDS"] ?? "-";
              const qty = details["QTY"]?.["Ref BOM"] ?? "-";
              const desc = details["DESCRIPTION"]?.["Ref BOM"] ?? "-";
              const drg = details["DRG. NO. / DIMENSION"]?.["Ref BOM"] ?? "-";
              const rev = details["REVISION NUMBER"]?.["Ref BOM"] ?? "-";
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
              const kw = details["KEYWORDS"]?.["Model BOM"] ?? item["KEYWORDS"] ?? "-";
              const qty = details["QTY"]?.["Model BOM"] ?? "-";
              const desc = details["DESCRIPTION"]?.["Model BOM"] ?? "-";
              const drg = details["DRG. NO. / DIMENSION"]?.["Model BOM"] ?? "-";
              const rev = details["REVISION NUMBER"]?.["Model BOM"] ?? "-";
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

export default ModelBomNewlyAdded;
