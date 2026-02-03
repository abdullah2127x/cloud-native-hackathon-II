/**
 * Component tests for TagInput
 * Spec: 002-todo-organization-features
 * Task: T053, T053b
 */

import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { TagInput } from "./TagInput";

describe("TagInput", () => {
  it("renders with placeholder", () => {
    render(<TagInput value={[]} onChange={jest.fn()} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    expect(input).toBeInTheDocument();
  });

  it("displays existing tags", () => {
    render(
      <TagInput
        value={["work", "important"]}
        onChange={jest.fn()}
        suggestions={[]}
      />
    );

    expect(screen.getByText("work")).toBeInTheDocument();
    expect(screen.getByText("important")).toBeInTheDocument();
  });

  it("adds a tag when pressing Enter", () => {
    const mockOnChange = jest.fn();
    render(<TagInput value={[]} onChange={mockOnChange} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "new-tag" } });
    fireEvent.keyDown(input, { key: "Enter" });

    expect(mockOnChange).toHaveBeenCalledWith(["new-tag"]);
  });

  it("adds a tag when pressing comma", () => {
    const mockOnChange = jest.fn();
    render(<TagInput value={[]} onChange={mockOnChange} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "new-tag" } });
    fireEvent.keyDown(input, { key: "," });

    expect(mockOnChange).toHaveBeenCalledWith(["new-tag"]);
  });

  it("removes a tag when clicking the remove button", () => {
    const mockOnChange = jest.fn();
    render(
      <TagInput
        value={["work", "important"]}
        onChange={mockOnChange}
        suggestions={[]}
      />
    );

    const removeButtons = screen.getAllByLabelText(/Remove tag/);
    fireEvent.click(removeButtons[0]); // Remove "work"

    expect(mockOnChange).toHaveBeenCalledWith(["important"]);
  });

  it("shows error when tag contains spaces", () => {
    const mockOnChange = jest.fn();
    render(<TagInput value={[]} onChange={mockOnChange} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "tag with spaces" } });
    fireEvent.keyDown(input, { key: "Enter" });

    expect(screen.getByText("Tags must be single words (no spaces)")).toBeInTheDocument();
  });

  it("shows error when tag is too long", () => {
    const mockOnChange = jest.fn();
    render(<TagInput value={[]} onChange={mockOnChange} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    const longTag = "a".repeat(51); // 51 characters, exceeding 50
    fireEvent.change(input, { target: { value: longTag } });
    fireEvent.keyDown(input, { key: "Enter" });

    expect(screen.getByText("Tag must be 50 characters or less")).toBeInTheDocument();
  });

  it("shows suggestions when typing", () => {
    render(
      <TagInput
        value={[]}
        onChange={jest.fn()}
        suggestions={["work", "personal", "urgent"]}
      />
    );

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "wor" } });

    expect(screen.getByText("work")).toBeInTheDocument();
  });

  it("adds suggested tag when clicked", () => {
    const mockOnChange = jest.fn();
    render(
      <TagInput
        value={[]}
        onChange={mockOnChange}
        suggestions={["work", "personal", "urgent"]}
      />
    );

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "wor" } });

    const suggestion = screen.getByText("work");
    fireEvent.click(suggestion);

    expect(mockOnChange).toHaveBeenCalledWith(["work"]);
  });

  it("doesn't add duplicate tags", () => {
    const mockOnChange = jest.fn();
    render(
      <TagInput
        value={["work"]}
        onChange={mockOnChange}
        suggestions={["work", "personal"]}
      />
    );

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "work" } });
    fireEvent.keyDown(input, { key: "Enter" });

    // onChange should not be called since tag already exists
    expect(mockOnChange).not.toHaveBeenCalled();
  });

  it("removes last tag when backspace pressed on empty input", () => {
    const mockOnChange = jest.fn();
    render(
      <TagInput
        value={["work", "important"]}
        onChange={mockOnChange}
        suggestions={[]}
      />
    );

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.keyDown(input, { key: "Backspace" });

    expect(mockOnChange).toHaveBeenCalledWith(["work"]);
  });

  it("disables input when disabled prop is true", () => {
    render(
      <TagInput
        value={[]}
        onChange={jest.fn()}
        suggestions={[]}
        disabled={true}
      />
    );

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    expect(input).toBeDisabled();
  });

  it("shows 'Tags must be single words' error when space entered (T053b)", () => {
    const mockOnChange = jest.fn();
    render(<TagInput value={[]} onChange={mockOnChange} suggestions={[]} />);

    const input = screen.getByPlaceholderText("Add tags (comma or enter to add)...");
    fireEvent.change(input, { target: { value: "test tag" } }); // Contains space
    fireEvent.keyDown(input, { key: "Enter" });

    expect(screen.getByText("Tags must be single words (no spaces)")).toBeInTheDocument();
  });
});
