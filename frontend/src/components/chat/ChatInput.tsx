/**
 * ChatInput component for message submission.
 *
 * Task ID: T127
 * Spec: specs/001-chat-interface/spec.md
 */

'use client';

import { useState, KeyboardEvent } from 'react';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/textarea';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading?: boolean;
}

export default function ChatInput({ onSend, isLoading = false }: ChatInputProps) {
  const [message, setMessage] = useState('');

  const handleSubmit = () => {
    if (!message.trim() || isLoading) return;

    onSend(message);
    setMessage(''); // Clear input after submission
  };

  // Handle Enter key submission (Shift+Enter for new line)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex gap-2">
      <Textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={isLoading ? "Waiting for response..." : "Type your message... (Press Enter to send, Shift+Enter for new line)"}
        disabled={false}
        className={`min-h-[60px] max-h-[200px] resize-none ${isLoading ? 'opacity-75' : ''}`}
        rows={2}
      />
      <Button
        onClick={handleSubmit}
        disabled={isLoading || !message.trim()}
        size="icon"
        className="h-[60px] w-[60px] shrink-0"
      >
        {isLoading ? (
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-gray-300 border-t-blue-600" />
        ) : (
          <>
            <Send className="h-5 w-5" />
            <span className="sr-only">Send message</span>
          </>
        )}
      </Button>
    </div>
  );
}
