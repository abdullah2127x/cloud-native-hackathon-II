"use client";

import { Menu } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface DashboardNavProps {
  onMenuToggle: () => void;
}

export function DashboardNav({ onMenuToggle }: DashboardNavProps) {
  return (
    // T024: Use semantic theme variables for DashboardNav
    <nav
      className="sticky top-0 z-40 border-b px-4 md:px-8 h-16 flex items-center gap-4 transition"
      style={{
        backgroundColor: "var(--background)",
        borderColor: "var(--border)",
      }}
    >
      {/* Mobile Menu Button */}
      <Button
        variant="ghost"
        size="sm"
        className="md:hidden"
        onClick={onMenuToggle}
      >
        <Menu className="h-6 w-6" />
      </Button>

      {/* Spacer */}
      <div className="flex-1" />
    </nav>
  );
}
