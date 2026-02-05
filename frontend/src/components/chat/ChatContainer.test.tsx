/**
 * Tests for ChatContainer component error handling.
 *
 * Task IDs: T427, T428, T429, T430
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import ChatContainer from './ChatContainer';

// Mock the dependencies
vi.mock('@/lib/auth-client', () => ({
  useSession: vi.fn(() => ({
    data: {
      user: { id: 'user-123', email: 'test@example.com' },
      token: 'mock-token',
    },
  })),
}));

vi.mock('@/lib/api/chat', () => ({
  getConversation: vi.fn(),
}));

vi.mock('./MessageList', () => ({
  default: ({ messages }: any) => (
    <div data-testid="message-list">
      {messages.map((msg: any) => (
        <div key={msg.id} data-testid="message">
          {msg.content}
        </div>
      ))}
    </div>
  ),
}));

vi.mock('./ChatInput', () => ({
  default: ({ onSend, isLoading }: any) => (
    <div data-testid="chat-input">
      <button
        data-testid="send-button"
        disabled={isLoading}
        onClick={() => onSend('Test message')}
      >
        Send
      </button>
    </div>
  ),
}));

vi.mock('./ConversationSidebar', () => ({
  default: () => <div data-testid="sidebar">Sidebar</div>,
}));

// T427: Test ErrorMessage component displays correct message and retry button
describe('ChatContainer - Error Handling', () => {
  let mockFetch: any;

  beforeEach(() => {
    mockFetch = vi.fn();
    global.fetch = mockFetch;
    localStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
    localStorage.clear();
  });

  it('T427: Displays error message with retry button on send failure', async () => {
    const user = userEvent.setup({ delay: null });

    mockFetch.mockRejectedValueOnce(
      new Error('Failed to send message')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    // Wait for error to be displayed
    await waitFor(() => {
      const errorMessage = screen.getByText(/connection lost/i);
      expect(errorMessage).toBeInTheDocument();
    });

    // T427: Verify retry button is present
    const retryButton = screen.getByRole('button', { name: /try again/i });
    expect(retryButton).toBeInTheDocument();
  });

  // T428: Test error classification logic
  it('T428: Classifies network errors correctly', async () => {
    const user = userEvent.setup({ delay: null });

    // Simulate network error
    mockFetch.mockRejectedValueOnce(
      new TypeError('Failed to fetch')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });
  });

  it('T428: Classifies timeout errors correctly', async () => {
    const user = userEvent.setup({ delay: null });

    // Simulate timeout error (DOMException with AbortError)
    mockFetch.mockRejectedValueOnce(
      new DOMException('The operation was aborted', 'AbortError')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/request timed out/i)).toBeInTheDocument();
    });
  });

  it('T428: Classifies auth errors correctly', async () => {
    const user = userEvent.setup({ delay: null });

    // Simulate auth error
    mockFetch.mockRejectedValueOnce(
      new Error('401 unauthorized')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/session expired/i)).toBeInTheDocument();
    });
  });

  it('T428: Classifies server errors correctly', async () => {
    const user = userEvent.setup({ delay: null });

    // Simulate server error
    mockFetch.mockRejectedValueOnce(
      new Error('500 server error')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
    });
  });

  // T428: Test that non-retryable errors don't show retry button
  it('T428: Non-retryable errors disable retry button', async () => {
    const user = userEvent.setup({ delay: null });

    // Simulate auth error (not retryable)
    mockFetch.mockRejectedValueOnce(
      new Error('401 unauthorized')
    );

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      const retryButton = screen.getByRole('button', { name: /try again/i });
      expect(retryButton).toBeDisabled();
    });
  });

  // T429: Test retry button re-submission with exponential backoff
  it('T429: Retry button re-submits message after exponential backoff', async () => {
    const user = userEvent.setup({ delay: null });

    // First call fails, second call succeeds
    mockFetch
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 'conv-123',
          message: 'Response message',
          role: 'assistant',
          created_at: new Date().toISOString(),
        }),
      });

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    // Wait for error to appear
    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // T429: Click retry button
    const retryButton = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButton);

    // T429: Verify exponential backoff delay (first retry is 1 second = 1000ms)
    expect(vi.getTimerCount()).toBeGreaterThan(0);

    // Advance timers by 1 second
    vi.advanceTimersByTime(1000);

    // Wait for successful response
    await waitFor(() => {
      expect(screen.queryByText(/connection lost/i)).not.toBeInTheDocument();
    });

    // Verify message was sent successfully
    expect(mockFetch).toHaveBeenCalledTimes(2);
  });

  // T429: Test exponential backoff increases with each retry
  it('T429: Exponential backoff increases with each retry attempt', async () => {
    const user = userEvent.setup({ delay: null });

    // All calls fail to test multiple retries
    mockFetch
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 'conv-123',
          message: 'Response message',
          role: 'assistant',
          created_at: new Date().toISOString(),
        }),
      });

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // First retry (1 second delay)
    let retryButton = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButton);
    vi.advanceTimersByTime(1000);

    // Wait for error again
    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // Second retry (2 second delay)
    retryButton = screen.getByRole('button', { name: /try again/i });
    await user.click(retryButton);
    vi.advanceTimersByTime(2000);

    // Wait for success
    await waitFor(() => {
      expect(screen.queryByText(/connection lost/i)).not.toBeInTheDocument();
    });

    expect(mockFetch).toHaveBeenCalledTimes(3);
  });

  // T430: Integration test - API failure, error display, successful retry
  it('T430: Full flow - API failure, error display, and successful retry', async () => {
    const user = userEvent.setup({ delay: null });

    // First request fails, second succeeds
    mockFetch
      .mockRejectedValueOnce(new TypeError('Failed to fetch'))
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          conversation_id: 'conv-456',
          message: 'Hello, how can I help?',
          role: 'assistant',
          created_at: new Date().toISOString(),
        }),
      });

    render(<ChatContainer userId="user-123" />);

    // Verify initial state
    expect(screen.getByTestId('message-list')).toBeInTheDocument();

    // T430: Send message (will fail)
    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    // T430: Verify error is displayed
    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // T430: Verify input field remains enabled (send button not disabled by error)
    const stateAfterError = screen.getByTestId('send-button');
    expect(stateAfterError).not.toBeDisabled();

    // T430: Click retry
    const retryButton = screen.getByRole('button', { name: /try again/i });
    expect(retryButton).toBeInTheDocument();
    await user.click(retryButton);

    // T430: Advance past exponential backoff delay
    vi.advanceTimersByTime(1000);

    // T430: Verify error is cleared and message is sent successfully
    await waitFor(() => {
      expect(screen.queryByText(/connection lost/i)).not.toBeInTheDocument();
      expect(mockFetch).toHaveBeenCalledTimes(2);
    });

    // T430: Verify conversation ID is stored
    expect(localStorage.getItem('chat_conversation_user-123')).toBe('conv-456');
  });

  it('T430: Input field remains enabled during error state', async () => {
    const user = userEvent.setup({ delay: null });

    mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // T430: Verify send button is enabled (FR-017)
    const buttonAfterError = screen.getByTestId('send-button');
    expect(buttonAfterError).not.toBeDisabled();
  });

  it('T430: Input field is disabled only during loading', async () => {
    const user = userEvent.setup({ delay: null });

    let resolveRequest: any;
    const requestPromise = new Promise((resolve) => {
      resolveRequest = resolve;
    });

    mockFetch.mockReturnValueOnce(requestPromise);

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');

    // Start sending - button should be disabled during loading
    const clickPromise = user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByTestId('send-button')).toBeDisabled();
    });

    // Complete the request
    resolveRequest({
      ok: true,
      json: async () => ({
        conversation_id: 'conv-123',
        message: 'Response',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    });

    await clickPromise;

    // After loading completes, button should be enabled again
    await waitFor(() => {
      expect(screen.getByTestId('send-button')).not.toBeDisabled();
    });
  });

  // Optimistic updates test
  it('FR-017: User message appears immediately (optimistic update)', async () => {
    const user = userEvent.setup({ delay: null });

    let resolveRequest: any;
    const requestPromise = new Promise((resolve) => {
      resolveRequest = resolve;
    });

    mockFetch.mockReturnValueOnce(requestPromise);

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');

    // Send message
    await user.click(sendButton);

    // User message should appear IMMEDIATELY (before server responds)
    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
    });

    // Server responds
    resolveRequest({
      ok: true,
      json: async () => ({
        conversation_id: 'conv-123',
        message: 'Server response',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    });

    // Both messages should now be visible
    await waitFor(() => {
      expect(screen.getByText('Test message')).toBeInTheDocument();
      expect(screen.getByText('Server response')).toBeInTheDocument();
    });
  });

  // Optimistic update rollback on error
  it('FR-017: Optimistic message is removed on error', async () => {
    const user = userEvent.setup({ delay: null });

    mockFetch.mockRejectedValueOnce(new TypeError('Failed to fetch'));

    render(<ChatContainer userId="user-123" />);

    const sendButton = screen.getByTestId('send-button');

    // Send message
    await user.click(sendButton);

    // Message appears optimistically
    expect(screen.getByText('Test message')).toBeInTheDocument();

    // Error occurs
    await waitFor(() => {
      expect(screen.getByText(/connection lost/i)).toBeInTheDocument();
    });

    // Optimistic message is removed because the request failed
    expect(screen.queryByText('Test message')).not.toBeInTheDocument();
  });
});
