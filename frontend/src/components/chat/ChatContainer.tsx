/**
 * ChatContainer component with OpenAI ChatKit integration.
 *
 * Task IDs: T122, T123, T124
 * Spec: specs/001-chat-interface/spec.md
 * Research: specs/001-chat-interface/research.md (Task 1 - Custom Fetch)
 */

'use client';

import { useState, useCallback } from 'react';
import { useChatKit } from '@openai/chatkit';
import { useSession } from '@/lib/auth-client';
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
  const [error, setError] = useState<string | null>(null);

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

      // Update conversation ID if new conversation
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
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

      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>

      <div className="border-t p-4">
        <ChatInput onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
