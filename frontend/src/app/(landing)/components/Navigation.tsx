"use client";

import Link from "next/link";
import { Button } from "@/components/ui/Button";
import { CheckSquare } from "lucide-react";

export function Navigation() {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-xl">
          <div className="bg-purple-600 p-2 rounded-lg">
            <CheckSquare className="w-5 h-5 text-white" />
          </div>
          <span>TaskHub</span>
        </Link>

        {/* Auth Actions */}
        <div className="flex items-center gap-3">
          <Link href="/sign-in">
            <Button variant="ghost">Sign In</Button>
          </Link>
          <Link href="/sign-up">
            <Button className="bg-purple-600 hover:bg-purple-700">Get Started</Button>
          </Link>
        </div>
      </div>
    </nav>
  );
}
