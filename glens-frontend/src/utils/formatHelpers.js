// Helper functions for formatting various data
export const formatPartDescription = (description) => {
  if (typeof description !== 'string') return description;
  
  // Add slashes to measurements like "1 2''" -> "1/2''"
  return description
    .replace(/(\d+)\s+(\d+)''/g, '$1/$2″')  // Handle fractions like "1 2''" -> "1/2″"
    .replace(/(\d+)\s+(\d+)"/g, '$1/$2″')   // Handle fractions with double quotes
    .replace(/(\d+)\s+(\d+)'/g, '$1/$2′')   // Handle fractions with single quotes
    .replace(/''/g, '″')                    // Convert double quotes to proper symbol
    .replace(/'/g, '′');                    // Convert single quotes to proper symbol
};

// Enhanced helper for nozzle data with slash logic for multiple numbers
export const formatNozzleData = (nozzleList) => {
  if (!Array.isArray(nozzleList)) return nozzleList;
  
  return nozzleList.map(nozzle => {
    let size = nozzle["Size (DN)"] || '';
    
    if (typeof size === 'string') {
      // First, handle multiple numbers separated by spaces "80 50 25" -> "80/50/25"
      size = size.replace(/(\d+(?:\s+\d+)+)/g, (match) => {
        // Replace spaces with slashes between consecutive numbers
        return match.replace(/\s+/g, '/');
      });
      
      // Then apply the existing fraction formatting
      size = size
        .replace(/(\d+)\s+(\d+)''/g, '$1/$2″')
        .replace(/(\d+)\s+(\d+)"/g, '$1/$2″')
        .replace(/(\d+)\s+(\d+)'/g, '$1/$2′')
        .replace(/''/g, '″')
        .replace(/'/g, '′');
    }
    
    return {
      ...nozzle,
      "Size (DN)": size
    };
  });
};