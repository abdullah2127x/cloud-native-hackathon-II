/**
 * Component tests for TagChip
 * Spec: 002-todo-organization-features
 * Task: T052
 */

import { render, screen, fireEvent } from "@testing-library/react";
import { TagChip } from "./TagChip";

describe("TagChip", () => {
  it("displays tag name", () => {
    render(<TagChip name="work" />);
    expect(screen.getByText("work")).toBeInTheDocument();
  });

  it("shows remove button when onRemove is provided", () => {
    const mockOnRemove = jest.fn();
    render(<TagChip name="work" onRemove={mockOnRemove} />);

    const removeButton = screen.getByLabelText("Remove tag work");
    expect(removeButton).toBeInTheDocument();

    fireEvent.click(removeButton);
    expect(mockOnRemove).toHaveBeenCalled();
  });

  it("does not show remove button when onRemove is not provided", () => {
    render(<TagChip name="work" />);

    const removeButton = screen.queryByLabelText("Remove tag work");
    expect(removeButton).not.toBeInTheDocument();
  });

  it("calls onClick when clicked", () => {
    const mockOnClick = jest.fn();
    render(<TagChip name="work" onClick={mockOnClick} />);

    fireEvent.click(screen.getByText("work"));
    expect(mockOnClick).toHaveBeenCalled();
  });

  it("stops event propagation when remove button is clicked", () => {
    const mockParentClick = jest.fn();
    const mockOnRemove = jest.fn();

    render(
      <div onClick={mockParentClick}>
        <TagChip name="work" onRemove={mockOnRemove} />
      </div>
    );

    const removeButton = screen.getByLabelText("Remove tag work");
    fireEvent.click(removeButton);

    expect(mockOnRemove).toHaveBeenCalled();
    expect(mockParentClick).not.toHaveBeenCalled();
  });
});
