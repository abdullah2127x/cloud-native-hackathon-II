/**
 * useTaskFilters hook - Manages task filters state
 * Spec: 002-todo-organization-features
 * Task: T086
 */

import { useState, useEffect } from "react";
import type { TaskFilters, SortField, SortOrder } from "@/types/task";
import { DEFAULT_SORT_ORDER, STORAGE_KEYS } from "@/lib/validations/task";

interface UseTaskFiltersReturn {
  filters: TaskFilters;
  setFilters: (filters: TaskFilters) => void;
  search: string;
  setSearch: (search: string) => void;
  sort: SortField;
  setSort: (sort: SortField) => void;
  clearFilters: () => void;
  hasActiveFilters: boolean;
}

export function useTaskFilters(): UseTaskFiltersReturn {
  const [filters, setFilters] = useState<TaskFilters>({
    status: "all",
    priority: "all",
    tags: [],
    noTags: false,
  });

  const [search, setSearch] = useState<string>("");
  const [sort, setSort] = useState<SortField>(() => {
    // Load sort preference from localStorage
    if (typeof window !== "undefined") {
      const savedSort = localStorage.getItem(STORAGE_KEYS.SORT_PREFERENCE);
      if (savedSort && ["priority", "title", "created_at"].includes(savedSort)) {
        return savedSort as SortField;
      }
    }
    return "priority";
  });

  // Save sort preference to localStorage when it changes
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEYS.SORT_PREFERENCE, sort);
    }
  }, [sort]);

  const clearFilters = () => {
    setFilters({
      status: "all",
      priority: "all",
      tags: [],
      noTags: false,
    });
    setSearch("");
  };

  const hasActiveFilters =
    filters.status !== "all" ||
    filters.priority !== "all" ||
    filters.tags.length > 0 ||
    filters.noTags ||
    search !== "";

  return {
    filters,
    setFilters,
    search,
    setSearch,
    sort,
    setSort,
    clearFilters,
    hasActiveFilters,
  };
}
