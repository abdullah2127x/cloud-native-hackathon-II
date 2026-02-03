import type { Todo } from "@/types/task";

/**
 * T060: Updated to use CSS theme variables instead of hardcoded Tailwind colors
 * Variables are defined in frontend/src/app/globals.css with light and dark mode support
 */
export interface PriorityConfig {
  label: string;
  color: string;
  bgColor: string;
  textColor: string;
  variant: "destructive" | "warning" | "success" | "secondary";
  /** CSS variables for theme-aware styling */
  bgVar: string;
  textVar: string;
}

export const priorityColors: Record<
  Todo["priority"],
  PriorityConfig
> = {
  high: {
    label: "High",
    color: "destructive",
    bgColor: "bg-red-50 dark:bg-red-950",
    textColor: "text-red-700 dark:text-red-300",
    variant: "destructive",
    // T060: Use CSS variables for dynamic theming
    bgVar: "var(--priority-high-bg)",
    textVar: "var(--priority-high-text)",
  },
  medium: {
    label: "Medium",
    color: "warning",
    bgColor: "bg-yellow-50 dark:bg-yellow-950",
    textColor: "text-yellow-700 dark:text-yellow-300",
    variant: "warning",
    // T060: Use CSS variables for dynamic theming
    bgVar: "var(--priority-medium-bg)",
    textVar: "var(--priority-medium-text)",
  },
  low: {
    label: "Low",
    color: "success",
    bgColor: "bg-green-50 dark:bg-green-950",
    textColor: "text-green-700 dark:text-green-300",
    variant: "success",
    // T060: Use CSS variables for dynamic theming
    bgVar: "var(--priority-low-bg)",
    textVar: "var(--priority-low-text)",
  },
  none: {
    label: "None",
    color: "secondary",
    bgColor: "bg-gray-50 dark:bg-gray-900",
    textColor: "text-gray-700 dark:text-gray-300",
    variant: "secondary",
    // T060: Use CSS variables for dynamic theming
    bgVar: "var(--priority-none-bg)",
    textVar: "var(--priority-none-text)",
  },
};

export function getPriorityConfig(
  priority: Todo["priority"]
): PriorityConfig {
  return priorityColors[priority] || priorityColors.none;
}

export function getPriorityColor(priority: Todo["priority"]): string {
  return getPriorityConfig(priority).color;
}
