const API_BASE = "http://127.0.0.1:8000/api/v1";

async function apiGet(endpoint: string) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`);
  }

  return res.json();
}

export const API = {
  revenue: () => apiGet("/analytics/revenue"),
  stockAge: () => apiGet("/analytics/product-age"),
  creditHealth: () => apiGet("/analytics/credit-health"),
  inventoryValue: () => apiGet("/analytics/inventory-value"), // optional 4th KPI
};
