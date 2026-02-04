---
name: openai-chatkit
description: |
  Integrates OpenAI ChatKit UI library into Next.js applications with proper authentication, event handling, and custom backend configuration.
  This skill should be used when building conversational AI interfaces that need ChatKit component integration, domain allowlist setup, client secret authentication, event monitoring, and client tool handling.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
---

# OpenAI ChatKit Integration Skill

## Overview

This skill provides production-ready patterns for integrating OpenAI ChatKit into Next.js + React + TypeScript applications. It encodes domain expertise from the official ChatKit library documentation and covers component setup, authentication flows, event handling, and custom backend integration.

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Next.js structure, authentication approach (Better Auth), API endpoint patterns |
| **Conversation** | User's specific requirements (ChatKit placement, custom styling, authentication method) |
| **Skill References** | ChatKit patterns from `references/` (API documentation, authentication flows, event handlers, client tools) |
| **User Guidelines** | Project conventions (component structure, TypeScript strictness, error handling patterns) |

Only ask user for THEIR specific requirements. Domain expertise is embedded in this skill's references.

---

## Core Concepts (Embedded Domain Knowledge)

### What is ChatKit?

ChatKit is OpenAI's official framework for building AI-powered chat experiences. It provides:
- Complete UI component (message display, input composer, conversation history)
- Built-in response streaming
- Event system for monitoring chat lifecycle
- Client tool integration for frontend-side actions
- Custom backend support for non-OpenAI APIs
- Production-ready error handling and accessibility

### Authentication Patterns

**Pattern 1: Client Secret (Recommended for Phase 3)**
```
Frontend requests /api/chatkit/start → Backend generates client_secret → ChatKit uses secret for API calls
```
- Secure: Token generated server-side, expires
- Flexible: Backend can refresh tokens
- Backend can verify JWT before issuing secret

**Pattern 2: Direct Client Token**
```
Frontend has clientToken → Pass directly to ChatKit
```
- Simpler setup
- Token embedded in frontend code (less secure)

**Pattern 3: Custom Fetch (Advanced)**
```
ChatKit calls custom fetch function → Inject authorization headers → Call your backend
```
- Full control over requests
- Enables custom APIs (not just OpenAI)
- Used for MCP integration or non-OpenAI backends

### Domain Allowlist Security

OpenAI's platform requires domain registration for security:
- Production deployments MUST register domain
- Provides domain key for ChatKit configuration
- Localhost typically works without registration
- Required at https://platform.openai.com/settings/organization/security/domain-allowlist

### Event System

ChatKit emits events at key lifecycle points:
- `onReady`: Component initialized
- `onError`: Chat or API errors
- `onResponseStart`: AI starts generating
- `onResponseEnd`: AI finishes
- `onThreadChange`: User switches conversation
- `onLog`: Detailed logging for analytics

### Client Tools

Frontend-side tools that AI can invoke:
- AI asks to execute action (e.g., "open a link")
- Frontend receives tool call with parameters
- Frontend executes locally, returns result
- Different from MCP tools (server-side)

---

## Implementation Patterns

### Pattern 1: Basic ChatKit with Client Secret

**When to use**: Authentication required, backend available, Phase 3 chatbot setup

**Components needed**:
1. Next.js route handler: `/api/chatkit/start` and `/api/chatkit/refresh`
2. React component: ChatKit with `useChatKit` hook
3. Environment variable: `OPENAI_DOMAIN_KEY`

**Flow**:
```
1. User loads ChatKit component
2. useChatKit hook calls getClientSecret
3. getClientSecret calls /api/chatkit/start
4. Backend validates JWT from Better Auth
5. Backend calls OpenAI API to get client_secret
6. Frontend receives secret, initializes ChatKit
7. User sends message → ChatKit uses secret for API calls
8. On token expiry, ChatKit calls getClientSecret again
9. This time currentClientSecret exists → calls /api/chatkit/refresh
```

**Security considerations**:
- Backend validates JWT before issuing secret
- Secrets are short-lived (typically 1 hour)
- Domain must be registered in OpenAI platform
- Secrets are returned in response body (HTTPS only in production)

### Pattern 2: Event Handling for Analytics & Error Tracking

**When to use**: Need to monitor user behavior, track errors, measure performance

**Events to capture**:
- `onReady`: Log when ChatKit is ready
- `onError`: Send to error tracking service (Sentry, etc.)
- `onResponseStart`/`onResponseEnd`: Calculate response time
- `onThreadChange`: Track conversation switches
- `onLog`: Custom analytics for tool calls

**Implementation**:
```typescript
onReady: () => {
  analytics.track('chatkit_ready');
},
onError: ({ error }) => {
  errorTracking.captureException(error);
},
onLog: ({ name, data }) => {
  if (name === 'message.send') {
    analytics.track('message_sent', data);
  }
}
```

### Pattern 3: Custom Fetch for MCP/Custom Backend

**When to use**: Not using OpenAI API directly, using custom backend (FastAPI), or MCP integration

**Configuration**:
```typescript
const { control } = useChatKit({
  api: {
    url: '/api/chat',  // Your backend endpoint
    domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
    fetch: async (input, init) => {
      return fetch(input, {
        ...init,
        headers: {
          ...init?.headers,
          'Authorization': `Bearer ${token}`,  // JWT from Better Auth
        },
      });
    },
  },
});
```

