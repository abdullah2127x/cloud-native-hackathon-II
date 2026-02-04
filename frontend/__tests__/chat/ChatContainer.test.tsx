/**
 * ChatContainer component tests.
 *
 * Task ID: T130
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatContainer from '@/components/chat/ChatContainer';
import { useSession } from '@/lib/auth-client';

// Mock dependencies
jest.mock('@/lib/auth-client');
jest.mock('@openai/chatkit', () => ({
  useChatKit: jest.fn(() => ({ control: {} })),
}));

const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;

describe('ChatContainer', () => {
  beforeEach(() => {
    mockUseSession.mockReturnValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        token: 'mock-token',
      },
      isPending: false,
    } as any);

    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('initializes useChatKit with correct config', () => {
    const { useChatKit } = require('@openai/chatkit');

    render(<ChatContainer userId="user-123" />);

    expect(useChatKit).toHaveBeenCalledWith(
      expect.objectContaining({
        api: expect.objectContaining({
          url: '/api/user-123/chat',
          domainKey: expect.any(String),
          fetch: expect.any(Function),
        }),
        onError: expect.any(Function),
      })
    );
  });

  it('displays error message when API call fails', async () => {
    const user = userEvent.setup();
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    render(<ChatContainer userId="user-123" />);

    const input = screen.getByPlaceholderText(/type your message/i);
    const sendButton = screen.getByRole('button', { name: /send/i });

    await user.type(input, 'Hello');
    await user.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });
  });
});
