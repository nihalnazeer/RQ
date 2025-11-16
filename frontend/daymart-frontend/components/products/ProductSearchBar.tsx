"use client";

import { useState } from "react";

export default function ProductSearchBar({ onResults }: any) {
  const [query, setQuery] = useState("");

  // dummy placeholder results
  const ALL_PRODUCTS = [
    { sku: "PTC001", name: "Aashirvaad Atta 5kg", category: "Grocery" },
    { sku: "PTC002", name: "Amul Toned Milk 1L", category: "Dairy" },
    { sku: "PTC003", name: "Colgate 120g", category: "FMCG" },
  ];

  function handleSearch(value: string) {
    setQuery(value);

    if (!value.trim()) {
      onResults([]);
      return;
    }

    const filtered = ALL_PRODUCTS.filter((p) =>
      p.name.toLowerCase().includes(value.toLowerCase()) ||
      p.sku.toLowerCase().includes(value.toLowerCase())
    );

    onResults(filtered);
  }

  return (
    <div className="w-full">
      <input
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search by SKU or product name..."
        className="w-full rounded-xl border border-white/10 bg-white/5 
                   px-4 py-3 text-white placeholder-white/40 
                   focus:outline-none focus:ring-2 focus:ring-white/20"
      />
    </div>
  );
}
