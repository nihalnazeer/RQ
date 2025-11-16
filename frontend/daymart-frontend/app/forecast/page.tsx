"use client";

import TopNav from "@/components/home/TopNav";
import ForecastKPIs from "@/components/forecast/ForecastKPIs";
import ForecastMainChart from "@/components/forecast/ForecastMainChart";
import ForecastScenarioControls from "@/components/forecast/ForecastScenarioControls";

export default function ForecastPage() {
  return (
    <main className="min-h-screen w-full bg-black text-white font-sans">
      {/* NAVBAR */}
      <TopNav />

      {/* PAGE CONTENT */}
      <div className="pt-32 px-10 space-y-12 max-w-7xl mx-auto animate-fade-in">
        {/* KPI STRIP */}
        <ForecastKPIs />

        {/* MAIN FORECAST GRAPH */}
        <ForecastMainChart />

        {/* SCENARIO & SETTINGS */}
        <ForecastScenarioControls />
      </div>
    </main>
  );
}
