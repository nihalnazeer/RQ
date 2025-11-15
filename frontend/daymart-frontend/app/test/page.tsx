"use client";
import { useState } from "react";

export default function TestBackend() {
  const [data, setData] = useState(null);

  const testBackend = async () => {
    const res = await fetch("http://127.0.0.1:8000/health");
    const json = await res.json();
    setData(json);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Test Backend API</h1>
      <button 
        style={{ padding: "10px 20px", background: "black", color: "white" }}
        onClick={testBackend}
      >
        Test Backend
      </button>

      <pre style={{ marginTop: 20 }}>
        {data ? JSON.stringify(data, null, 2) : "Click the button to test."}
      </pre>
    </div>
  );
}