**Backend responsibility**:
- Accept requests from ChatKit
- Validate authorization header
- Forward to OpenAI API or process with MCP
- Return ChatKit-compatible responses

### Pattern 4: Client Tool Integration

**When to use**: AI needs to trigger frontend actions (open links, send emails, etc.)

**Define tool types**:
```typescript
type ClientToolCall =
  | { name: 'open_link'; params: { url: string } }
  | { name: 'send_email'; params: { email: string } }
  | { name: 'update_task'; params: { taskId: number; status: string } };
```

**Handle in ChatKit**:
```typescript
const { control } = useChatKit({
  api: { ... },
  onClientTool: async (toolCall) => {
    const { name, params } = toolCall as ClientToolCall;
    switch (name) {
      case 'open_link':
        window.open(params.url, '_blank');
        return { opened: true };
      case 'send_email':
        await sendEmail(params.email);
        return { sent: true };
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  },
});
```

---

## Decision Tree: Which Pattern?

```
Do you need OpenAI's API directly?
├─ YES, with authentication → Pattern 1 (Client Secret)
├─ NO, using custom backend → Pattern 3 (Custom Fetch)
└─ Don't know yet → Start with Pattern 1

Do you need analytics/error tracking?
├─ YES → Add Pattern 2 (Event Handling)
└─ NO → Skip for now

Do you need frontend-side actions?
├─ YES → Add Pattern 4 (Client Tools)
└─ NO → Skip for now
```

---

## Anti-Patterns to Avoid

❌ **Hardcoding tokens in frontend code**
- ✅ Use backend to issue short-lived secrets

❌ **Ignoring domain allowlist**
- ✅ Register domain in OpenAI platform before production

❌ **No error handling**
- ✅ Implement `onError` handler for graceful degradation

❌ **Storing conversation state in memory**
- ✅ Store in database (ChatKit manages thread history, but persist conversations)

❌ **Forgetting to pass JWT token to custom fetch**
- ✅ Always inject authorization header in custom fetch function

❌ **Client tools that block indefinitely**
- ✅ Implement timeouts, handle errors gracefully

---

## Best Practices

✅ **Always use custom fetch for JWT injection** - Pass Bearer token from Better Auth
✅ **Implement event handlers early** - Enables monitoring and debugging
✅ **Validate domain allowlist before production** - Required for hosted ChatKit
✅ **Handle token refresh gracefully** - ChatKit will call getClientSecret on expiry
✅ **Separate concerns** - ChatKit component in separate file, event handlers in hook
✅ **Type client tools** - Prevents runtime errors from unexpected tool calls
✅ **Test with network throttling** - Response streaming should work on slow connections
✅ **Use environment variables** - Domain key, API URLs, feature flags

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "Domain not allowed" | Domain not registered in allowlist | Register at https://platform.openai.com/settings/organization/security/domain-allowlist |
| Token refresh loop | Client secret always expired | Ensure backend issues long-lived secrets (typically 1 hour) |
| No messages appear | Custom fetch not injecting token | Verify Authorization header in fetch function |
| Slow initial load | Waiting for client secret | Move getClientSecret call to useEffect to non-block |
| Client tool not called | Tool type mismatch | Ensure `onClientTool` handles all tool types AI can invoke |

---

## Files Generated by This Skill

When implementing ChatKit integration, you'll create:

### Route Handlers (Backend)
- `/api/chatkit/start` - Generate initial client secret (POST)
- `/api/chatkit/refresh` - Refresh expired client secret (POST)
- Optional: `/api/chat` - Custom backend if not using OpenAI API

### React Components
- `ChatKitWrapper` or `ChatInterface` - Main ChatKit component
- `useChat` or custom hook - Manage chat state and events
- Optional: `ClientToolHandler` - Handle tool invocations

### Environment Variables
- `NEXT_PUBLIC_CHATKIT_DOMAIN_KEY` - ChatKit domain key from OpenAI
- `OPENAI_API_KEY` or `OPENAI_API_BASE_URL` - API configuration

---

## References

- **Official ChatKit Docs**: https://github.com/openai/chatkit-js
- **Domain Allowlist**: https://platform.openai.com/settings/organization/security/domain-allowlist
- **Authentication Patterns**: See `references/authentication-flows.md`
- **Event Handlers**: See `references/event-handling-patterns.md`
- **Client Tools**: See `references/client-tools.md`
- **Custom Backend**: See `references/custom-backend-integration.md`
- **Code Examples**: See `references/code-examples.md`

---

## When to Use This Skill

- Implementing conversational AI UI in Next.js
- Setting up OpenAI ChatKit with custom backend
- Integrating chat with existing authentication system (Better Auth)
- Adding analytics and error tracking to chat
- Implementing frontend-side tool actions
- Handling token management and domain configuration

## When NOT to Use This Skill

- Building chat without UI (API-only)
- Using third-party chat SDKs (not OpenAI ChatKit)
- Chat implementation in non-React/Next.js projects
- Minimal chat without authentication (simple iframe)
