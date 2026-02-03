"use client";

import { Menu } from "lucide-react";
import { Button } from "@/components/ui/Button";

interface DashboardNavProps {
  onMenuToggle: () => void;
}

export function DashboardNav({ onMenuToggle }: DashboardNavProps) {
  return (
    <nav className="sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 md:px-8 h-16 flex items-center gap-4">
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
