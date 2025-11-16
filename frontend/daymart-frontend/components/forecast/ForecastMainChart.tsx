"use client";

import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend
);

export default function ForecastMainChart() {
  const data = {
    labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    datasets: [
      {
        label: "Historic Sales",
        data: [120, 140, 160, 200, 230, 250],
        borderColor: "rgba(255,255,255,0.9)",
        tension: 0.4,
      },
      {
        label: "Forecast",
        data: [null, null, null, 230, 260, 310],
        borderColor: "rgba(255,255,255,0.35)",
        borderDash: [8, 6],
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6">
      <h2 className="text-xl font-semibold mb-4">Sales Forecast</h2>
      <Line data={data} />
    </div>
  );
}
