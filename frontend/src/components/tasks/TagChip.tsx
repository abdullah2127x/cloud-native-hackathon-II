/**
 * TagChip component - Clickable tag display
 * Spec: 002-todo-organization-features
 * Task: T054
 */

import React from "react";
import { X } from "lucide-react";

interface TagChipProps {
  name: string;
  onRemove?: () => void;  // Show X button if provided
  onClick?: () => void;   // Click to filter
}

export function TagChip({ name, onRemove, onClick }: TagChipProps) {
  const [isHovered, setIsHovered] = React.useState(false);

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling if used in a clickable container
    if (onClick) {
      onClick();
    }
  };

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium border cursor-pointer transition-colors ${
        onClick ? "hover:underline" : ""
      }`}
      style={{
        backgroundColor: isHovered ? "var(--primary)" : "var(--accent)",
        color: isHovered ? "var(--primary-foreground)" : "var(--foreground)",
        borderColor: "var(--border)",
      }}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      aria-label={`Tag: ${name}${onRemove ? ", removable" : ""}`}
    >
      {name}
      {onRemove && (
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onRemove();
          }}
          className="ml-1 focus:outline-none transition-colors hover:opacity-70"
          style={{ color: isHovered ? "var(--primary-foreground)" : "var(--foreground)" }}
          aria-label={`Remove tag ${name}`}
        >
          <X size={12} />
        </button>
      )}
    </span>
  );
}
