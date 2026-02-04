/**
 * Hook for managing conversation history.
 *
 * Task ID: T221
 * Spec: specs/001-chat-interface/spec.md
 */

import { useState, useEffect } from 'react';
import { listConversations, type ConversationSummary } from '@/lib/api/chat';
import { useSession } from '@/lib/auth-client';

interface UseConversationHistoryResult {
  conversations: ConversationSummary[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

/**
 * Hook to fetch and manage conversation list on mount.
 *
 * @param userId - Authenticated user ID
 * @returns Conversations state, loading state, error state, and refetch function
 */
export function useConversationHistory(userId: string): UseConversationHistoryResult {
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { data: session } = useSession();

  const fetchConversations = async (): Promise<void> => {
    if (!session?.token) {
      setError('No authentication token');
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const result = await listConversations(userId, session.token);
      setConversations(result.conversations);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch conversations');
      console.error('Error fetching conversations:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, [userId, session?.token]);

  return {
    conversations,
    isLoading,
    error,
    refetch: fetchConversations,
  };
}
