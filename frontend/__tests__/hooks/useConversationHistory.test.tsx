/**
 * useConversationHistory hook tests.
 *
 * Task ID: T228
 * Spec: specs/001-chat-interface/spec.md
 */

import { renderHook, waitFor } from '@testing-library/react';
import { useConversationHistory } from '@/hooks/useConversationHistory';
import { useSession } from '@/lib/auth-client';
import * as chatApi from '@/lib/api/chat';

jest.mock('@/lib/auth-client');
jest.mock('@/lib/api/chat');

const mockUseSession = useSession as jest.MockedFunction<typeof useSession>;
const mockListConversations = chatApi.listConversations as jest.MockedFunction<
  typeof chatApi.listConversations
>;

describe('useConversationHistory', () => {
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

  it('fetches conversations on mount', async () => {
    const mockConversations = [
      {
        id: 'conv-1',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
      {
        id: 'conv-2',
        created_at: '2024-01-02T00:00:00Z',
        updated_at: '2024-01-02T00:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 2,
      limit: 20,
      offset: 0,
    });

    const { result } = renderHook(() => useConversationHistory('user-123'));

    // Initially loading
    expect(result.current.isLoading).toBe(true);
    expect(result.current.conversations).toEqual([]);

    // Wait for fetch to complete
    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(mockListConversations).toHaveBeenCalledWith('user-123', 'mock-token');
    expect(result.current.conversations).toEqual(mockConversations);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    mockListConversations.mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useConversationHistory('user-123'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBe('Network error');
    expect(result.current.conversations).toEqual([]);
  });

  it('handles missing token', async () => {
    mockUseSession.mockReturnValue({
      data: null,
      isPending: false,
    } as any);

    const { result } = renderHook(() => useConversationHistory('user-123'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.error).toBe('No authentication token');
    expect(mockListConversations).not.toHaveBeenCalled();
  });

  it('refetch function reloads conversations', async () => {
    const mockConversations = [
      {
        id: 'conv-1',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
    ];

    mockListConversations.mockResolvedValue({
      conversations: mockConversations,
      total: 1,
      limit: 20,
      offset: 0,
    });

    const { result } = renderHook(() => useConversationHistory('user-123'));

    await waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    // Clear mock and call refetch
    mockListConversations.mockClear();
    await result.current.refetch();

    expect(mockListConversations).toHaveBeenCalledTimes(1);
  });
});
