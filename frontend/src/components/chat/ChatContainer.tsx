/**
 * ChatContainer component with OpenAI ChatKit integration.
 *
 * Task IDs: T122, T123, T124, T225, T226, T227, T305, T306, T422, T423, T424, T425, T426
 * Spec: specs/001-chat-interface/spec.md
 * Research: specs/001-chat-interface/research.md (Task 1 - Custom Fetch)
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
// import { useChatKit } from '@openai/chatkit';
import { useSession, getJwtToken } from '@/lib/auth-client';
import { getConversation, type Message } from '@/lib/api/chat';
import { Button } from '@/components/ui/Button';
import { Menu, X } from 'lucide-react';
import MessageList from './MessageList';
import ChatInput from './ChatInput';
import ConversationSidebar from './ConversationSidebar';
import ErrorMessage from './ErrorMessage';
import { classifyError, type ClassifiedError } from '@/lib/error-classifier';

interface ChatContainerProps {
  userId: string;
}

export default function ChatContainer({ userId }: ChatContainerProps) {
  const { data: session } = useSession();
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Array<{ role: string; content: string; id: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [classifiedError, setClassifiedError] = useState<ClassifiedError | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [lastMessage, setLastMessage] = useState<string | null>(null);
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
      if (!conversationId) return;

      const token = getJwtToken();
      if (!token) {
        setIsLoadingHistory(false);
        return;
      }

      setIsLoadingHistory(true);
      setClassifiedError(null);
      setRetryCount(0);

      try {
        const conversation = await getConversation(userId, conversationId, token);

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
        const error = classifyError(err);
        setClassifiedError(error);
      } finally {
        setIsLoadingHistory(false);
      }
    };

    loadConversationHistory();
  }, [conversationId, userId]);

  // T122-T124: ChatKit integration commented out
  // Using custom fetch and manual state management instead for full control
  // See: handleSendMessage() for stateless API implementation

  // T422/T424: Handle message submission with error classification and retry logic
  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    const token = getJwtToken();
    if (!token) {
      const error = classifyError(new Error('No authentication token'));
      setClassifiedError(error);
      return;
    }

    // Optimistic update: Add user message immediately (FR-017)
    const userMessageId = `user-${Date.now()}`;
    setMessages((prev) => [
      ...prev,
      { role: 'user', content: message, id: userMessageId },
    ]);

    setLastMessage(message);
    setIsLoading(true);
    setClassifiedError(null);

    try {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiBaseUrl}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
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

      // Clear error and retry count on success
      setRetryCount(0);
      setLastMessage(null);

      // Add only assistant response (user message already added optimistically)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.message,
          id: `assistant-${Date.now()}`,
        },
      ]);
    } catch (err) {
      // Remove optimistic user message on error
      setMessages((prev) => prev.filter((msg) => msg.id !== userMessageId));

      // T423: Classify error for empathetic messaging
      const error = classifyError(err);
      setClassifiedError(error);
      console.error('Failed to send message:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // T424: Handle retry with exponential backoff
  const handleRetry = async () => {
    if (!lastMessage) return;

    // T424: Calculate exponential backoff delay (1s, 2s, 4s, 8s, ...)
    const delay = 1000 * Math.pow(2, retryCount);

    setRetryCount((prev) => prev + 1);

    // Wait for exponential backoff before retrying
    await new Promise((resolve) => setTimeout(resolve, delay));

    // Retry sending the message
    await handleSendMessage(lastMessage);
  };

  // T305: Handle conversation selection from sidebar
  const handleConversationSelect = (selectedConversationId: string) => {
    console.log('[ChatContainer] handleConversationSelect called with:', selectedConversationId);
    setConversationId(selectedConversationId);
    localStorage.setItem(`chat_conversation_${userId}`, selectedConversationId);
    setIsSidebarOpen(false); // Close mobile sidebar after selection
    console.log('[ChatContainer] Set conversation ID and saved to localStorage');
  };

  // T305: Handle conversation load (set messages)
  const handleConversationLoad = (loadedMessages: Array<{ id: string; role: string; content: string }>) => {
    console.log('[ChatContainer] handleConversationLoad called with', loadedMessages.length, 'messages');
    console.log('[ChatContainer] Messages:', loadedMessages);
    setMessages(loadedMessages);
    setClassifiedError(null);
    setRetryCount(0);
    console.log('[ChatContainer] Updated state with', loadedMessages.length, 'messages');
  };

  // T305: Handle new conversation
  const handleNewConversation = () => {
    setConversationId(null);
    setMessages([]);
    setClassifiedError(null);
    setRetryCount(0);
    setLastMessage(null);
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

        {/* T422: Integrate ErrorMessage with retry capability */}
        {classifiedError && (
          <div className="border-b p-4">
            <ErrorMessage
              message={classifiedError.message}
              onRetry={handleRetry}
              isRetrying={isLoading}
            />
          </div>
        )}

        {isLoadingHistory && (
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3 bg-background/50 backdrop-blur-sm">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
            <p className="text-sm text-muted-foreground">Loading conversation history...</p>
          </div>
        )}

        <div className="flex-1 overflow-hidden">
          <MessageList messages={messages} isLoading={isLoading} />
        </div>

        <div className="border-t p-4">
          {/* T425: Keep input enabled during error state (FR-017) - optimistic updates enabled */}
          <ChatInput onSend={handleSendMessage} isLoading={isLoading || isLoadingHistory} />
        </div>
      </div>
    </div>
  );
}


