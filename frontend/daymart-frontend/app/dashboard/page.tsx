"use client";

import { useEffect, useState } from "react";
import { apiGet } from "@/lib/api";

export default function Dashboard() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    apiGet("/health")
      .then((data) => setHealth(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Daymart Dashboard</h1>

      <div style={{ marginTop: 20 }}>
        <h2>Backend Status</h2>
        <pre>{JSON.stringify(health, null, 2)}</pre>
      </div>
    </div>
  );
}
