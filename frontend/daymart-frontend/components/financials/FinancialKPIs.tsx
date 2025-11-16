"use client";

export default function FinancialKPIs() {
  const KPIs = [
    { label: "Total Revenue", value: "₹ 0" },
    { label: "Current Inventory Value", value: "₹ 0" },
    { label: "Total Profit Margin", value: "0%" },
    { label: "Purchase Price Variance", value: "0%" },
    { label: "Inventory Value vs Cash Outflow", value: "₹ 0" },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 xl:grid-cols-5 gap-6">
      {KPIs.map((kpi, idx) => (
        <div
          key={idx}
          className="rounded-xl bg-white/5 border border-white/10 p-5 backdrop-blur-md shadow-lg"
        >
          <p className="text-sm text-white/60">{kpi.label}</p>
          <p className="text-2xl font-semibold text-white mt-1">
            {kpi.value}
          </p>
        </div>
      ))}
    </div>
  );
}
