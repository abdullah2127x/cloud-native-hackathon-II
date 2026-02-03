import type { Todo } from "@/types/task";

export interface PriorityConfig {
  label: string;
  color: string;
  bgColor: string;
  textColor: string;
  variant: "destructive" | "warning" | "success" | "secondary";
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
  },
  medium: {
    label: "Medium",
    color: "warning",
    bgColor: "bg-yellow-50 dark:bg-yellow-950",
    textColor: "text-yellow-700 dark:text-yellow-300",
    variant: "warning",
  },
  low: {
    label: "Low",
    color: "success",
    bgColor: "bg-green-50 dark:bg-green-950",
    textColor: "text-green-700 dark:text-green-300",
    variant: "success",
  },
  none: {
    label: "None",
    color: "secondary",
    bgColor: "bg-gray-50 dark:bg-gray-900",
    textColor: "text-gray-700 dark:text-gray-300",
    variant: "secondary",
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
