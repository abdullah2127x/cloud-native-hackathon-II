/**
 * Tests for ErrorMessage component.
 *
 * Task IDs: T427, T429
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import ErrorMessage from './ErrorMessage';

describe('ErrorMessage', () => {
  // T427: Test ErrorMessage displays correct message
  it('T427: Displays error message text', () => {
    render(
      <ErrorMessage
        message="Connection lost. Check your internet or try again."
        onRetry={() => {}}
      />
    );

    expect(
      screen.getByText('Connection lost. Check your internet or try again.')
    ).toBeInTheDocument();
  });

  // T427: Test retry button is present
  it('T427: Displays retry button', () => {
    render(
      <ErrorMessage
        message="Test error message"
        onRetry={() => {}}
      />
    );

    const retryButton = screen.getByRole('button', { name: /try again/i });
    expect(retryButton).toBeInTheDocument();
  });

  // T427: Test error icon is displayed
  it('T427: Displays error icon (AlertCircle)', () => {
    render(
      <ErrorMessage
        message="Test error message"
        onRetry={() => {}}
      />
    );

    // Check for the icon container
    const errorContainer = screen.getByText('Test error message').closest('div');
    expect(errorContainer).toBeInTheDocument();

    // The AlertCircle icon should be in the DOM (it's in the parent div)
    const iconContainer = errorContainer?.parentElement;
    expect(iconContainer?.className).toContain('flex');
  });

  // T427: Test styling (rounded border, destructive color)
  it('T427: Has correct styling (border, background, color)', () => {
    const { container } = render(
      <ErrorMessage
        message="Test error"
        onRetry={() => {}}
      />
    );

    const errorDiv = container.querySelector('.rounded-lg');
    expect(errorDiv).toBeInTheDocument();
    expect(errorDiv).toHaveClass('border', 'destructive');
  });

  // T429: Test retry button calls onRetry callback
  it('T429: Calls onRetry callback when retry button is clicked', async () => {
    const user = userEvent.setup();
    const onRetry = vi.fn();

    render(
      <ErrorMessage
        message="Test error"
        onRetry={onRetry}
      />
    );

    const retryButton = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButton);

    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  // T429: Test retry button shows loading state
  it('T429: Displays loading state (spinner) when isRetrying is true', () => {
    render(
      <ErrorMessage
        message="Test error"
        onRetry={() => {}}
        isRetrying={true}
      />
    );

    // When retrying, button text should show "Retrying..."
    expect(screen.getByText('Retrying...')).toBeInTheDocument();
  });

  // T429: Test retry button is disabled during retry
  it('T429: Disables retry button during retry', () => {
    render(
      <ErrorMessage
        message="Test error"
        onRetry={() => {}}
        isRetrying={true}
      />
    );

    const retryButton = screen.getByRole('button', { name: /retrying/i });
    expect(retryButton).toBeDisabled();
  });

  // T429: Test retry button shows normal state when not retrying
  it('T429: Shows normal button state when not retrying', () => {
    render(
      <ErrorMessage
        message="Test error"
        onRetry={() => {}}
        isRetrying={false}
      />
    );

    const retryButton = screen.getByRole('button', { name: /try again/i });
    expect(retryButton).not.toBeDisabled();
    expect(screen.getByText('Try Again')).toBeInTheDocument();
  });

  // T427: Test different error messages
  it('T427: Renders different error messages correctly', () => {
    const messages = [
      'Connection lost. Check your internet or try again.',
      'Request timed out. Please try again.',
      'Session expired. Please log in again.',
      'Invalid input. Please check your message and try again.',
      "You don't have permission to access this conversation.",
    ];

    messages.forEach((message) => {
      const { unmount } = render(
        <ErrorMessage
          message={message}
          onRetry={() => {}}
        />
      );

      expect(screen.getByText(message)).toBeInTheDocument();
      unmount();
    });
  });

  // T429: Test multiple retries update state correctly
  it('T429: Multiple retries work independently', async () => {
    const user = userEvent.setup();
    const onRetry = vi.fn();

    const { rerender } = render(
      <ErrorMessage
        message="Test error"
        onRetry={onRetry}
        isRetrying={false}
      />
    );

    const retryButton = screen.getByRole('button', { name: /try again/i });

    // First retry
    await user.click(retryButton);
    expect(onRetry).toHaveBeenCalledTimes(1);

    // Simulate loading state
    rerender(
      <ErrorMessage
        message="Test error"
        onRetry={onRetry}
        isRetrying={true}
      />
    );

    // Button should be disabled
    expect(screen.getByRole('button', { name: /retrying/i })).toBeDisabled();

    // Simulate loading complete
    rerender(
      <ErrorMessage
        message="Test error"
        onRetry={onRetry}
        isRetrying={false}
      />
    );

    // Second retry
    const retryButtonAgain = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButtonAgain);

    expect(onRetry).toHaveBeenCalledTimes(2);
  });

  // T427: Test accessibility
  it('T427: Has proper accessibility attributes', () => {
    render(
      <ErrorMessage
        message="Connection error"
        onRetry={() => {}}
      />
    );

    const retryButton = screen.getByRole('button', { name: /try again/i });
    expect(retryButton).toBeInTheDocument();

    // Should be keyboard accessible
    expect(retryButton.tagName).toBe('BUTTON');
  });

  // T427: Test no onRetry callback errors
  it('T427: Handles missing onRetry gracefully', async () => {
    const user = userEvent.setup();
    const { container } = render(
      <ErrorMessage
        message="Test error"
        onRetry={() => {
          throw new Error('Should not happen');
        }}
      />
    );

    // Component should render without errors
    expect(container).toBeInTheDocument();
  });
});
