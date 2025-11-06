import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8006";

export const compareDrawings = async (pdf1, pdf2) => {
  const formData = new FormData();
  formData.append("pdf1", pdf1);
  formData.append("pdf2", pdf2);

  try {
    const response = await axios.post(
      `${API_BASE_URL}/api/comparison/compare_drawings/`,
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
