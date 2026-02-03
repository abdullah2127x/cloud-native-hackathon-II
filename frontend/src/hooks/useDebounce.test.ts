/**
 * Hook tests for useDebounce
 * Spec: 002-todo-organization-features
 * Task: T065
 */

import { renderHook, act } from "@testing-library/react";
import { useDebounce } from "./useDebounce";

describe("useDebounce", () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it("should initially return the initial value", () => {
    const { result } = renderHook(() => useDebounce("initial", 300));

    expect(result.current).toBe("initial");
  });

  it("should return the same value after delay if no changes", () => {
    const { result } = renderHook(() => useDebounce("initial", 300));

    act(() => {
      jest.advanceTimersByTime(300);
    });

    expect(result.current).toBe("initial");
  });

  it("should debounce value changes", () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: "initial", delay: 300 }
      }
    );

    // Change the value
    rerender({ value: "updated", delay: 300 });
    expect(result.current).toBe("initial"); // Should still be the initial value

    // Advance time but not enough for debounce
    act(() => {
      jest.advanceTimersByTime(200);
    });
    expect(result.current).toBe("initial"); // Should still be the initial value

    // Advance time enough for debounce
    act(() => {
      jest.advanceTimersByTime(100);
    });
    expect(result.current).toBe("updated"); // Should now be updated
  });

  it("should respect the delay time", () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: "initial", delay: 500 }
      }
    );

    rerender({ value: "updated", delay: 500 });

    // Advance time less than delay
    act(() => {
      jest.advanceTimersByTime(400);
    });
    expect(result.current).toBe("initial"); // Should still be initial

    // Advance time to meet delay
    act(() => {
      jest.advanceTimersByTime(100);
    });
    expect(result.current).toBe("updated"); // Should now be updated
  });

  it("should cancel previous timers when value changes quickly", () => {
    const { result, rerender } = renderHook(
      ({ value, delay }) => useDebounce(value, delay),
      {
        initialProps: { value: "initial", delay: 300 }
      }
    );

    // Change value
    rerender({ value: "updated", delay: 300 });
    expect(result.current).toBe("initial");

    // Change value again before delay
    act(() => {
      jest.advanceTimersByTime(150);
    });
    rerender({ value: "final", delay: 300 });

    // Advance time to complete delay
    act(() => {
      jest.advanceTimersByTime(300);
    });

    // Should show the final value, not the intermediate one
    expect(result.current).toBe("final");
  });
});
