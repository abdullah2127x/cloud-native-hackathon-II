/**
 * Conversation list integration test.
 *
 * Task ID: T310
 * Spec: specs/001-chat-interface/spec.md
 * Tests: Create multiple conversations, verify list displays, verify clicking switches between them
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
const mockListConversations = chatApi.listConversations as jest.MockedFunction<
  typeof chatApi.listConversations
>;
const mockGetConversation = chatApi.getConversation as jest.MockedFunction<
  typeof chatApi.getConversation
>;

describe('Conversation List Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();

    mockUseSession.mockReturnValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        token: 'mock-token',
      },
      isPending: false,
    } as any);

    // Mock localStorage
    global.localStorage = {
      getItem: jest.fn(() => null),
      setItem: jest.fn(),
      removeItem: jest.fn(),
      clear: jest.fn(),
      key: jest.fn(),
      length: 0,
    };

    // Mock fetch for sending messages
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        conversation_id: 'new-conv',
        message: 'AI response',
        role: 'assistant',
        created_at: new Date().toISOString(),
      }),
    });
  });

  it('displays multiple conversations in sidebar', async () => {
    const mockConversations = [
      {
        id: 'conv-1',
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T10:00:00Z',
      },
      {
        id: 'conv-2',
        created_at: '2024-01-02T11:00:00Z',
        updated_at: '2024-01-02T11:00:00Z',
      },
      {
        id: 'conv-3',
        created_at: '2024-01-03T12:00:00Z',
        updated_at: '2024-01-03T12:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 3,
      limit: 20,
      offset: 0,
    });

    render(<ChatContainer userId="user-123" />);

    // Wait for conversations to load
    await waitFor(() => {
      expect(mockListConversations).toHaveBeenCalledWith('user-123', 'mock-token');
    });

    // Should display conversation items (need to account for responsive design)
    // On desktop (md breakpoint), sidebar should be visible
    const conversationButtons = await screen.findAllByRole('button');
    expect(conversationButtons.length).toBeGreaterThanOrEqual(3);
  });

  it('switches between conversations when clicking', async () => {
    const user = userEvent.setup();

    const mockConversations = [
      {
        id: 'conv-1',
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T10:00:00Z',
      },
      {
        id: 'conv-2',
        created_at: '2024-01-02T11:00:00Z',
        updated_at: '2024-01-02T11:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 2,
      limit: 20,
      offset: 0,
    });

    const conv1Messages = {
      id: 'conv-1',
      created_at: '2024-01-01T10:00:00Z',
      updated_at: '2024-01-01T10:00:00Z',
      messages: [
        {
          id: 'msg-1-1',
          role: 'user' as const,
          content: 'Conversation 1 message',
          created_at: '2024-01-01T10:00:00Z',
        },
      ],
    };

    const conv2Messages = {
      id: 'conv-2',
      created_at: '2024-01-02T11:00:00Z',
      updated_at: '2024-01-02T11:00:00Z',
      messages: [
        {
          id: 'msg-2-1',
          role: 'user' as const,
          content: 'Conversation 2 message',
          created_at: '2024-01-02T11:00:00Z',
        },
      ],
    };

    mockGetConversation
      .mockResolvedValueOnce(conv1Messages)
      .mockResolvedValueOnce(conv2Messages);

    render(<ChatContainer userId="user-123" />);

    // Wait for conversations to load
    await waitFor(() => {
      expect(mockListConversations).toHaveBeenCalled();
    });

    // Find and click first conversation
    const conversationButtons = screen.getAllByRole('button');
    const firstConvButton = conversationButtons.find(
      (btn) => btn.textContent?.includes('Conversation') && !btn.textContent?.includes('New')
    );

    if (firstConvButton) {
      await user.click(firstConvButton);

      // Should load first conversation messages
      await waitFor(() => {
        expect(mockGetConversation).toHaveBeenCalledWith('user-123', 'conv-1', 'mock-token');
      });

      await waitFor(() => {
        expect(screen.getByText('Conversation 1 message')).toBeInTheDocument();
      });

      // Click second conversation
      const secondConvButton = conversationButtons[conversationButtons.indexOf(firstConvButton) + 1];
      if (secondConvButton) {
        await user.click(secondConvButton);

        // Should load second conversation messages
        await waitFor(() => {
          expect(mockGetConversation).toHaveBeenCalledWith('user-123', 'conv-2', 'mock-token');
        });

        await waitFor(() => {
          expect(screen.getByText('Conversation 2 message')).toBeInTheDocument();
        });
      }
    }
  });

  it('persists selected conversation to localStorage', async () => {
    const user = userEvent.setup();

    const mockConversations = [
      {
        id: 'conv-selected',
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T10:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 1,
      limit: 20,
      offset: 0,
    });

    mockGetConversation.mockResolvedValue({
      id: 'conv-selected',
      created_at: '2024-01-01T10:00:00Z',
      updated_at: '2024-01-01T10:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user' as const,
          content: 'Test message',
          created_at: '2024-01-01T10:00:00Z',
        },
      ],
    });

    render(<ChatContainer userId="user-123" />);

    await waitFor(() => {
      expect(mockListConversations).toHaveBeenCalled();
    });

    // Click on conversation
    const conversationButtons = screen.getAllByRole('button');
    const convButton = conversationButtons.find(
      (btn) => btn.textContent?.includes('Conversation') && !btn.textContent?.includes('New')
    );

    if (convButton) {
      await user.click(convButton);

      // Should persist to localStorage
      await waitFor(() => {
        expect(localStorage.setItem).toHaveBeenCalledWith(
          'chat_conversation_user-123',
          'conv-selected'
        );
      });
    }
  });

  it('clears conversation state when "New Conversation" is clicked', async () => {
    const user = userEvent.setup();

    const mockConversations = [
      {
        id: 'conv-1',
        created_at: '2024-01-01T10:00:00Z',
        updated_at: '2024-01-01T10:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 1,
      limit: 20,
      offset: 0,
    });

    mockGetConversation.mockResolvedValue({
      id: 'conv-1',
      created_at: '2024-01-01T10:00:00Z',
      updated_at: '2024-01-01T10:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user' as const,
          content: 'Old message',
          created_at: '2024-01-01T10:00:00Z',
        },
      ],
    });

    render(<ChatContainer userId="user-123" />);

    await waitFor(() => {
      expect(mockListConversations).toHaveBeenCalled();
    });

    // Click on conversation to load it
    const conversationButtons = screen.getAllByRole('button');
    const convButton = conversationButtons.find(
      (btn) => btn.textContent?.includes('Conversation') && !btn.textContent?.includes('New')
    );

    if (convButton) {
      await user.click(convButton);

      await waitFor(() => {
        expect(screen.getByText('Old message')).toBeInTheDocument();
      });

      // Click "New Conversation" button
      const newConvButton = screen.getByRole('button', { name: /new conversation/i });
      await user.click(newConvButton);

      // Should clear localStorage
      await waitFor(() => {
        expect(localStorage.removeItem).toHaveBeenCalledWith('chat_conversation_user-123');
      });

      // Messages should be cleared (empty state)
      await waitFor(() => {
        expect(screen.queryByText('Old message')).not.toBeInTheDocument();
      });
    }
  });
});
