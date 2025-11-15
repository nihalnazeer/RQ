export const API_BASE = "http://127.0.0.1:8000";

export async function apiGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error("API Error");
  return res.json();
}
