/**
 * Chat flow integration test.
 *
 * Task ID: T133
 * Spec: specs/001-chat-interface/spec.md
 * Tests: User sends message → saved to DB → AI responds → response saved → UI updates
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatContainer from '@/components/chat/ChatContainer';
import { useSession } from '@/lib/auth-client';

jest.mock('@/lib/auth-client');
jest.mock('@openai/chatkit', () => ({
  useChatKit: jest.fn(() => ({ control: {} })),
}));

const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;

describe('Chat Flow Integration', () => {
  beforeEach(() => {
    mockUseSession.mockReturnValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        token: 'mock-token',
      },
      isPending: false,
    } as any);

    // Mock successful API response
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        conversation_id: 'conv-123',
        message: 'I received: Hello, AI!',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('completes full message flow: send → save → AI respond → update UI', async () => {
    const user = userEvent.setup();

    render(<ChatContainer userId="user-123" />);

    // User types message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Hello, AI!');

    // User submits message
    const sendButton = screen.getByRole('button', { name: /send/i });
    await user.click(sendButton);

    // Verify API call was made with correct data
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/user-123/chat',
        expect.objectContaining({
          method: 'POST',
          headers: expect.objectContaining({
            'Authorization': 'Bearer mock-token',
            'Content-Type': 'application/json',
          }),
          body: JSON.stringify({
            conversation_id: null,
            message: 'Hello, AI!',
          }),
        })
      );
    });

    // Verify UI updates with messages
    await waitFor(() => {
      expect(screen.getByText('Hello, AI!')).toBeInTheDocument();
      expect(screen.getByText('I received: Hello, AI!')).toBeInTheDocument();
    });

    // Verify input was cleared
    expect(input).toHaveValue('');
  });

  it('continues existing conversation with conversation_id', async () => {
    const user = userEvent.setup();

    // Mock response with existing conversation_id
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        conversation_id: 'existing-conv',
        message: 'Response 1',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    }).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        conversation_id: 'existing-conv',
        message: 'Response 2',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    });

    render(<ChatContainer userId="user-123" />);

    const input = screen.getByPlaceholderText(/type your message/i);

    // First message
    await user.type(input, 'First message');
    await user.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      expect(screen.getByText('Response 1')).toBeInTheDocument();
    });

    // Second message should include conversation_id
    await user.type(input, 'Second message');
    await user.click(screen.getByRole('button', { name: /send/i }));

    await waitFor(() => {
      const calls = (global.fetch as jest.Mock).mock.calls;
      expect(calls[1][1].body).toContain('existing-conv');
    });
  });
});
