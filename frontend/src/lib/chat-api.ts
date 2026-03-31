import { getJwtToken } from "@/lib/auth-client";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

console.log("Chat API initialized with BACKEND_URL:", BACKEND_URL);

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponsePayload {
  conversation_id: string;
  response: string;
  tool_calls: unknown[];
}

export interface ChatHistoryResponsePayload {
  conversation_id: string | null;
  messages: ChatMessage[];
}

export const chatApi = {
  /**
   * Send a chat message to the FastAPI backend.
   * Automatically attaches the Better Auth JWT token.
   */
  async sendMessage(message: string, conversation_id: string | null = null): Promise<ChatResponsePayload> {
    const token = getJwtToken();
    
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({
        message,
        conversation_id,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Chat API error (${response.status}): ${errorText}`);
    }

    return response.json();
  },

  /**
   * Fetch the latest conversation history from the backend.
   */
  async getHistory(): Promise<ChatHistoryResponsePayload> {
    const token = getJwtToken();
    
    const response = await fetch(`${BACKEND_URL}/api/chat/history`, {
      method: "GET",
      headers: {
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Chat History API error (${response.status}): ${errorText}`);
    }

    return response.json();
  }
};
