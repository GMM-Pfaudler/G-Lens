import { useState, useEffect } from "react";
import { fetchSplitHistory } from "../services/pdfService";

export default function useLivePdfSplits() {
  const [splitRecords, setSplitRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  const reload = async () => {
    setLoading(true);

    try {
      const res = await fetchSplitHistory();

      // Backend returns: { success: true, records: [...] }
      const rawRecords = res.records || [];

      // Convert backend fields → frontend format
      const formatted = rawRecords.map(r => ({
        id: r.id,
        filename: r.file_name,
        status: r.status,
        uploaded_at: r.uploaded_on,
        files: (r.results || []).map(path => ({
          download_url: path, // keep original path (or convert later)
        })),
      }));

      setSplitRecords(formatted);

    } catch (error) {
      console.error("Failed to load PDF split history:", error);
    }

    setLoading(false);
  };

  useEffect(() => {
    reload();
  }, []);

  return { splitRecords, loading, reload };
}
