/**
 * Conversation persistence integration test.
 *
 * Task ID: T230
 * Spec: specs/001-chat-interface/spec.md
 * Tests: Create conversation, refresh page, verify history restored
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatContainer from '@/components/chat/ChatContainer';
import { useSession } from '@/lib/auth-client';
import * as chatApi from '@/lib/api/chat';

jest.mock('@/lib/auth-client');
jest.mock('@openai/chatkit', () => ({
  useChatKit: jest.fn(() => ({ control: {} })),
}));
jest.mock('@/lib/api/chat');

const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;
const mockGetConversation = chatApi.getConversation as jest.MockedFunction<
  typeof chatApi.getConversation
>;

describe('Conversation Persistence Integration', () => {
  let localStorageMock: { [key: string]: string };

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock localStorage
    localStorageMock = {};
    global.localStorage = {
      getItem: jest.fn((key: string) => localStorageMock[key] || null),
      setItem: jest.fn((key: string, value: string) => {
        localStorageMock[key] = value;
      }),
      removeItem: jest.fn((key: string) => {
        delete localStorageMock[key];
      }),
      clear: jest.fn(() => {
        localStorageMock = {};
      }),
      key: jest.fn(),
      length: 0,
    };

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

  it('persists conversation_id to localStorage on creation', async () => {
    const user = userEvent.setup();

    render(<ChatContainer userId="user-123" />);

    // User types and sends message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Hello, AI!');

    const sendButton = screen.getByRole('button', { name: /send/i });
    await user.click(sendButton);

    // Wait for conversation_id to be stored
    await waitFor(() => {
      expect(localStorage.setItem).toHaveBeenCalledWith(
        'chat_conversation_user-123',
        'conv-123'
      );
    });
  });

  it('restores conversation history from localStorage on mount', async () => {
    // Simulate existing conversation in localStorage
    localStorageMock['chat_conversation_user-123'] = 'conv-existing';

    const mockConversation = {
      id: 'conv-existing',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user' as const,
          content: 'Previous message',
          created_at: '2024-01-01T00:00:00Z',
        },
        {
          id: 'msg-2',
          role: 'assistant' as const,
          content: 'Previous response',
          created_at: '2024-01-01T00:00:01Z',
        },
      ],
    };

    mockGetConversation.mockResolvedValue(mockConversation);

    render(<ChatContainer userId="user-123" />);

    // Should load conversation from localStorage
    expect(localStorage.getItem).toHaveBeenCalledWith('chat_conversation_user-123');

    // Should fetch conversation history
    await waitFor(() => {
      expect(mockGetConversation).toHaveBeenCalledWith(
        'user-123',
        'conv-existing',
        'mock-token'
      );
    });

    // Should display loaded messages
    await waitFor(() => {
      expect(screen.getByText('Previous message')).toBeInTheDocument();
      expect(screen.getByText('Previous response')).toBeInTheDocument();
    });
  });

  it('clears invalid conversation_id on fetch error', async () => {
    localStorageMock['chat_conversation_user-123'] = 'invalid-conv';

    mockGetConversation.mockRejectedValue(new Error('Conversation not found'));

    render(<ChatContainer userId="user-123" />);

    // Should attempt to load conversation
    await waitFor(() => {
      expect(mockGetConversation).toHaveBeenCalledWith(
        'user-123',
        'invalid-conv',
        'mock-token'
      );
    });

    // Should clear localStorage on error
    await waitFor(() => {
      expect(localStorage.removeItem).toHaveBeenCalledWith('chat_conversation_user-123');
    });

    // Should show error message
    expect(screen.getByText(/failed to load conversation history/i)).toBeInTheDocument();
  });

  it('continues existing conversation after refresh', async () => {
    const user = userEvent.setup();

    // Simulate existing conversation
    localStorageMock['chat_conversation_user-123'] = 'conv-existing';

    const mockConversation = {
      id: 'conv-existing',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user' as const,
          content: 'Old message',
          created_at: '2024-01-01T00:00:00Z',
        },
      ],
    };

    mockGetConversation.mockResolvedValue(mockConversation);

    render(<ChatContainer userId="user-123" />);

    // Wait for history to load
    await waitFor(() => {
      expect(screen.getByText('Old message')).toBeInTheDocument();
    });

    // Send new message
    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'New message');
    await user.click(screen.getByRole('button', { name: /send/i }));

    // Should send with existing conversation_id
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/user-123/chat',
        expect.objectContaining({
          body: expect.stringContaining('conv-existing'),
        })
      );
    });
  });
});
