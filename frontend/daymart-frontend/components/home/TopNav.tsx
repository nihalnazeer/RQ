"use client";

import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect, useRef } from "react";

export default function TopNav() {
  const navItems = [
    { label: "Home", path: "/" },
    { label: "Financials", path: "/financials" },
    { label: "Forecast", path: "/forecast" },
    { label: "Products", path: "/products" },
  ];

  const pathname = usePathname();

  // --- Scroll Visibility State ---
  const [visible, setVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  // --- Dropdown State ---
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // --- Effect for Scroll Detection ---
  useEffect(() => {
    const controlNavbar = () => {
      if (typeof window !== "undefined") {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
          setVisible(false);
          setIsDropdownOpen(false); // Close dropdown on scroll
        } else {
          setVisible(true);
        }
        setLastScrollY(window.scrollY);
      }
    };

    if (typeof window !== "undefined") {
      window.addEventListener("scroll", controlNavbar);
      return () => {
        window.removeEventListener("scroll", controlNavbar);
      };
    }
  }, [lastScrollY]);

  // --- Effect for Click-Outside-to-Close Dropdown ---
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [dropdownRef]);

  return (
    <nav
      className={cn(
        "fixed top-6 left-0 right-0 z-50 mx-auto max-w-2xl",
        "rounded-full",
        // --- GLOW EFFECT REDUCED HERE ---
        "border border-emerald-600/15", // Border opacity reduced to 15%
        "bg-black/50 backdrop-blur-lg",
        "shadow-[0_0_25px_rgba(16,185,129,0.25)]", // Glow opacity reduced to 25%
        // --- END GLOW EFFECT ---
        "transition-all duration-300 ease-in-out",
        visible
          ? "translate-y-0 opacity-100"
          : "-translate-y-24 opacity-0"
      )}
    >
      <div className="flex h-14 w-full items-center justify-between px-6">
        {/* --- Left: Logo --- */}
        <Link
          href="/"
          className="text-lg font-bold text-white transition-colors hover:text-white/80"
        >
          Blacklane
        </Link>

        {/* --- Center: Nav Links --- */}
        <div className="flex items-center gap-2">
          {navItems.map((item) => {
            const isActive = pathname === item.path;
            return (
              <Link
                key={item.path}
                href={item.path}
                className={cn(
                  "rounded-full px-4 py-1.5 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-white/10 text-white"
                    : "text-white/70 hover:text-white"
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </div>

        {/* --- Right: Profile Dropdown --- */}
        <div className="relative" ref={dropdownRef}>
          {/* Avatar Button */}
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className={cn(
              "flex h-9 w-9 items-center justify-center rounded-full",
              "border border-white/10 bg-white/5",
              "text-white/70 transition-colors hover:border-white/20 hover:text-white"
            )}
            aria-label="Open user menu"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="h-5 w-5"
            >
              <path d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.095a1.23 1.23 0 00.41-1.412A9.99 9.99 0 0010 12.75a9.99 9.99 0 00-6.535 1.743z" />
            </svg>
          </button>

          {/* Dropdown Menu */}
          {isDropdownOpen && (
            <div
              className={cn(
                "absolute right-0 top-12 z-50 w-56",
                "origin-top-right rounded-xl border border-white/10",
                "bg-black/80 p-3 backdrop-blur-xl shadow-2xl",
                "flex flex-col gap-1"
              )}
            >
              <div className="px-2 py-1">
                <p className="font-semibold text-white">Mr. Aashiq</p>
                <p className="text-sm text-white/70">Operational Head</p>
              </div>
              <div className="my-1 h-px bg-white/10" />
              <button className="rounded-md px-2 py-1.5 text-left text-sm text-white/70 hover:bg-white/10 hover:text-white">
                Settings
              </button>
              <button className="rounded-md px-2 py-1.5 text-left text-sm text-red-400 hover:bg-red-500/20">
                Sign Out
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}