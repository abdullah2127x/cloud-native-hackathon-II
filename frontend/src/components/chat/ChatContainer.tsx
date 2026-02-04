/**
 * ChatContainer component with OpenAI ChatKit integration.
 *
 * Task IDs: T122, T123, T124, T225, T226, T227
 * Spec: specs/001-chat-interface/spec.md
 * Research: specs/001-chat-interface/research.md (Task 1 - Custom Fetch)
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
import { useChatKit } from '@openai/chatkit';
import { useSession } from '@/lib/auth-client';
import { getConversation, type Message } from '@/lib/api/chat';
import MessageList from './MessageList';
import ChatInput from './ChatInput';

interface ChatContainerProps {
  userId: string;
}

export default function ChatContainer({ userId }: ChatContainerProps) {
  const { data: session } = useSession();
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Array<{ role: string; content: string; id: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // T226: Load conversation_id from localStorage on mount
  useEffect(() => {
    const storedConversationId = localStorage.getItem(`chat_conversation_${userId}`);
    if (storedConversationId) {
      setConversationId(storedConversationId);
    }
  }, [userId]);

  // T227: Load conversation history if conversation_id exists
  useEffect(() => {
    const loadConversationHistory = async () => {
      if (!conversationId || !session?.token) return;

      setIsLoadingHistory(true);
      setError(null);

      try {
        const conversation = await getConversation(userId, conversationId, session.token);

        // Convert API messages to component format
        const formattedMessages = conversation.messages.map((msg: Message) => ({
          id: msg.id,
          role: msg.role,
          content: msg.content,
        }));

        setMessages(formattedMessages);
      } catch (err) {
        console.error('Failed to load conversation history:', err);
        // Clear invalid conversation ID
        setConversationId(null);
        localStorage.removeItem(`chat_conversation_${userId}`);
        setError('Failed to load conversation history');
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadConversationHistory();
  }, [conversationId, userId, session?.token]);

  // T123: Custom fetch function with JWT injection
  const customFetch = useCallback(
    async (input: RequestInfo | URL, init?: RequestInit) => {
      if (!session?.token) {
        throw new Error('No authentication token available');
      }

      return fetch(input, {
        ...init,
        headers: {
          ...init?.headers,
          'Authorization': `Bearer ${session.token}`,
          'Content-Type': 'application/json',
        },
      });
    },
    [session]
  );

  // T122: Initialize ChatKit with custom fetch and domain key
  const { control } = useChatKit({
    api: {
      url: `/api/${userId}/chat`,
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY || '',
      fetch: customFetch,
    },
    // T124: Error handler
    onError: ({ error: err }) => {
      console.error('Chat error:', err);
      setError(err.message || 'An error occurred. Please try again.');
      setIsLoading(false);
    },
  });

  // Handle message submission
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session?.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: message.trim(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }

      const data = await response.json();

      // T226: Update and persist conversation ID if new conversation
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
        localStorage.setItem(`chat_conversation_${userId}`, data.conversation_id);
      }

      // Add user message and assistant response to messages
      setMessages((prev) => [
        ...prev,
        { role: 'user', content: message, id: `user-${Date.now()}` },
        {
          role: 'assistant',
          content: data.message,
          id: `assistant-${Date.now()}`,
        },
      ]);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An error occurred';
      setError(errorMessage);
      console.error('Failed to send message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      {error && (
        <div className="border-b border-destructive bg-destructive/10 p-3 text-sm text-destructive">
          {error}
        </div>
      )}

      {isLoadingHistory && (
        <div className="flex items-center justify-center p-4 text-sm text-muted-foreground">
          Loading conversation history...
        </div>
      )}

      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>

      <div className="border-t p-4">
        <ChatInput onSend={handleSendMessage} disabled={isLoading || isLoadingHistory} />
      </div>
    </div>
  );
}
