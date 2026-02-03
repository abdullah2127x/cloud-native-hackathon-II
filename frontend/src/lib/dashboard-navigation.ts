import { LayoutDashboard, CheckSquare, Flag, Tag, Settings } from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface NavigationSection {
  id: string;
  label: string;
  icon: LucideIcon;
  href: string;
  badge?: number;
}

export const navigationSections: NavigationSection[] = [
  {
    id: "overview",
    label: "Overview",
    icon: LayoutDashboard,
    href: "/dashboard/overview",
  },
  {
    id: "todos",
    label: "All Todos",
    icon: CheckSquare,
    href: "/dashboard/todos",
  },
  {
    id: "priority",
    label: "By Priority",
    icon: Flag,
    href: "/dashboard/priority",
  },
  {
    id: "tags",
    label: "By Tags",
    icon: Tag,
    href: "/dashboard/tags",
  },
  {
    id: "settings",
    label: "Settings",
    icon: Settings,
    href: "/dashboard/settings",
  },
];

export function getActiveSection(pathname: string): string | null {
  for (const section of navigationSections) {
    if (pathname.startsWith(section.href)) {
      return section.id;
    }
  }
  return null;
}
