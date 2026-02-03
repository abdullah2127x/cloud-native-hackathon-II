/**
 * Priority constants and configuration
 *
 * Spec: 002-todo-organization-features
 * Date: 2026-01-23
 */

import type { Priority } from "@/lib/validations/task";

/**
 * Priority color configuration
 * Maps priority levels to Tailwind CSS classes
 */
export const PRIORITY_COLORS: Record<
  Priority,
  {
    badge: string;
    bg: string;
    text: string;
    border: string;
  }
> = {
  high: {
    badge: "bg-red-100 text-red-800 border-red-200",
    bg: "bg-red-100",
    text: "text-red-800",
    border: "border-red-200",
  },
  medium: {
    badge: "bg-yellow-100 text-yellow-800 border-yellow-200",
    bg: "bg-yellow-100",
    text: "text-yellow-800",
    border: "border-yellow-200",
  },
  low: {
    badge: "bg-blue-100 text-blue-800 border-blue-200",
    bg: "bg-blue-100",
    text: "text-blue-800",
    border: "border-blue-200",
  },
  none: {
    badge: "bg-gray-100 text-gray-600 border-gray-200",
    bg: "bg-gray-100",
    text: "text-gray-600",
    border: "border-gray-200",
  },
};

/**
 * Priority display labels
 */
export const PRIORITY_LABELS: Record<Priority, string> = {
  high: "High",
  medium: "Medium",
  low: "Low",
  none: "None",
};

/**
 * Priority sort order (for client-side sorting)
 */
export const PRIORITY_SORT_ORDER: Record<Priority, number> = {
  high: 0,
  medium: 1,
  low: 2,
  none: 3,
};
