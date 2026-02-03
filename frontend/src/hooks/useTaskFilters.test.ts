/**
 * Hook tests for useTaskFilters
 * Spec: 002-todo-organization-features
 * Task: T085
 */

import { renderHook, act } from "@testing-library/react";
import { useTaskFilters } from "./useTaskFilters";

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe("useTaskFilters", () => {
  beforeEach(() => {
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
  });

  it("should initialize with default values", () => {
    const { result } = renderHook(() => useTaskFilters());

    expect(result.current.filters).toEqual({
      status: "all",
      priority: "all",
      tags: [],
      noTags: false,
    });
    expect(result.current.search).toBe("");
    expect(result.current.sort).toBe("priority");
    expect(result.current.hasActiveFilters).toBe(false);
  });

  it("should update filters correctly", () => {
    const { result } = renderHook(() => useTaskFilters());

    act(() => {
      result.current.setFilters({
        status: "pending",
        priority: "high",
        tags: ["work"],
        noTags: false,
      });
    });

    expect(result.current.filters.status).toBe("pending");
    expect(result.current.filters.priority).toBe("high");
    expect(result.current.filters.tags).toEqual(["work"]);
  });

  it("should update search correctly", () => {
    const { result } = renderHook(() => useTaskFilters());

    act(() => {
      result.current.setSearch("test search");
    });

    expect(result.current.search).toBe("test search");
  });

  it("should update sort correctly", () => {
    const { result } = renderHook(() => useTaskFilters());

    act(() => {
      result.current.setSort("title");
    });

    expect(result.current.sort).toBe("title");
  });

  it("should save sort to localStorage when changed", () => {
    const { result } = renderHook(() => useTaskFilters());

    act(() => {
      result.current.setSort("title");
    });

    expect(localStorageMock.setItem).toHaveBeenCalledWith("todo-sort-preference", "title");
  });

  it("should load sort from localStorage if available", () => {
    localStorageMock.getItem.mockReturnValue("title");

    const { result } = renderHook(() => useTaskFilters());

    expect(result.current.sort).toBe("title");
  });

  it("should use default sort if localStorage value is invalid", () => {
    localStorageMock.getItem.mockReturnValue("invalid-sort");

    const { result } = renderHook(() => useTaskFilters());

    expect(result.current.sort).toBe("priority"); // Default value
  });

  it("should detect active filters correctly", () => {
    const { result } = renderHook(() => useTaskFilters());

    // Initially no active filters
    expect(result.current.hasActiveFilters).toBe(false);

    // Set search - should be active
    act(() => {
      result.current.setSearch("test");
    });
    expect(result.current.hasActiveFilters).toBe(true);

    // Clear search, set status filter - should be active
    act(() => {
      result.current.setSearch("");
      result.current.setFilters({
        ...result.current.filters,
        status: "pending",
      });
    });
    expect(result.current.hasActiveFilters).toBe(true);

    // Clear all filters - should not be active
    act(() => {
      result.current.setFilters({
        status: "all",
        priority: "all",
        tags: [],
        noTags: false,
      });
    });
    expect(result.current.hasActiveFilters).toBe(false);
  });

  it("should clear all filters correctly", () => {
    const { result } = renderHook(() => useTaskFilters());

    // Set some filters
    act(() => {
      result.current.setFilters({
        status: "pending",
        priority: "high",
        tags: ["work"],
        noTags: true,
      });
      result.current.setSearch("test");
    });

    // Verify filters are active
    expect(result.current.hasActiveFilters).toBe(true);

    // Clear filters
    act(() => {
      result.current.clearFilters();
    });

    // Verify filters are cleared
    expect(result.current.filters).toEqual({
      status: "all",
      priority: "all",
      tags: [],
      noTags: false,
    });
    expect(result.current.search).toBe("");
    expect(result.current.hasActiveFilters).toBe(false);
  });

  it("should maintain sort when clearing filters", () => {
    const { result } = renderHook(() => useTaskFilters());

    // Change sort
    act(() => {
      result.current.setSort("title");
    });

    // Set some filters and clear them
    act(() => {
      result.current.setFilters({
        status: "pending",
        priority: "high",
        tags: ["work"],
        noTags: false,
      });
      result.current.clearFilters();
    });

    // Sort should remain the same
    expect(result.current.sort).toBe("title");
  });
});
