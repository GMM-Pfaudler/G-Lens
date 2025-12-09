import React from "react";

const ModelModelToCreateNew = ({ items = [], category }) => {
  if (!Array.isArray(items) || items.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        No items found in {category}.
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
        <table className="min-w-full text-sm">
          <thead className="bg-gray-100 text-xs text-gray-600 uppercase">
            <tr>
              {["Part No.", "Qty", "Description", "Drawing No.", "Revision", "Material"].map((head) => (
                <th
                  key={head}
                  className="px-4 py-3 text-left font-semibold tracking-wider"
                >
                  {head}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {items.map((item, idx) => (
              <tr key={idx} className="hover:bg-blue-50 transition-colors">
                <td className="px-4 py-3 font-medium text-gray-900">{item["PART NO."]}</td>
                <td className="px-4 py-3">{item.QTY}</td>
                <td className="px-4 py-3">{item.DESCRIPTION}</td>
                <td className="px-4 py-3">{item["DRG. NO. / DIMENSION"]}</td>
                <td className="px-4 py-3">{item["REVISION NUMBER"]}</td>
                <td className="px-4 py-3">{item.MATERIAL}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ModelModelToCreateNew;
