"use client";

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export default function ActionCenter() {
  const suggestions = [
    "Product X stock age exceeds 120 days",
    "Category Y showing overstock risk",
    "Consider discounting SKUs with low weekly sell-through",
    "Dead stock detected in 3 categories"
  ];

  return (
    <section className="mt-10 mb-16">
      <Card className="bg-white text-black rounded-xl shadow-lg border-0">
        <CardHeader>
          <CardTitle>Action Suggestion Center</CardTitle>
        </CardHeader>

        <CardContent>
          <ul className="space-y-3">
            {suggestions.map((s, idx) => (
              <li
                key={idx}
                className="p-3 rounded-lg bg-black/5 text-sm"
              >
                {s}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </section>
  );
}
