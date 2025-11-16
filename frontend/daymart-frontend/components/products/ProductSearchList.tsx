"use client";

export default function ProductSearchList({ results, onSelect }: any) {
  return (
    <div className="mt-3 w-full rounded-xl bg-white/5 backdrop-blur-xl 
                    border border-white/10 shadow-xl divide-y divide-white/10">
      {results.map((item: any, i: number) => (
        <button
          key={i}
          onClick={() => onSelect(item)}
          className="w-full text-left px-4 py-3 hover:bg-white/10 transition"
        >
          <p className="text-white font-medium">{item.name}</p>
          <p className="text-white/60 text-sm">{item.sku}</p>
        </button>
      ))}
    </div>
  );
}
