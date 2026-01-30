"use client";

import { usePathname, useRouter } from "next/navigation";
import { useSession, signOut } from "@/lib/auth-client";
import { Button } from "@/components/ui/Button";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { navigationSections, getActiveSection } from "@/lib/dashboard-navigation";
import { LogOut, CheckSquare } from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const { data: session } = useSession();
  const activeSection = getActiveSection(pathname);

  const handleSignOut = async () => {
    await signOut();
    router.push("/sign-in");
  };

  const userInitials = session?.user?.name
    ? session.user.name.split(" ").map((n) => n[0]).join("").toUpperCase()
    : session?.user?.email?.[0]?.toUpperCase() || "U";

  return (
    <div className="h-full flex flex-col overflow-y-auto p-4 space-y-6">
      {/* Logo */}
      <div className="flex items-center gap-2 px-2">
        <div className="bg-purple-600 p-2 rounded-lg">
          <CheckSquare className="w-5 h-5 text-white" />
        </div>
        <span className="font-bold text-lg hidden sm:block">TaskHub</span>
      </div>

      <Separator className="bg-slate-200 dark:bg-slate-700" />

      {/* User Info */}
      <div className="px-2 space-y-3">
        <div className="flex items-center gap-3">
          <Avatar className="h-10 w-10">
            <AvatarFallback className="bg-purple-600 text-white">
              {userInitials}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-semibold text-slate-900 dark:text-white truncate">
              {session?.user?.name || "User"}
            </p>
            <p className="text-xs text-slate-600 dark:text-slate-400 truncate">
              {session?.user?.email}
            </p>
          </div>
        </div>
      </div>

      <Separator className="bg-slate-200 dark:bg-slate-700" />

      {/* Navigation */}
      <nav className="flex-1 space-y-2">
        {navigationSections.map((section) => {
          const Icon = section.icon;
          const isActive = activeSection === section.id;

          return (
            <button
              key={section.id}
              onClick={() => router.push(section.href)}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition ${
                isActive
                  ? "bg-purple-100 dark:bg-purple-900/30 text-purple-900 dark:text-purple-400"
                  : "text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800"
              }`}
            >
              <Icon className="h-5 w-5 flex-shrink-0" />
              <span className="truncate">{section.label}</span>
            </button>
          );
        })}
      </nav>

      <Separator className="bg-slate-200 dark:bg-slate-700" />

      {/* Sign Out Button */}
      <Button
        onClick={handleSignOut}
        variant="outline"
        className="w-full border-slate-300 dark:border-slate-600"
      >
        <LogOut className="h-4 w-4 mr-2" />
        Sign Out
      </Button>
    </div>
  );
}
