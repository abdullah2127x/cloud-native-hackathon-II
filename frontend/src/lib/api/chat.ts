/**
 * Chat API client functions.
 *
 * Task IDs: T129, T222, T223
 * Spec: specs/001-chat-interface/spec.md
 */

interface ChatRequest {
  conversation_id?: string;
  message: string;
}

interface ChatResponse {
  conversation_id: string;
  message: string;
  role: 'assistant';
  created_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface ConversationSummary {
  id: string;
  created_at: string;
  updated_at: string;
}

export interface ConversationList {
  conversations: ConversationSummary[];
  total: number;
  limit: number;
  offset: number;
}

export interface ConversationDetail {
  id: string;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

/**
 * Send a message to the chat endpoint.
 *
 * @param userId - Authenticated user ID
 * @param message - User message content
 * @param conversationId - Optional conversation ID to continue existing conversation
 * @param token - JWT authentication token
 */
export async function sendMessage(
  userId: string,
  message: string,
  conversationId: string | null,
  token: string
): Promise<ChatResponse> {
  const requestBody: ChatRequest = {
    message,
  };

  if (conversationId) {
    requestBody.conversation_id = conversationId;
  }

  const response = await fetch(`/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}

/**
 * List conversations for the authenticated user.
 *
 * Task ID: T222
 *
 * @param userId - Authenticated user ID
 * @param token - JWT authentication token
 * @param limit - Maximum conversations per page (default: 20)
 * @param offset - Number of conversations to skip (default: 0)
 */
export async function listConversations(
  userId: string,
  token: string,
  limit: number = 20,
  offset: number = 0
): Promise<ConversationList> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  const response = await fetch(`/api/${userId}/conversations?${params}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to list conversations');
  }

  return response.json();
}

/**
 * Get conversation detail with all messages.
 *
 * Task ID: T223
 *
 * @param userId - Authenticated user ID
 * @param conversationId - Conversation ID to fetch
 * @param token - JWT authentication token
 */
export async function getConversation(
  userId: string,
  conversationId: string,
  token: string
): Promise<ConversationDetail> {
  const response = await fetch(`/api/${userId}/conversations/${conversationId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to get conversation');
  }

  return response.json();
}
