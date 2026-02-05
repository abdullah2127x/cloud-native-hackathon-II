/**
 * ConversationSidebar component tests.
 *
 * Task IDs: T307, T308, T309
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ConversationSidebar from '@/components/chat/ConversationSidebar';
import { useConversationHistory } from '@/hooks/useConversationHistory';
import { useSession } from '@/lib/auth-client';
import * as chatApi from '@/lib/api/chat';

jest.mock('@/hooks/useConversationHistory');
jest.mock('@/lib/auth-client');
jest.mock('@/lib/api/chat');

const mockUseConversationHistory = useConversationHistory as jest.MockedFunction<
  typeof useConversationHistory
>;
const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;
const mockGetConversation = chatApi.getConversation as jest.MockedFunction<
  typeof chatApi.getConversation
>;

describe('ConversationSidebar', () => {
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

  beforeEach(() => {
    jest.clearAllMocks();

    mockUseSession.mockReturnValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        token: 'mock-token',
      },
      isPending: false,
    } as any);

    mockUseConversationHistory.mockReturnValue({
      conversations: mockConversations,
      isLoading: false,
      error: null,
      refetch: jest.fn(),
    });
  });

  // T307: Renders conversation list correctly
  it('renders conversation list correctly', () => {
    const onConversationSelect = jest.fn();
    const onNewConversation = jest.fn();

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={onConversationSelect}
        onNewConversation={onNewConversation}
      />
    );

    // Should render "New Conversation" button
    expect(screen.getByText(/new conversation/i)).toBeInTheDocument();

    // Should render all conversations
    const conversationButtons = screen.getAllByRole('button', { name: /conversation/i });
    // +1 for "New Conversation" button
    expect(conversationButtons.length).toBeGreaterThanOrEqual(mockConversations.length);
  });

  it('displays loading state', () => {
    mockUseConversationHistory.mockReturnValue({
      conversations: [],
      isLoading: true,
      error: null,
      refetch: jest.fn(),
    });

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={jest.fn()}
        onNewConversation={jest.fn()}
      />
    );

    expect(screen.getByText(/loading conversations/i)).toBeInTheDocument();
  });

  it('displays error state', () => {
    mockUseConversationHistory.mockReturnValue({
      conversations: [],
      isLoading: false,
      error: 'Failed to load conversations',
      refetch: jest.fn(),
    });

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={jest.fn()}
        onNewConversation={jest.fn()}
      />
    );

    expect(screen.getByText(/failed to load conversations/i)).toBeInTheDocument();
  });

  it('displays empty state when no conversations', () => {
    mockUseConversationHistory.mockReturnValue({
      conversations: [],
      isLoading: false,
      error: null,
      refetch: jest.fn(),
    });

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={jest.fn()}
        onNewConversation={jest.fn()}
      />
    );

    expect(screen.getByText(/no conversations yet/i)).toBeInTheDocument();
  });

  it('highlights active conversation', () => {
    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId="conv-2"
        onConversationSelect={jest.fn()}
        onNewConversation={jest.fn()}
      />
    );

    // Find all conversation buttons
    const buttons = screen.getAllByRole('button');

    // The active conversation should have a visual indicator
    // Check for the presence of the active indicator dot
    const activeDot = document.querySelector('.bg-primary');
    expect(activeDot).toBeInTheDocument();
  });

  // T308: Clicking conversation loads that conversation
  it('loads conversation when clicked', async () => {
    const user = userEvent.setup();
    const onConversationSelect = jest.fn();
    const onConversationLoad = jest.fn();

    const mockFullConversation = {
      id: 'conv-1',
      created_at: '2024-01-01T10:00:00Z',
      updated_at: '2024-01-01T10:00:00Z',
      messages: [
        {
          id: 'msg-1',
          role: 'user' as const,
          content: 'Hello',
          created_at: '2024-01-01T10:00:00Z',
        },
        {
          id: 'msg-2',
          role: 'assistant' as const,
          content: 'Hi there!',
          created_at: '2024-01-01T10:00:01Z',
        },
      ],
    };

    mockGetConversation.mockResolvedValue(mockFullConversation);

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={onConversationSelect}
        onNewConversation={jest.fn()}
        onConversationLoad={onConversationLoad}
      />
    );

    // Click on first conversation
    const conversationButtons = screen.getAllByRole('button');
    const firstConversationButton = conversationButtons.find(
      (btn) => btn.textContent?.includes('Conversation') && !btn.textContent?.includes('New')
    );

    if (firstConversationButton) {
      await user.click(firstConversationButton);
    }

    // Should fetch conversation
    await waitFor(() => {
      expect(mockGetConversation).toHaveBeenCalledWith('user-123', 'conv-1', 'mock-token');
    });

    // Should call callbacks
    await waitFor(() => {
      expect(onConversationSelect).toHaveBeenCalledWith('conv-1');
      expect(onConversationLoad).toHaveBeenCalledWith([
        { id: 'msg-1', role: 'user', content: 'Hello' },
        { id: 'msg-2', role: 'assistant', content: 'Hi there!' },
      ]);
    });
  });

  // T309: "New Conversation" button creates fresh state
  it('handles new conversation button click', async () => {
    const user = userEvent.setup();
    const onNewConversation = jest.fn();

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId="conv-1"
        onConversationSelect={jest.fn()}
        onNewConversation={onNewConversation}
      />
    );

    // Click "New Conversation" button
    const newConversationButton = screen.getByRole('button', {
      name: /new conversation/i,
    });
    await user.click(newConversationButton);

    // Should call callback
    expect(onNewConversation).toHaveBeenCalled();
  });

  it('displays relative timestamps', () => {
    // Mock Date to control relative time calculations
    const now = new Date('2024-01-03T12:30:00Z');
    jest.spyOn(global, 'Date').mockImplementation(() => now as any);

    render(
      <ConversationSidebar
        userId="user-123"
        currentConversationId={null}
        onConversationSelect={jest.fn()}
        onNewConversation={jest.fn()}
      />
    );

    // Should display relative times like "30m ago", "1d ago", etc.
    // The exact format depends on the time difference
    const timestamps = screen.getAllByText(/ago|Just now/i);
    expect(timestamps.length).toBeGreaterThan(0);

    jest.restoreAllMocks();
  });
});
