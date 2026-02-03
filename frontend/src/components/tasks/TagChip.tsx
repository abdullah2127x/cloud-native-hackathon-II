/**
 * TagChip component - Clickable tag display
 * Spec: 002-todo-organization-features
 * Task: T054
 */

import { X } from "lucide-react";

interface TagChipProps {
  name: string;
  onRemove?: () => void;  // Show X button if provided
  onClick?: () => void;   // Click to filter
}

export function TagChip({ name, onRemove, onClick }: TagChipProps) {
  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent event bubbling if used in a clickable container
    if (onClick) {
      onClick();
    }
  };

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200 cursor-pointer hover:bg-blue-200 transition-colors ${
        onClick ? "hover:underline" : ""
      }`}
      onClick={handleClick}
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
          className="ml-1 text-blue-600 hover:text-blue-800 focus:outline-none"
          aria-label={`Remove tag ${name}`}
        >
          <X size={12} />
        </button>
      )}
    </span>
  );
}
