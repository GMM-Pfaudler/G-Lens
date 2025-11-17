export default function formatUserName(userId) {
  if (!userId || typeof userId !== "string") return "";

  // Only keep part before '@'
  const local = userId.split("@")[0] || userId;

  // If it's clearly non-personal (like 'admin'), return capitalized single token
  const tokens = local.split(/[\._\-]+/).filter(Boolean);
  if (tokens.length === 0) return "";

  const formatted = tokens
    .map((t) => {
      // handle cases like "john", "o'neil", "mcgregor" lightly
      const lower = t.toLowerCase();
      return lower.charAt(0).toUpperCase() + lower.slice(1);
    })
    .join(" ");

  return formatted;
}