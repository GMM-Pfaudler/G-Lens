import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8006";

export const compareFullBOM = async (fileA, fileB, bomLevel = "1") => {
  const formData = new FormData();
  formData.append("file_a", fileA);
  formData.append("file_b", fileB);
  formData.append("bom_level", bomLevel);

  const response = await axios.post(`${API_BASE_URL}/api/comparison/compare-full-bom`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
