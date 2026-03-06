// Task: T013 | Spec: specs/007-chatkit-ui-integration/spec.md
"use client";

import Script from "next/script";
import { useEffect, useRef } from "react";
import { getJwtToken } from "@/lib/auth-client";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const CHATKIT_CDN = "https://cdn.platform.openai.com/deployments/chatkit/chatkit.js";

export default function ChatPage(): React.JSX.Element {
  const chatRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    // Once the web component is defined, set its options
    const setupOptions = (): void => {
      const el = chatRef.current as HTMLElement & { setOptions?: (opts: unknown) => void };
      if (!el || typeof el.setOptions !== "function") return;
      el.setOptions({
        api: {
          url: `/api/chatkit`,
          domainKey: "",
          fetch: async (url: string, init?: RequestInit): Promise<Response> => {
            const token = getJwtToken();
            return fetch(url, {
              ...init,
              headers: {
                ...(init?.headers as Record<string, string> | undefined),
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
              },
            });
          },
        },
        theme: { colorScheme: "dark" },
      });
    };

    // Try immediately (component may already be defined from a prior navigation)
    if (customElements.get("openai-chatkit")) {
      setupOptions();
    } else {
      // Wait for the element to be defined after the script loads
      customElements.whenDefined("openai-chatkit").then(setupOptions);
    }
  }, []);

  return (
    <div className="flex flex-col h-full min-h-[calc(100vh-4rem)]">
      <Script src={CHATKIT_CDN} strategy="afterInteractive" />
      {/* @ts-expect-error openai-chatkit is a custom element (types from @openai/chatkit) */}
      <openai-chatkit
        ref={chatRef}
        style={{ height: "100%", display: "block", flex: "1" }}
      />
    </div>
  );
}
