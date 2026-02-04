/**
 * ChatContainer component with OpenAI ChatKit integration.
 *
 * Task IDs: T122, T123, T124, T225, T226, T227, T305, T306
 * Spec: specs/001-chat-interface/spec.md
 * Research: specs/001-chat-interface/research.md (Task 1 - Custom Fetch)
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
import { useChatKit } from '@openai/chatkit';
import { useSession } from '@/lib/auth-client';
import { getConversation, type Message } from '@/lib/api/chat';
import { Button } from '@/components/ui/button';
import { Menu, X } from 'lucide-react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import ConversationSidebar from './ConversationSidebar';

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
  // T306: Mobile sidebar state
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

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

  // T305: Handle conversation selection from sidebar
  const handleConversationSelect = (selectedConversationId: string) => {
    setConversationId(selectedConversationId);
    localStorage.setItem(`chat_conversation_${userId}`, selectedConversationId);
    setIsSidebarOpen(false); // Close mobile sidebar after selection
  };

  // T305: Handle conversation load (set messages)
  const handleConversationLoad = (loadedMessages: Array<{ id: string; role: string; content: string }>) => {
    setMessages(loadedMessages);
    setError(null);
  };

  // T305: Handle new conversation
  const handleNewConversation = () => {
    setConversationId(null);
    setMessages([]);
    setError(null);
    localStorage.removeItem(`chat_conversation_${userId}`);
    setIsSidebarOpen(false); // Close mobile sidebar after action
  };

  return (
    <div className="flex h-full">
      {/* T305/T306: Sidebar - Desktop: always visible, Mobile: collapsible */}
      <div className="hidden md:block md:w-80">
        <ConversationSidebar
          userId={userId}
          currentConversationId={conversationId}
          onConversationSelect={handleConversationSelect}
          onNewConversation={handleNewConversation}
          onConversationLoad={handleConversationLoad}
        />
      </div>

      {/* T306: Mobile sidebar overlay */}
      {isSidebarOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40 bg-black/50 md:hidden"
            onClick={() => setIsSidebarOpen(false)}
          />
          {/* Sidebar */}
          <div className="fixed inset-y-0 left-0 z-50 w-80 bg-background md:hidden">
            <ConversationSidebar
              userId={userId}
              currentConversationId={conversationId}
              onConversationSelect={handleConversationSelect}
              onNewConversation={handleNewConversation}
              onConversationLoad={handleConversationLoad}
            />
          </div>
        </>
      )}

      {/* Main chat area */}
      <div className="flex flex-1 flex-col">
        {/* T306: Mobile hamburger menu */}
        <div className="flex items-center border-b p-3 md:hidden">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          >
            {isSidebarOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </Button>
          <h1 className="ml-2 text-sm font-medium">Chat Assistant</h1>
        </div>

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
    </div>
  );
}
