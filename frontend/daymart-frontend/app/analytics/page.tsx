"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function AnalyticsTest() {
  const [revenue, setRevenue] = useState(null);

  useEffect(() => {
    apiGet("/api/v1/analytics/revenue")
      .then(setRevenue)
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Analytics Test</h1>
      <pre>{JSON.stringify(revenue, null, 2)}</pre>
    </div>
  );
}
