import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8006";

export const uploadAndCompareModelBom = async (modelFile, refFile) => {
  const formData = new FormData();
  formData.append("model_bom", modelFile);
  formData.append("ref_bom", refFile);

  const response = await axios.post(`${API_BASE}/api/comparison/model-bom-comparison`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
