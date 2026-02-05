/**
 * ConversationSidebar component for displaying conversation history.
 *
 * Task IDs: T301, T302, T303, T304
 * Spec: specs/001-chat-interface/spec.md
 */

'use client';

import { useConversationHistory } from '@/hooks/useConversationHistory';
import { getConversation, type ConversationSummary } from '@/lib/api/chat';
import { useSession, getJwtToken } from '@/lib/auth-client';
import { Button } from '@/components/ui/Button';
import { PlusCircle, MessageSquare } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ConversationSidebarProps {
  userId: string;
  currentConversationId: string | null;
  onConversationSelect: (conversationId: string) => void;
  onNewConversation: () => void;
  onConversationLoad?: (messages: Array<{ id: string; role: string; content: string }>) => void;
}

export default function ConversationSidebar({
  userId,
  currentConversationId,
  onConversationSelect,
  onNewConversation,
  onConversationLoad,
}: ConversationSidebarProps) {
  const { conversations, isLoading, error, refetch } = useConversationHistory(userId);

  // T303: Click handler to load conversation
  const handleConversationClick = async (conversation: ConversationSummary) => {
    const token = getJwtToken();
    if (!token) {
      console.error('[ConversationSidebar] No auth token available');
      return;
    }

    console.log('[ConversationSidebar] Clicked conversation:', conversation.id);

    try {
      console.log('[ConversationSidebar] Fetching conversation with ID:', conversation.id, 'for user:', userId);

      // Fetch full conversation with messages
      const fullConversation = await getConversation(
        userId,
        conversation.id,
        token
      );

      console.log('[ConversationSidebar] Received conversation:', fullConversation);

      // Convert messages to component format
      const formattedMessages = fullConversation.messages.map((msg) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
      }));

      console.log('[ConversationSidebar] Formatted messages:', formattedMessages);

      // Notify parent component
      onConversationSelect(conversation.id);
      console.log('[ConversationSidebar] Called onConversationSelect with:', conversation.id);

      if (onConversationLoad) {
        onConversationLoad(formattedMessages);
        console.log('[ConversationSidebar] Called onConversationLoad with', formattedMessages.length, 'messages');
      } else {
        console.warn('[ConversationSidebar] onConversationLoad callback not provided');
      }
    } catch (err) {
      console.error('[ConversationSidebar] Failed to load conversation:', err);
      if (err instanceof Error) {
        console.error('[ConversationSidebar] Error message:', err.message);
        console.error('[ConversationSidebar] Error stack:', err.stack);
      }
    }
  };

  // T304: New Conversation button handler
  const handleNewConversation = () => {
    onNewConversation();
  };

  // Format timestamp to relative time
  const formatTimestamp = (timestamp: string): string => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="flex h-full flex-col border-r bg-muted/10">
      {/* T304: New Conversation Button */}
      <div className="border-b p-4">
        <Button
          onClick={handleNewConversation}
          className="w-full justify-start gap-2"
          variant="outline"
        >
          <PlusCircle className="h-4 w-4" />
          New Conversation
        </Button>
      </div>

      {/* T301: Conversation List */}
      <div className="flex-1 overflow-y-auto">
        {isLoading && (
          <div className="flex flex-col items-center justify-center gap-3 p-4">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
            <p className="text-xs text-muted-foreground">Loading conversations...</p>
          </div>
        )}

        {error && (
          <div className="p-4 text-center text-sm text-destructive">
            {error}
          </div>
        )}

        {!isLoading && !error && conversations.length === 0 && (
          <div className="p-4 text-center text-sm text-muted-foreground">
            <MessageSquare className="mx-auto mb-2 h-8 w-8 opacity-50" />
            <p>No conversations yet</p>
            <p className="mt-1 text-xs">Start a new conversation to get started</p>
          </div>
        )}

        {/* T302: Conversation Item Rendering */}
        <div className="space-y-1 p-2">
          {conversations.map((conversation) => {
            const isActive = conversation.id === currentConversationId;

            return (
              <button
                key={conversation.id}
                onClick={() => handleConversationClick(conversation)}
                className={cn(
                  'w-full rounded-lg p-3 text-left transition-colors hover:bg-accent',
                  isActive && 'bg-accent/50 font-medium'
                )}
              >
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 overflow-hidden">
                    <div className="flex items-center gap-2">
                      <MessageSquare className="h-4 w-4 flex-shrink-0" />
                      <span className="text-sm">
                        Conversation
                      </span>
                    </div>
                    {/* T302: Display timestamp */}
                    <p className="mt-1 text-xs text-muted-foreground">
                      {formatTimestamp(conversation.updated_at)}
                    </p>
                  </div>
                  {isActive && (
                    <div className="h-2 w-2 rounded-full bg-primary" />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
