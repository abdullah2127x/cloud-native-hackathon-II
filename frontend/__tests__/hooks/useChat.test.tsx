/**
 * useChat hook tests.
 *
 * Task ID: T229
 * Spec: specs/001-chat-interface/spec.md
 */

import { renderHook, waitFor, act } from '@testing-library/react';
import { useChat } from '@/hooks/useChat';
import { useSession } from '@/lib/auth-client';
import * as chatApi from '@/lib/api/chat';

jest.mock('@/lib/auth-client');
jest.mock('@/lib/api/chat');

const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;
const mockSendMessage = chatApi.sendMessage as jest.MockedFunction<typeof chatApi.sendMessage>;

describe('useChat', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockUseSession.mockReturnValue({
      data: {
        user: { id: 'user-123', email: 'test@example.com' },
        token: 'mock-token',
      },
      isPending: false,
    } as any);
  });

  it('manages conversation_id state correctly', async () => {
    mockSendMessage.mockResolvedValue({
      conversation_id: 'conv-123',
      message: 'AI response',
      role: 'assistant',
      created_at: '2024-01-01T00:00:00Z',
    });

    const { result } = renderHook(() => useChat('user-123'));

    // Initially no conversation
    expect(result.current.conversationId).toBeNull();

    // Send first message
    await act(async () => {
      await result.current.sendChatMessage('Hello');
    });

    // Conversation ID should be set
    await waitFor(() => {
      expect(result.current.conversationId).toBe('conv-123');
    });

    expect(mockSendMessage).toHaveBeenCalledWith('user-123', 'Hello', null, 'mock-token');
  });

  it('maintains conversation_id on subsequent messages', async () => {
    mockSendMessage.mockResolvedValue({
      conversation_id: 'conv-123',
      message: 'AI response',
      role: 'assistant',
      created_at: '2024-01-01T00:00:00Z',
    });

    const { result } = renderHook(() => useChat('user-123'));

    // Send first message
    await act(async () => {
      await result.current.sendChatMessage('First message');
    });

    await waitFor(() => {
      expect(result.current.conversationId).toBe('conv-123');
    });

    // Send second message
    await act(async () => {
      await result.current.sendChatMessage('Second message');
    });

    // Should use existing conversation ID
    expect(mockSendMessage).toHaveBeenLastCalledWith(
      'user-123',
      'Second message',
      'conv-123',
      'mock-token'
    );
  });

  it('calls onMessageSent callback after successful send', async () => {
    const onMessageSent = jest.fn();

    mockSendMessage.mockResolvedValue({
      conversation_id: 'conv-123',
      message: 'AI response',
      role: 'assistant',
      created_at: '2024-01-01T00:00:00Z',
    });

    const { result } = renderHook(() => useChat('user-123', onMessageSent));

    await act(async () => {
      await result.current.sendChatMessage('Hello');
    });

    await waitFor(() => {
      expect(onMessageSent).toHaveBeenCalledWith('conv-123');
    });
  });

  it('handles send error', async () => {
    mockSendMessage.mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useChat('user-123'));

    await act(async () => {
      try {
        await result.current.sendChatMessage('Hello');
      } catch (err) {
        // Expected to throw
      }
    });

    await waitFor(() => {
      expect(result.current.error).toBe('Network error');
    });
  });

  it('handles missing token', async () => {
    mockUseSession.mockReturnValue({
      data: null,
      isPending: false,
    } as any);

    const { result } = renderHook(() => useChat('user-123'));

    await act(async () => {
      await result.current.sendChatMessage('Hello');
    });

    expect(result.current.error).toBe('No authentication token');
    expect(mockSendMessage).not.toHaveBeenCalled();
  });

  it('handles empty message', async () => {
    const { result } = renderHook(() => useChat('user-123'));

    await act(async () => {
      await result.current.sendChatMessage('   ');
    });

    expect(result.current.error).toBe('Message cannot be empty');
    expect(mockSendMessage).not.toHaveBeenCalled();
  });

  it('allows manual conversation_id update', () => {
    const { result } = renderHook(() => useChat('user-123'));

    act(() => {
      result.current.setConversationId('manual-conv-id');
    });

    expect(result.current.conversationId).toBe('manual-conv-id');
  });
});
