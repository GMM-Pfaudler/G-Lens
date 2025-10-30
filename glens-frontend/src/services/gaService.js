export const extractGa = async (file) => {
  if (!file) throw new Error("No file selected!");

  const formData = new FormData();
  const API_URL = import.meta.env.VITE_API_URL;
  formData.append("file", file);

  try {
    const response = await fetch(`${API_URL}/api/ga/extract`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || "Extraction failed!");
    }

    const data = await response.json();

    // Ensure job_id is returned even if backend says "Already running"
    return {
      job_id: data.job_id || null,
      message: data.message || "",
      status: "started",
      progress: 0,
    };
  } catch (err) {
    console.error("GA extraction service error:", err);
    throw err;
  }
};
