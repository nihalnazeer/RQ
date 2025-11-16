"use client";

export default function ProductDetailsPanel({ product }: any) {
  // placeholder dummy data for UI preview
  const dummy = {
    stock: 120,
    avgAge: "14 days",
    cost: 42,
    price: 55,
    margin: "23%",
    movement30: 88,
    alerts: ["Overstocked", "High avg age"],
  };

  return (
    <div className="w-full rounded-2xl bg-white text-black p-8 shadow-2xl space-y-8">

      {/* TITLE */}
      <div>
        <h1 className="text-3xl font-bold">{product.name}</h1>
        <p className="text-gray-700">SKU: {product.sku}</p>
      </div>

      {/* GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* BASIC INFO */}
        <div className="rounded-xl bg-gray-100 p-5 space-y-2">
          <h2 className="text-xl font-semibold">Basic Info</h2>
          <p><strong>Category:</strong> {product.category}</p>
          <p><strong>Average Age:</strong> {dummy.avgAge}</p>
          <p><strong>Stock Level:</strong> {dummy.stock} units</p>
        </div>

        {/* PRICING */}
        <div className="rounded-xl bg-gray-100 p-5 space-y-2">
          <h2 className="text-xl font-semibold">Pricing</h2>
          <p><strong>Cost Price:</strong> ₹{dummy.cost}</p>
          <p><strong>Selling Price:</strong> ₹{dummy.price}</p>
          <p><strong>Margin:</strong> {dummy.margin}</p>
        </div>

        {/* MOVEMENT */}
        <div className="rounded-xl bg-gray-100 p-5 space-y-2">
          <h2 className="text-xl font-semibold">Movement</h2>
          <p><strong>Last 30 days sold:</strong> {dummy.movement30}</p>
        </div>

        {/* ALERTS */}
        <div className="rounded-xl bg-gray-100 p-5 space-y-2">
          <h2 className="text-xl font-semibold">Alerts</h2>
          {dummy.alerts.map((a: string, i: number) => (
            <p key={i} className="text-red-600 font-medium">
              • {a}
            </p>
          ))}
        </div>

      </div>
    </div>
  );
}
