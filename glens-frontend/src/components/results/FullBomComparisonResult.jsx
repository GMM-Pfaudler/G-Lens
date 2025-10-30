// src/components/results/FullBomComparisonResult.jsx
import React, { useState } from "react";
import { useFullBomComparison } from "../../context/FullBomComparisonContext";
import { Download, Filter, Search, ChevronDown, ChevronUp } from "lucide-react";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

const FullBomComparisonResult = () => {
  const { comparisonResult } = useFullBomComparison();
  const [filterStatus, setFilterStatus] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState("asc");

  if (!comparisonResult) return null;

  const { 
    message, 
    bom_level, 
    file1, 
    file2, 
    result_count, 
    comparison_result = [] 
  } = comparisonResult;

  // ✅ Filter + Search logic
  const filteredResults = comparison_result.filter((item) => {
    const statusVal = item.Status || "";
    const matchesStatus =
      filterStatus === "all" ||
      (filterStatus === "other" &&
        (statusVal.includes("❌") || statusVal.includes("➕"))) ||
      statusVal.includes(filterStatus);

    const matchesSearch =
      searchTerm === "" ||
      Object.values(item).some((value) =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      );

    return matchesStatus && matchesSearch;
  });

  // ✅ Sort logic
  const sortedResults = [...filteredResults].sort((a, b) => {
    if (!sortField) return 0;
    const aValue = a[sortField] || "";
    const bValue = b[sortField] || "";
    return sortDirection === "asc"
      ? String(aValue).localeCompare(String(bValue))
      : String(bValue).localeCompare(String(aValue));
  });

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  // ✅ Badge styling fix
  const getStatusBadge = (status) => {
    const base =
      "inline-flex items-center justify-center gap-1 px-2 py-1 text-xs font-medium rounded-full border whitespace-nowrap";
    if (status.includes("✅ Matched"))
      return `${base} bg-green-50 text-green-700 border-green-200`;
    if (status.includes("❌ Modified"))
      return `${base} bg-yellow-50 text-yellow-700 border-yellow-200`;
    if (status.includes("❌ Replaced"))
      return `${base} bg-orange-50 text-orange-700 border-orange-200`;
    if (status.includes("❌"))
      return `${base} bg-red-50 text-red-700 border-red-200`;
    if (status.includes("➕"))
      return `${base} bg-blue-50 text-blue-700 border-blue-200`;
    return `${base} bg-gray-50 text-gray-700 border-gray-200`;
  };

  // ✅ Excel export (no emoji if unrenderable)
  const exportToExcel = () => {
    const headers = Object.keys(comparison_result[0] || {});
    const cleanData = comparison_result.map((row) => {
      const newRow = {};
      for (const key of headers) {
        const value = row[key];
        // remove emoji symbols that may break Excel
        newRow[key] = typeof value === "string" ? value.replace(/[✅❌➕]/g, "").trim() : value;
      }
      return newRow;
    });

    const ws = XLSX.utils.json_to_sheet(cleanData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "BOM Comparison");
    const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    saveAs(new Blob([wbout], { type: "application/octet-stream" }), `BOM_Comparison_${file1}_vs_${file2}.xlsx`);
  };

  return (
    <div className="mt-6 bg-white rounded-lg border border-gray-200 overflow-hidden max-h-[60vh] flex flex-col">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            Comparison Results
            <span className="bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded-full">
              {result_count} items
            </span>
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {message} • BOM Level: <strong>{bom_level}</strong>
          </p>
        </div>

        <button
          onClick={exportToExcel}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition"
        >
          <Download className="w-4 h-4" />
          Export to Excel
        </button>
      </div>

      {/* Filters */}
      <div className="px-6 py-3 bg-gray-50 border-b border-gray-200 flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
          <input
            type="text"
            placeholder="Search across all fields..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Status</option>
          <option value="✅">Matched</option>
          <option value="❌ Modified">Modified</option>
          <option value="❌ Replaced">Replaced</option>
          <option value="other">Other Changes</option>
        </select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto flex-1">
        <table className="w-full min-w-full table-fixed text-sm">
          <thead className="bg-gray-50 border-b border-gray-200 sticky top-0">
            <tr>
              {comparison_result[0] &&
                Object.keys(comparison_result[0]).map((key) => (
                  <th
                    key={key}
                    onClick={() => handleSort(key)}
                    className={`px-4 py-2 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider cursor-pointer hover:bg-gray-100 ${
                      key === "Status" ? "whitespace-nowrap w-[150px]" : "break-words max-w-[250px]"
                    }`}
                  >
                    <div className="flex items-center gap-1">
                      {key.replace(/_/g, " ")}
                      {sortField === key &&
                        (sortDirection === "asc" ? (
                          <ChevronUp className="w-3 h-3" />
                        ) : (
                          <ChevronDown className="w-3 h-3" />
                        ))}
                    </div>
                  </th>
                ))}
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-200">
            {sortedResults.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50">
                {Object.entries(item).map(([key, value]) => (
                  <td
                    key={key}
                    className={`px-4 py-2 align-top ${
                      key === "Status"
                        ? "whitespace-nowrap text-center"
                        : "break-words truncate max-w-[250px]"
                    }`}
                    title={key !== "Status" ? String(value) : undefined}
                  >
                    {key === "Status" ? (
                      <span className={getStatusBadge(value)}>{value}</span>
                    ) : (
                      <span className="text-gray-900 break-words">{value || "-"}</span>
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Empty State */}
      {sortedResults.length === 0 && (
        <div className="text-center py-10">
          <Filter className="w-10 h-10 text-gray-300 mx-auto mb-3" />
          <p className="text-gray-500">No results found</p>
          <p className="text-gray-400 text-sm">Try adjusting filters or search</p>
        </div>
      )}
    </div>
  );
};

export default FullBomComparisonResult;
