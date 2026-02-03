/**
 * SortSelector component - Sort options
 * Spec: 002-todo-organization-features
 * Task: T102
 */

import { SortField } from "@/types/task";
import { SORT_LABELS } from "@/lib/validations/task";

interface SortSelectorProps {
  value: SortField;
  onChange: (value: SortField) => void;
}

export function SortSelector({ value, onChange }: SortSelectorProps) {
  return (
    <div>
      {/* T062: Replace hardcoded colors with theme variables */}
      <label className="block text-sm font-medium mb-1" style={{ color: "var(--foreground)" }}>
        Sort by
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as SortField)}
        className="w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-1 transition"
        style={{
          backgroundColor: "var(--input-bg)",
          borderColor: "var(--input-border)",
          color: "var(--input-text)",
        }}
        onFocus={(e) => {
          e.currentTarget.style.borderColor = "var(--primary)";
          e.currentTarget.style.boxShadow = "0 0 0 1px var(--primary)";
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = "var(--input-border)";
          e.currentTarget.style.boxShadow = "none";
        }}
      >
        <option value="priority">{SORT_LABELS.priority}</option>
        <option value="title">{SORT_LABELS.title}</option>
        <option value="created_at">{SORT_LABELS.created_at}</option>
      </select>
    </div>
  );
}
