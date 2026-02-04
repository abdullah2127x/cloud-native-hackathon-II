/**
 * Chat interface page for conversational task management.
 *
 * Task ID: T121
 * Spec: specs/001-chat-interface/spec.md
 * User Story: US1 - Start a New Chat Conversation
 */

import { redirect } from 'next/navigation';
import { auth } from '@/lib/auth-client';
import ChatContainer from '@/components/chat/ChatContainer';

export default async function ChatPage() {
  // Server component with Better Auth session check
  const session = await auth();

  // Redirect to login if unauthenticated
  if (!session?.user) {
    redirect('/auth/signin');
  }

  return (
    <div className="container mx-auto h-[calc(100vh-4rem)] p-4">
      <div className="flex h-full flex-col">
        <div className="mb-4">
          <h1 className="text-2xl font-bold">Chat Assistant</h1>
          <p className="text-sm text-muted-foreground">
            Manage your tasks through natural conversation
          </p>
        </div>
        <div className="flex-1 overflow-hidden rounded-lg border bg-card">
          <ChatContainer userId={session.user.id} />
        </div>
      </div>
    </div>
  );
}
