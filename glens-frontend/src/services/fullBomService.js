// import axios from "axios";
import api from "../api/axios";

export const compareFullBOM = async (fileA, fileB, bomLevel = "1") => {
  const formData = new FormData();
  formData.append("file_a", fileA);
  formData.append("file_b", fileB);
  formData.append("bom_level", bomLevel);

  const response = await api.post("/api/comparison/compare-full-bom", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
};
