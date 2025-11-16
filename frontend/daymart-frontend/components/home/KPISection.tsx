"use client";

import { useEffect, useState } from "react";
import { API } from "@/lib/api";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

type KPIData = {
  revenue: number | null;
  stockAge: number | null;
  creditHealth: number | null;
  inventoryValue: number | null;
};

export default function KPISection() {
  const [loading, setLoading] = useState(true);

  const [kpi, setKpi] = useState<KPIData>({
    revenue: null,
    stockAge: null,
    creditHealth: null,
    inventoryValue: null,
  });

  useEffect(() => {
    async function loadKPIs() {
      try {
        const [revenue, stockAge, credit, inventory] = await Promise.all([
          API.revenue(),
          API.stockAge(),
          API.creditHealth(),
          API.inventoryValue(),
        ]);

        setKpi({
          revenue: revenue.total_revenue,
          stockAge: stockAge.average_age,
          creditHealth: credit.score,
          inventoryValue: inventory.total_value,
        });
      } catch (e) {
        console.error("KPI fetch error:", e);
      } finally {
        setLoading(false);
      }
    }

    loadKPIs();
  }, []);

  const kpiList = [
    {
      label: "Total Revenue",
      value:
        typeof kpi.revenue === "number"
          ? `₹${kpi.revenue.toLocaleString()}`
          : "—",
    },
    {
      label: "Avg Stock Age",
      value:
        typeof kpi.stockAge === "number" ? `${kpi.stockAge} days` : "—",
    },
    {
      label: "Credit Health",
      value: kpi.creditHealth ?? "—",
    },
    {
      label: "Inventory Value",
      value:
        typeof kpi.inventoryValue === "number"
          ? `₹${kpi.inventoryValue.toLocaleString()}`
          : "—",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
      {kpiList.map((item) => (
        <Card
          key={item.label}
          className="bg-white/5 backdrop-blur-lg border border-white/10 rounded-2xl transition hover:bg-white/10"
        >
          <CardHeader>
            <CardTitle className="text-white/80 text-sm">{item.label}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-semibold text-white">
              {loading ? "…" : item.value}
            </p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
