import { formatNozzleData } from './formatHelpers';

export const reverseAndFormatNozzleList = (nozzleList) => {
  if (!Array.isArray(nozzleList)) return nozzleList;
  
  // Reverse the array to get correct order
  const reversed = [...nozzleList].reverse();
  
  // Format the sizes
  return formatNozzleData(reversed);
};