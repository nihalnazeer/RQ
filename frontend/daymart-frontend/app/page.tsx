"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((res) => res.json())
      .then((d) => setData(d))
      .catch((err) => setError("Failed to connect to backend"));
  }, []);

  return (
    <div style={{ padding: 40 }}>
      <h1>Testing Backend Connection</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
