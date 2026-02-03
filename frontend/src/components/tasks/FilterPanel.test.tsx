/**
 * Component tests for FilterPanel
 * Spec: 002-todo-organization-features
 * Task: T084
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { FilterPanel } from "./FilterPanel";

describe("FilterPanel", () => {
  const mockFilters = {
    status: "all",
    priority: "all",
    tags: [],
    noTags: false,
  };

  const mockOnFiltersChange = jest.fn();
  const mockOnClearFilters = jest.fn();

  beforeEach(() => {
    mockOnFiltersChange.mockClear();
    mockOnClearFilters.mockClear();
  });

  it("renders all filter controls", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    expect(screen.getByLabelText("Status")).toBeInTheDocument();
    expect(screen.getByLabelText("Priority")).toBeInTheDocument();
    expect(screen.getByText("Select tags...")).toBeInTheDocument();
  });

  it("renders status options correctly", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    const statusSelect = screen.getByLabelText("Status");
    expect(statusSelect).toHaveValue("all");
  });

  it("renders priority options correctly", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    const prioritySelect = screen.getByLabelText("Priority");
    expect(prioritySelect).toHaveValue("all");
  });

  it("changes status filter when selected", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    const statusSelect = screen.getByLabelText("Status");
    fireEvent.change(statusSelect, { target: { value: "pending" } });

    expect(mockOnFiltersChange).toHaveBeenCalledWith({
      ...mockFilters,
      status: "pending",
    });
  });

  it("changes priority filter when selected", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    const prioritySelect = screen.getByLabelText("Priority");
    fireEvent.change(prioritySelect, { target: { value: "high" } });

    expect(mockOnFiltersChange).toHaveBeenCalledWith({
      ...mockFilters,
      priority: "high",
    });
  });

  it("toggles tags in filter", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={["work", "personal"]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    // Click to open tag dropdown
    fireEvent.click(screen.getByText("Select tags..."));

    // Click on a tag to add it
    fireEvent.click(screen.getByText("work"));

    expect(mockOnFiltersChange).toHaveBeenCalledWith({
      ...mockFilters,
      tags: ["work"],
    });
  });

  it("removes tags from filter", () => {
    const filtersWithTags = {
      ...mockFilters,
      tags: ["work"],
    };

    render(
      <FilterPanel
        filters={filtersWithTags}
        onFiltersChange={mockOnFiltersChange}
        availableTags={["work", "personal"]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={true}
      />
    );

    // Click the remove button for the tag
    const removeButton = screen.getByLabelText("Remove tag work");
    fireEvent.click(removeButton);

    expect(mockOnFiltersChange).toHaveBeenCalledWith({
      ...mockFilters,
      tags: [],
    });
  });

  it("toggles no tags filter", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={["work"]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    // Click to open tag dropdown
    fireEvent.click(screen.getByText("Select tags..."));

    // Click on "No tags" option
    fireEvent.click(screen.getByText("No tags"));

    expect(mockOnFiltersChange).toHaveBeenCalledWith({
      ...mockFilters,
      noTags: true,
    });
  });

  it("shows clear filters button when filters are active", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={true}
      />
    );

    const clearButton = screen.getByText("Clear All Filters");
    expect(clearButton).toBeInTheDocument();
  });

  it("does not show clear filters button when no filters are active", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={false}
      />
    );

    const clearButton = screen.queryByText("Clear All Filters");
    expect(clearButton).not.toBeInTheDocument();
  });

  it("calls onClearFilters when clear button is clicked", () => {
    render(
      <FilterPanel
        filters={mockFilters}
        onFiltersChange={mockOnFiltersChange}
        availableTags={[]}
        onClearFilters={mockOnClearFilters}
        hasActiveFilters={true}
      />
    );

    const clearButton = screen.getByText("Clear All Filters");
    fireEvent.click(clearButton);

    expect(mockOnClearFilters).toHaveBeenCalled();
  });
});
