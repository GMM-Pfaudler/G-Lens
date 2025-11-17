// import axios from "axios";
import api from "../api/axios";

export const uploadAndCompareModelBom = async (modelFile, refFile) => {
  const formData = new FormData();
  formData.append("model_bom", modelFile);
  formData.append("ref_bom", refFile);

  const response = await api.post(`/api/comparison/model-bom-comparison`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
