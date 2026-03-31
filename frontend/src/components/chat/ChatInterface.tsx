"use client";

import { useState, useRef, useEffect, forwardRef, KeyboardEvent } from "react";
import { chatApi, ChatMessage } from "@/lib/chat-api";
import { Send, User, Bot, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";

// Assuming we want a beautiful scrollable container
export function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isFetchingHistory, setIsFetchingHistory] = useState(true);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to latest message
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading, isFetchingHistory]);

  // Fetch history on mount
  useEffect(() => {
    async function loadHistory() {
      console.log("ChatInterface: Starting history fetch...");
      try {
        const history = await chatApi.getHistory();
        console.log("ChatInterface: History fetched successfully:", history);
        if (history.conversation_id) {
          setConversationId(history.conversation_id);
          setMessages(history.messages);
        } else {
          console.log("ChatInterface: No previous conversation found.");
        }
      } catch (error) {
        console.error("ChatInterface: Failed to load chat history:", error);
      } finally {
        console.log("ChatInterface: Setting isFetchingHistory to false.");
        setIsFetchingHistory(false);
      }
    }
    loadHistory();
  }, []);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const result = await chatApi.sendMessage(userMessage, conversationId);
      setMessages((prev) => [...prev, { role: "assistant", content: result.response }]);
      setConversationId(result.conversation_id);
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I encountered an error communicating with the server." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-background rounded-lg border shadow-sm mx-auto max-w-4xl overflow-hidden mt-4 mb-8" style={{ height: "calc(100vh - 100px)" }}>
      {/* Header */}
      <div className="p-4 border-b bg-card">
        <h2 className="text-lg font-semibold flex items-center gap-2">
          <Bot className="w-5 h-5 text-primary" />
          Todo Assistant
        </h2>
        <p className="text-sm text-muted-foreground">Manage your tasks via natural language</p>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {isFetchingHistory ? (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50 space-y-4">
            <Loader2 className="w-8 h-8 animate-spin" />
            <p>Loading history...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground opacity-50 space-y-4">
            <Bot className="w-16 h-16" />
            <p className="max-w-md text-center">Hello! I'm your AI Todo assistant. Ask me to add a task, show your pending items, or mark something as complete.</p>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} className={`flex gap-3 ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              {m.role === "assistant" && (
                <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                  <Bot className="w-5 h-5 text-primary" />
                </div>
              )}
              
              <div 
                className={`px-4 py-3 rounded-2xl max-w-[80%] whitespace-pre-wrap ${
                  m.role === "user" 
                    ? "bg-primary text-primary-foreground rounded-br-sm" 
                    : "bg-muted text-foreground rounded-bl-sm border"
                }`}
              >
                {m.content}
              </div>

              {m.role === "user" && (
                <div className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center shrink-0">
                  <User className="w-5 h-5 text-secondary-foreground" />
                </div>
              )}
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex gap-3 justify-start">
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
              <Bot className="w-5 h-5 text-primary" />
            </div>
            <div className="px-5 py-4 rounded-2xl bg-muted rounded-bl-sm border flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
              <span className="text-sm text-muted-foreground">Thinking...</span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-card border-t">
        <div className="relative flex items-end gap-2 max-w-4xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask me to create a task..."
            className="w-full min-h-[56px] max-h-32 resize-none bg-background rounded-xl border p-4 pr-12 focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm shadow-sm"
            rows={1}
            disabled={isLoading}
          />
          <Button 
            size="icon" 
            className="absolute right-2 bottom-2 rounded-lg" 
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
        <p className="text-xs text-center text-muted-foreground mt-2">
          AI agents can make mistakes. Always verify your task changes.
        </p>
      </div>
    </div>
  );
}
