import api from "../api/axios";

// 1. Upload PDF with userId
export const uploadPdfForSplit = async (file) => {
  const userId = localStorage.getItem("user_id"); // <-- refreshed
  const formData = new FormData();
  formData.append("file", file);
  formData.append("user_id", userId);

  const response = await api.post("/pdf-splitter/split-pdf", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

// 2. Fetch split history for logged-in user
export const fetchSplitHistory = async () => {
  const userId = localStorage.getItem("user_id"); // <-- refreshed
  const response = await api.get("/pdf-splitter/records", {
    params: { user_id: userId }
  });
  return response.data;
};

// 3. Fetch single record
export const fetchSplitRecord = async (id) => {
  const response = await api.get(`/pdf-splitter/record/${id}`);
  return response.data;
};
