/**
 * FilterPanel component - Task filters
 * Spec: 002-todo-organization-features
 * Task: T087, T088
 */

import { useState } from "react";
import { X } from "lucide-react";
import type { TaskFilters, SortField, SortOrder } from "@/types/task";
import {
  statusFilterValues,
  priorityFilterValues,
  STATUS_FILTER_LABELS,
  PRIORITY_FILTER_LABELS
} from "@/lib/validations/task";

interface FilterPanelProps {
  filters: TaskFilters;
  onFiltersChange: (filters: TaskFilters) => void;
  availableTags: string[];
  onClearFilters: () => void;
  hasActiveFilters: boolean;
}

export function FilterPanel({
  filters,
  onFiltersChange,
  availableTags,
  onClearFilters,
  hasActiveFilters
}: FilterPanelProps) {
  const [showTagDropdown, setShowTagDropdown] = useState(false);

  const handleStatusChange = (status: string) => {
    onFiltersChange({
      ...filters,
      status: status as "all" | "pending" | "completed",
    });
  };

  const handlePriorityChange = (priority: string) => {
    onFiltersChange({
      ...filters,
      priority: priority as "all" | "high" | "medium" | "low" | "none",
    });
  };

  const handleTagToggle = (tagName: string) => {
    const newTags = filters.tags.includes(tagName)
      ? filters.tags.filter(tag => tag !== tagName)
      : [...filters.tags, tagName];

    onFiltersChange({
      ...filters,
      tags: newTags,
    });
  };

  const handleNoTagsToggle = () => {
    onFiltersChange({
      ...filters,
      noTags: !filters.noTags,
    });
  };

  return (
    <div className="mb-4 p-4 bg-white border border-gray-200 rounded-md">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            value={filters.status}
            onChange={(e) => handleStatusChange(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {statusFilterValues.map((status) => (
              <option key={status} value={status}>
                {STATUS_FILTER_LABELS[status]}
              </option>
            ))}
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            value={filters.priority}
            onChange={(e) => handlePriorityChange(e.target.value)}
            className="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            {priorityFilterValues.map((priority) => (
              <option key={priority} value={priority}>
                {PRIORITY_FILTER_LABELS[priority]}
              </option>
            ))}
          </select>
        </div>

        {/* Tags Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tags
          </label>
          <div className="relative">
            <div className="flex flex-wrap gap-1 mb-2 max-h-20 overflow-y-auto">
              {filters.tags.map((tag, index) => (
                <span
                  key={`selected-${tag}-${index}`}
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 border border-blue-200"
                >
                  {tag}
                  <button
                    type="button"
                    onClick={() => handleTagToggle(tag)}
                    className="ml-1 text-blue-600 hover:text-blue-800 focus:outline-none"
                    aria-label={`Remove tag ${tag}`}
                  >
                    <X size={12} />
                  </button>
                </span>
              ))}
              {filters.noTags && (
                <span
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800 border border-gray-200"
                >
                  No tags
                  <button
                    type="button"
                    onClick={handleNoTagsToggle}
                    className="ml-1 text-gray-600 hover:text-gray-800 focus:outline-none"
                    aria-label="Remove 'No tags' filter"
                  >
                    <X size={12} />
                  </button>
                </span>
              )}
            </div>

            <button
              type="button"
              onClick={() => setShowTagDropdown(!showTagDropdown)}
              className="w-full text-left rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              Select tags...
            </button>

            {showTagDropdown && (
              <div className="absolute z-10 mt-1 w-full rounded-md bg-white shadow-lg border border-gray-200 max-h-60 overflow-auto">
                <div className="py-1">
                  {availableTags.map((tag) => (
                    <div
                      key={tag}
                      className={`px-4 py-2 text-sm cursor-pointer ${
                        filters.tags.includes(tag)
                          ? "bg-blue-100 text-blue-800"
                          : "text-gray-700 hover:bg-gray-100"
                      }`}
                      onClick={() => handleTagToggle(tag)}
                    >
                      {tag}
                    </div>
                  ))}
                  {availableTags.length === 0 && (
                    <div className="px-4 py-2 text-sm text-gray-500">
                      No tags available
                    </div>
                  )}

                  {/* "No tags" option */}
                  <div
                    className={`px-4 py-2 text-sm cursor-pointer ${
                      filters.noTags
                        ? "bg-blue-100 text-blue-800"
                        : "text-gray-700 hover:bg-gray-100"
                    }`}
                    onClick={handleNoTagsToggle}
                  >
                    No tags
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Clear Filters Button */}
      {hasActiveFilters && (
        <div className="mt-4 flex justify-end">
          <button
            type="button"
            onClick={onClearFilters}
            className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Clear All Filters
          </button>
        </div>
      )}
    </div>
  );
}
