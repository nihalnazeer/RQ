"use client";

export default function ForecastKPIs() {
  const cards = [
    { label: "Projected Revenue (Next 30 Days)", value: "₹14.2M" },
    { label: "Expected Footfall Increase", value: "+6.8%" },
    { label: "Forecast Accuracy (Last Quarter)", value: "92%" },
    { label: "Top Category Trend", value: "Fresh Produce ↑" },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
      {cards.map((c) => (
        <div
          key={c.label}
          className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6
          hover:bg-white/[0.07] transition-all"
        >
          <p className="text-sm text-white/60">{c.label}</p>
          <p className="text-2xl font-semibold mt-2">{c.value}</p>
        </div>
      ))}
    </div>
  );
}
