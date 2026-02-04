/**
 * Chat API client functions.
 *
 * Task ID: T129
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
