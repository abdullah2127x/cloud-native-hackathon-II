/**
 * Component tests for SearchBar
 * Spec: 002-todo-organization-features
 * Task: T064
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { SearchBar } from "./SearchBar";

describe("SearchBar", () => {
  it("renders with placeholder", () => {
    render(<SearchBar value="" onChange={jest.fn()} />);

    const input = screen.getByPlaceholderText("Search tasks...");
    expect(input).toBeInTheDocument();
  });

  it("shows search icon", () => {
    render(<SearchBar value="" onChange={jest.fn()} />);

    const searchIcon = screen.getByLabelText("");
    expect(searchIcon.closest('svg')).toBeInTheDocument();
  });

  it("updates value when input changes", () => {
    const mockOnChange = jest.fn();
    render(<SearchBar value="" onChange={mockOnChange} />);

    const input = screen.getByPlaceholderText("Search tasks...");
    fireEvent.change(input, { target: { value: "test search" } });

    expect(mockOnChange).toHaveBeenCalledWith("test search");
  });

  it("shows clear button when there is a value", () => {
    render(<SearchBar value="test" onChange={jest.fn()} />);

    const clearButton = screen.getByLabelText("Clear search");
    expect(clearButton).toBeInTheDocument();
  });

  it("hides clear button when value is empty", () => {
    render(<SearchBar value="" onChange={jest.fn()} />);

    const clearButton = screen.queryByLabelText("Clear search");
    expect(clearButton).not.toBeInTheDocument();
  });

  it("clears value when clear button is clicked", () => {
    const mockOnChange = jest.fn();
    render(<SearchBar value="test" onChange={mockOnChange} />);

    const clearButton = screen.getByLabelText("Clear search");
    fireEvent.click(clearButton);

    expect(mockOnChange).toHaveBeenCalledWith("");
  });

  it("displays current value", () => {
    render(<SearchBar value="current search" onChange={jest.fn()} />);

    const input = screen.getByDisplayValue("current search");
    expect(input).toBeInTheDocument();
  });
});
