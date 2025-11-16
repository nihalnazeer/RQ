"use client";

import { useState, useEffect } from "react";
import WelcomeSplash from "@/components/ui/WelcomeSplash";
import TopNav from "@/components/home/TopNav";
import KPISection from "@/components/home/KPISection";
import ForecastSection from "@/components/home/ForecastSection";
import ActionCenter from "@/components/home/ActionCenter";

export default function HomePage() {
  const [showSplash, setShowSplash] = useState(false);
  const [mounted, setMounted] = useState(false); // smooth fade animation

  useEffect(() => {
    setMounted(true); // enables fade-in animation
  }, []);

  useEffect(() => {
    const hasSeenSplash = sessionStorage.getItem("seenSplash");

    if (!hasSeenSplash) {
      setShowSplash(true);
      sessionStorage.setItem("seenSplash", "true");

      const timer = setTimeout(() => setShowSplash(false), 2500);
      return () => clearTimeout(timer);
    }
  }, []);

  return (
    <main className="min-h-screen w-full bg-black text-white font-sans">

      {/* --- SPLASH SCREEN (first visit only) --- */}
      {showSplash && <WelcomeSplash />}

      {/* --- MAIN CONTENT --- */}
      {!showSplash && (
        <div
          className={`transition-opacity duration-700 ${
            mounted ? "opacity-100" : "opacity-0"
          }`}
        >
          <TopNav />

          {/* Unified layout spacing matching Financials */}
          <div className="pt-32 px-10 space-y-12 max-w-7xl mx-auto">

            <KPISection />

            <ForecastSection />

            <ActionCenter />
          </div>
        </div>
      )}
    </main>
  );
}
