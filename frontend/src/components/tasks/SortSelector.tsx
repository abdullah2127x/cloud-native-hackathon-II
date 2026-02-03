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
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Sort by
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value as SortField)}
        className="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        <option value="priority">{SORT_LABELS.priority}</option>
        <option value="title">{SORT_LABELS.title}</option>
        <option value="created_at">{SORT_LABELS.created_at}</option>
      </select>
    </div>
  );
}
