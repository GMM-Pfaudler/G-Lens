import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

/**
 * Exports the entire model vs BOM comparison result as a single Excel
 * file with multiple sheets — one per unique Comparison Status.
 *
 * @param {Object} comparisonResult - The "comparison_result" object from backend.
 */
export const exportModelBOMComparisonToExcel = (comparisonResult) => {
  if (!comparisonResult || typeof comparisonResult !== "object") return;

  const workbook = XLSX.utils.book_new();

  // 🧩 Step 1: Flatten all data and group by Comparison Status
  const groupedData = {};

  Object.entries(comparisonResult).forEach(([category, items]) => {
    if (!Array.isArray(items)) return;

    items.forEach((item) => {
      const status = item["Comparison Status"] || category; // fallback to category name
      if (!groupedData[status]) groupedData[status] = [];
      groupedData[status].push({ ...item, _category: category });
    });
  });

  // 🧮 Step 2: Build sheets for each status group
  Object.entries(groupedData).forEach(([status, items]) => {
    if (!items.length) return;

    // Determine if these items have "Comparison Details" or are plain BOM rows
    const hasDetails = !!items[0]["Comparison Details"];
    let data = [];

    if (hasDetails) {
      // Dynamic headers — based on what exists in first item's details
      const sampleDetails = items[0]["Comparison Details"];
      const fields = Object.keys(sampleDetails || {});

      const headers = [
        "Keywords / Part No.",
        "Comparison Status",
        "Mismatched Fields",
        ...fields.flatMap((f) => [
          `${f} (Model BOM)`,
          `${f} (Ref BOM)`
        ])
      ];

      data.push(headers);

      items.forEach((item) => {
        const details = item["Comparison Details"] || {};
        const row = [
          item["KEYWORDS"] ?? "-",
          item["Comparison Status"] ?? "-",
           Array.isArray(item["Mismatched Fields"]) && item["Mismatched Fields"].length
            ? item["Mismatched Fields"].join(", ")   // ✅ JOIN FIELD NAMES
            : "-",
          ...Object.keys(details).flatMap((f) => [
            details[f]?.["Model BOM"] ?? "-",
            details[f]?.["Ref BOM"] ?? "-"
          ])
        ];
        data.push(row);
      });
    } else {
      // Simpler sheet (e.g., TO CREATE NEW, EMPTY OR DASHED)
      const headers = [
        "Part No.",
        "Qty",
        "Description",
        "Drawing No. / Dimension",
        "Revision No.",
        "Material",
        "Status",
      ];
      data.push(headers);

      items.forEach((item) => {
        data.push([
          item["PART NO."] ?? "-",
          item["QTY"] ?? "-",
          item["DESCRIPTION"] ?? "-",
          item["DRG. NO. / DIMENSION"] ?? "-",
          item["REVISION NUMBER"] ?? "-",
          item["MATERIAL"] ?? "-",
          item["KEYWORDS"] ?? "-",
        ]);
      });
    }

    const ws = XLSX.utils.aoa_to_sheet(data);

    // 🪄 Auto column width
    const colWidths = data[0].map((_, i) => ({
      wch: Math.max(...data.map((r) => (r[i] ? r[i].toString().length : 10))) + 2,
    }));
    ws["!cols"] = colWidths;

    // Append to workbook
    XLSX.utils.book_append_sheet(workbook, ws, status.slice(0, 31)); // Excel tab name limit
  });

  // 💾 Save Excel file
  const wbout = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  saveAs(
    new Blob([wbout], { type: "application/octet-stream" }),
    "Model_vs_BOM_Comparison.xlsx"
  );
};



export const exportModelModelComparisonToExcel = (comparisonResult) => {
  if (!comparisonResult || typeof comparisonResult !== "object") return;

  const workbook = XLSX.utils.book_new();

  // 🧩 Step 1: Flatten all data and group by Comparison Status
  const groupedData = {};

  Object.entries(comparisonResult).forEach(([category, items]) => {
    if (!Array.isArray(items)) return;

    items.forEach((item) => {
      const status = item["Comparison Status"] || category; // fallback to category name
      if (!groupedData[status]) groupedData[status] = [];
      groupedData[status].push({ ...item, _category: category });
    });
  });

  // 🧮 Step 2: Build sheets for each status group
  Object.entries(groupedData).forEach(([status, items]) => {
    if (!items.length) return;

    // Determine if these items have "Comparison Details" or are plain BOM rows
    const hasDetails = !!items[0]["Comparison Details"];
    let data = [];

    if (hasDetails) {
      // Dynamic headers — based on what exists in first item's details
      const sampleDetails = items[0]["Comparison Details"];
      const fields = Object.keys(sampleDetails || {});

      const headers = [
        "Keywords",
        "Comparison Status",
        "Mismatched Fields",
        ...fields.flatMap((f) => [
          `${f} (Model A BOM)`,
          `${f} (Model B BOM)`
        ])
      ];

      data.push(headers);

      items.forEach((item) => {
        const details = item["Comparison Details"] || {};
        const row = [
          item["KEYWORDS"] ?? "-",
          item["Comparison Status"] ?? "-",
           Array.isArray(item["Mismatched Fields"]) && item["Mismatched Fields"].length
            ? item["Mismatched Fields"].join(", ")   // ✅ JOIN FIELD NAMES
            : "-",
          ...Object.keys(details).flatMap((f) => [
            details[f]?.["Model A BOM"] ?? "-",
            details[f]?.["Model B BOM"] ?? "-"
          ])
        ];
        data.push(row);
      });
    } else {
      // Simpler sheet (e.g., TO CREATE NEW, EMPTY OR DASHED)
      const headers = [
        "Part No.",
        "Qty",
        "Description",
        "Drawing No. / Dimension",
        "Revision No.",
        "Material",
        "Status",
      ];
      data.push(headers);

      items.forEach((item) => {
        data.push([
          item["PART NO."] ?? "-",
          item["QTY"] ?? "-",
          item["DESCRIPTION"] ?? "-",
          item["DRG. NO. / DIMENSION"] ?? "-",
          item["REVISION NUMBER"] ?? "-",
          item["MATERIAL"] ?? "-",
          item["KEYWORDS"] ?? "-",
        ]);
      });
    }

    const ws = XLSX.utils.aoa_to_sheet(data);

    // 🪄 Auto column width
    const colWidths = data[0].map((_, i) => ({
      wch: Math.max(...data.map((r) => (r[i] ? r[i].toString().length : 10))) + 2,
    }));
    ws["!cols"] = colWidths;

    // Append to workbook
    XLSX.utils.book_append_sheet(workbook, ws, status.slice(0, 31)); // Excel tab name limit
  });

  // 💾 Save Excel file
  const wbout = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  saveAs(
    new Blob([wbout], { type: "application/octet-stream" }),
    "Model_vs_Model_Comparison.xlsx"
  );
};
