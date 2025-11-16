"use client";

export default function ForecastScenarioControls() {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-xl p-6 space-y-6">
      <h2 className="text-xl font-semibold">Scenario Simulator</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* A. Adjust Demand Growth */}
        <div>
          <label className="text-sm text-white/60">Demand Change (%)</label>
          <input
            type="range"
            min="-20"
            max="20"
            defaultValue="0"
            className="w-full mt-2"
          />
        </div>

        {/* B. Pricing Change */}
        <div>
          <label className="text-sm text-white/60">Price Variation (%)</label>
          <input
            type="range"
            min="-15"
            max="15"
            defaultValue="0"
            className="w-full mt-2"
          />
        </div>

        {/* C. Promotion Model */}
        <div>
          <label className="text-sm text-white/60">Promotion Strategy</label>
          <select className="w-full mt-2 bg-black border border-white/20 p-2 rounded-xl">
            <option>No promotion</option>
            <option>5% discount</option>
            <option>Combo deals</option>
            <option>High-frequency items only</option>
          </select>
        </div>
      </div>

      <button className="w-full rounded-xl py-3 bg-white/10 hover:bg-white/20 transition">
        Recalculate Forecast
      </button>
    </div>
  );
}
