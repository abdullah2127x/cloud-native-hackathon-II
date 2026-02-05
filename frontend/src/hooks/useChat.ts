/**
 * Hook for managing chat conversation state.
 *
 * Task ID: T224
 * Spec: specs/001-chat-interface/spec.md
 */

import { useState, useCallback } from 'react';
import { sendMessage } from '@/lib/api/chat';
import { useSession, getJwtToken } from '@/lib/auth-client';

interface UseChatResult {
  conversationId: string | null;
  setConversationId: (id: string | null) => void;
  sendChatMessage: (message: string) => Promise<void>;
  isSubmitting: boolean;
  error: string | null;
}

/**
 * Hook to manage conversation_id state and message submission.
 *
 * @param userId - Authenticated user ID
 * @param onMessageSent - Callback invoked after message is successfully sent
 * @returns Conversation state, send function, submitting state, and error state
 */
export function useChat(
  userId: string,
  onMessageSent?: (conversationId: string) => void
): UseChatResult {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { data: session } = useSession();

  const sendChatMessage = useCallback(
    async (message: string): Promise<void> => {
      const token = getJwtToken();
      if (!token) {
        setError('No authentication token');
        return;
      }

      if (!message.trim()) {
        setError('Message cannot be empty');
        return;
      }

      try {
        setIsSubmitting(true);
        setError(null);

        const response = await sendMessage(
          userId,
          message,
          conversationId,
          token
        );

        // Update conversation ID if this was a new conversation
        if (!conversationId) {
          setConversationId(response.conversation_id);
        }

        // Notify parent component
        if (onMessageSent) {
          onMessageSent(response.conversation_id);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to send message');
        console.error('Error sending message:', err);
        throw err; // Re-throw so ChatKit can handle it
      } finally {
        setIsSubmitting(false);
      }
    },
    [userId, conversationId, onMessageSent]
  );

  return {
    conversationId,
    setConversationId,
    sendChatMessage,
    isSubmitting,
    error,
  };
}
