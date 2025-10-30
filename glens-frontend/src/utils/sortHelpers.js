import { formatPartDescription } from './formatHelpers';

// Helper functions for sorting various data types
export const sortPartList = (partList) => {
  if (!Array.isArray(partList)) return partList;
  
  return [...partList].sort((a, b) => {
    const partA = parseInt(a.part_no) || 0;
    const partB = parseInt(b.part_no) || 0;
    return partA - partB;
  });
};

export const formatAndSortPartList = (partList) => {
  if (!Array.isArray(partList)) return partList;
  
  const sorted = sortPartList(partList);
  
  // Format descriptions in the sorted list
  return sorted.map(part => ({
    ...part,
    description: formatPartDescription(part.description)
  }));
};