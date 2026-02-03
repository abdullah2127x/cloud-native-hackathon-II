/**
 * Component tests for SortSelector
 * Spec: 002-todo-organization-features
 * Task: T101
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { SortSelector } from "./SortSelector";

describe("SortSelector", () => {
  it("renders with label", () => {
    render(<SortSelector value="priority" onChange={jest.fn()} />);

    const label = screen.getByText("Sort by");
    expect(label).toBeInTheDocument();
  });

  it("renders with correct options", () => {
    render(<SortSelector value="priority" onChange={jest.fn()} />);

    const select = screen.getByRole("combobox");
    expect(select).toHaveValue("priority");

    const options = screen.getAllByRole("option");
    expect(options).toHaveLength(3);

    const optionValues = options.map(option => option.getAttribute("value"));
    expect(optionValues).toContain("priority");
    expect(optionValues).toContain("title");
    expect(optionValues).toContain("created_at");
  });

  it("has correct default display values", () => {
    render(<SortSelector value="priority" onChange={jest.fn()} />);

    const select = screen.getByRole("combobox");
    expect(select).toHaveValue("priority");
  });

  it("calls onChange when selection changes", () => {
    const mockOnChange = jest.fn();
    render(<SortSelector value="priority" onChange={mockOnChange} />);

    const select = screen.getByRole("combobox");
    fireEvent.change(select, { target: { value: "title" } });

    expect(mockOnChange).toHaveBeenCalledWith("title");
  });

  it("reflects the current value prop", () => {
    const { rerender } = render(<SortSelector value="priority" onChange={jest.fn()} />);

    const select = screen.getByRole("combobox");
    expect(select).toHaveValue("priority");

    rerender(<SortSelector value="title" onChange={jest.fn()} />);
    expect(select).toHaveValue("title");
  });

  it("displays correct options for each sort type", () => {
    const { rerender } = render(<SortSelector value="priority" onChange={jest.fn()} />);

    // Check that all options are available
    const select = screen.getByRole("combobox");
    fireEvent.focus(select); // Focus to expand options

    expect(screen.getByText("Priority (highest first)")).toBeInTheDocument();
    expect(screen.getByText("Title (A to Z)")).toBeInTheDocument();
    expect(screen.getByText("Creation date (newest first)")).toBeInTheDocument();
  });
});
