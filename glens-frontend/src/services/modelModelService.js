// import axios from "axios";
import api from "../api/axios";

export const uploadAndCompareModelModel = async (modelAFile, modelBFile) => {
  const formData = new FormData();
  formData.append("model_a", modelAFile);
  formData.append("model_b", modelBFile);

  const response = await api.post(`/api/comparison/compare-modelBOMs`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
