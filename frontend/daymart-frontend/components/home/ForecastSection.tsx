"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function ForecastSection() {
  return (
    <section className="mt-10">
      <Card className="bg-white text-black rounded-xl shadow-lg border-0">
        <CardHeader>
          <CardTitle>Sales Forecast</CardTitle>
        </CardHeader>

        <CardContent className="h-64 flex items-center justify-center">
          <p className="text-black/50">Forecast graph will appear here</p>
        </CardContent>
      </Card>
    </section>
  );
}
