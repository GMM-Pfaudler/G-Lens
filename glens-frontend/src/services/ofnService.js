export const extractOfn = async (file) => {
  const formData = new FormData();
  const API_URL = import.meta.env.VITE_API_URL;
  formData.append("file", file);

  const response = await fetch(`${API_URL}/api/ofn/extract`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) throw new Error("Extraction failed!");
  return await response.json();
};
