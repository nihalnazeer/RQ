const API_BASE = "http://127.0.0.1:8000/api/v1";

async function apiGet(endpoint: string, params?: Record<string, any>) {
  const url = new URL(`${API_BASE}${endpoint}`);

  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null) url.searchParams.append(k, String(v));
    });
  }

  const res = await fetch(url.toString(), { cache: "no-store" });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export const API = {
  analytics: {
    revenue: (params?: { start_date?: string; end_date?: string }) =>
      apiGet("/analytics/revenue", params),

    profit: (params?: { start_date?: string; end_date?: string }) =>
      apiGet("/analytics/profit", params),

    inventoryValue: () =>
      apiGet("/analytics/inventory-value"),

    salesTrend: (params?: { days?: number }) =>
      apiGet("/analytics/sales-trend", params),

    categoryRevenue: (params?: { start_date?: string; end_date?: string }) =>
      apiGet("/analytics/category-revenue", params),

    performers: (params?: { limit?: number }) =>
      apiGet("/analytics/performers", params),

    stockAlerts: () =>
      apiGet("/analytics/stock-alerts"),

    productAge: () =>
      apiGet("/analytics/product-age"),

    cashFlow: (params?: { days?: number }) =>
      apiGet("/analytics/cash-flow", params),

    priceVariance: () =>
      apiGet("/analytics/price-variance"),

    creditHealth: () =>
      apiGet("/analytics/credit-health"),

    forecast: (params?: { days?: number; sku_id?: string }) =>
      apiGet("/analytics/forecast", params),

    suggestions: () =>
      apiGet("/analytics/suggestions"),

    dashboard: () =>
      apiGet("/analytics/dashboard"),
  }
};
