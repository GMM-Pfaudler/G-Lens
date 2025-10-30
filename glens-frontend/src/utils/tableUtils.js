// utils/tableUtils.js
export const getSectionIcon = (section) => {
  const icons = {
    'nozzles': '🔧',
    'agitator': '⚙️', 
    'material': '🏗️',
    'dimensions': '📐'
  };
  return icons[section] || '📋';
};

export const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1);

export const formatHeader = (header) => {
  return header
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/\./g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase())
    .trim();
};

export const renderSimpleValue = (val) => {
  if (val === null || val === undefined) return "-";
  if (typeof val === "object") return "[Nested Object]";
  return String(val);
};