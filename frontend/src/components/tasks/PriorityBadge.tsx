/**
 * PriorityBadge component - Visual priority indicator
 *
 * Spec: 002-todo-organization-features
 * Displays priority level with appropriate color coding
 */

import { PRIORITY_CONFIG, type Priority } from "@/lib/validations/task";

interface PriorityBadgeProps {
  priority: Priority;
  size?: "sm" | "md";
}

export function PriorityBadge({ priority, size = "md" }: PriorityBadgeProps){
  const config = PRIORITY_CONFIG[priority];

  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-2.5 py-1",
  };

  return (
    // T060: Use semantic priority variables for badge colors
    <span
      className={`inline-flex items-center rounded-full border font-medium transition ${sizeClasses[size]}`}
      style={{
        backgroundColor: config.bgVar,
        color: config.textVar,
        borderColor: config.bgVar,
      }}
      aria-label={`Priority: ${config.label}`}
    >
      {config.label}
    </span>
  );
}
