/**
 * Proxy route for ChatKit: forwards requests from the same-origin ChatKit iframe
 * to the FastAPI backend, avoiding cross-origin CORS issues entirely.
 */
import { NextRequest } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export async function POST(req: NextRequest): Promise<Response> {
  // Read body as text to avoid ReadableStream consumption issues
  const body = await req.text();

  const backendResponse = await fetch(`${BACKEND_URL}/chatkit`, {
    method: "POST",
    headers: {
      "Content-Type": req.headers.get("Content-Type") ?? "application/json",
      ...(req.headers.get("Authorization")
        ? { Authorization: req.headers.get("Authorization")! }
        : {}),
    },
    body,
  });

  const contentType = backendResponse.headers.get("Content-Type") ?? "application/json";

  // For SSE streaming responses, pipe through a TransformStream to avoid buffering
  if (contentType.includes("text/event-stream") && backendResponse.body) {
    const { readable, writable } = new TransformStream();
    backendResponse.body.pipeTo(writable);
    return new Response(readable, {
      status: backendResponse.status,
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
        Connection: "keep-alive",
      },
    });
  }

  // Non-streaming (JSON) responses
  return new Response(backendResponse.body, {
    status: backendResponse.status,
    headers: {
      "Content-Type": contentType,
      "Cache-Control": "no-cache",
    },
  });
}
