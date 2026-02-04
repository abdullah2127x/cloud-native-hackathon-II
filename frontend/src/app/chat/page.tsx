/**
 * Chat interface page for conversational task management.
 *
 * Task ID: T121
 * Spec: specs/001-chat-interface/spec.md
 * User Story: US1 - Start a New Chat Conversation
 */

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from '@/lib/auth-client';
import ChatContainer from '@/components/chat/ChatContainer';

export default function ChatPage() {
  const router = useRouter();
  const { data: session, isPending } = useSession();

  useEffect(() => {
    // Redirect to login if unauthenticated and session check is complete
    if (!isPending && !session?.user) {
      router.push('/sign-in');
    }
  }, [session, isPending, router]);

  // Show loading state while checking session
  if (isPending) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="mb-4 h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Redirect if no user (double-check)
  if (!session?.user) {
    return null;
  }

  // Debug: Log session data
  console.log('Session data:', { userId: session.user.id, userName: session.user.name, userEmail: session.user.email });

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
