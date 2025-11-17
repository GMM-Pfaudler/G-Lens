// import axios from "axios";
import api from "../api/axios";

export const compareDrawings = async (pdf1, pdf2) => {
  const formData = new FormData();
  formData.append("pdf1", pdf1);
  formData.append("pdf2", pdf2);

  try {
    const response = await api.post(
      `/api/comparison/compare_drawings/`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob", // important
      }
    );

    console.log("✅ Blob received:", response.data);
    return response.data; // <-- return blob directly
  } catch (error) {
    console.error("Error comparing drawings:", error);
    throw error;
  }
};
