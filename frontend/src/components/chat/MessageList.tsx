/**
 * MessageList component with React Virtuoso for virtual scrolling.
 *
 * Task IDs: T125, T126
 * Spec: specs/001-chat-interface/spec.md
 * Research: specs/001-chat-interface/research.md (Task 2 - Virtual Scrolling)
 */

'use client';

import { useEffect, useRef } from 'react';
import { Virtuoso, VirtuosoHandle } from 'react-virtuoso';
import { cn } from '@/lib/utils';

interface Message {
  role: string;
  content: string;
  id: string;
}

interface MessageListProps {
  messages: Message[];
  isLoading?: boolean;
}

export default function MessageList({ messages, isLoading = false }: MessageListProps) {
  const virtuosoRef = useRef<VirtuosoHandle>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (messages.length > 0) {
      virtuosoRef.current?.scrollToIndex({
        index: messages.length - 1,
        behavior: 'smooth',
      });
    }
  }, [messages]);

  // Scroll to bottom when loading state changes
  useEffect(() => {
    if (isLoading && messages.length > 0) {
      virtuosoRef.current?.scrollToIndex({
        index: messages.length,
        behavior: 'smooth',
      });
    }
  }, [isLoading, messages.length]);

  if (messages.length === 0) {
    return (
      <div className="flex h-full items-center justify-center p-8 text-center">
        <div className="space-y-2">
          <p className="text-lg font-medium">Start a conversation</p>
          <p className="text-sm text-muted-foreground">
            Type a message below to begin chatting with your AI assistant
          </p>
        </div>
      </div>
    );
  }

  // T125: Configure React Virtuoso with initialTopMostItemIndex and followOutput
  return (
    <div className="flex h-full flex-col">
      <Virtuoso
        ref={virtuosoRef}
        data={messages}
        initialTopMostItemIndex={messages.length - 1}
        followOutput="smooth"
        className="flex-1"
        itemContent={(index, message) => (
          <MessageBubble key={message.id} message={message} />
        )}
      />
      {/* Typing indicator shown outside Virtuoso */}
      {isLoading && (
        <div className="flex w-full px-4 py-3">
          <div className="flex items-center gap-1 rounded-lg bg-muted px-4 py-2">
            <span className="text-sm text-muted-foreground">AI is typing</span>
            <div className="flex gap-1">
              <span className="inline-block h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0ms' }} />
              <span className="inline-block h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '150ms' }} />
              <span className="inline-block h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// T126: Message rendering with user/assistant alignment
function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user';

  return (
    <div
      className={cn(
        'flex w-full px-4 py-3',
        isUser ? 'justify-end' : 'justify-start'
      )}
    >
      <div
        className={cn(
          'max-w-[80%] rounded-lg px-4 py-2',
          isUser
            ? 'bg-primary text-primary-foreground'
            : 'bg-muted text-foreground'
        )}
      >
        <div className="whitespace-pre-wrap break-words text-sm">
          {message.content}
        </div>
      </div>
    </div>
  );
}
