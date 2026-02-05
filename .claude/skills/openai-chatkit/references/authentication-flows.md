# ChatKit Authentication Flows

## Flow 1: Client Secret (Backend-Issued)

**Best for**: Secure applications with authentication, ability to call backend

```typescript
// Frontend: React Component
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function ChatInterface() {
  const { control } = useChatKit({
    api: {
      async getClientSecret(currentClientSecret) {
        // Initial request - no secret yet
        if (!currentClientSecret) {
          const res = await fetch('/api/chatkit/start', { method: 'POST' });
          return (await res.json()).client_secret;
        }

        // Token refresh - secret expired
        const res = await fetch('/api/chatkit/refresh', {
          method: 'POST',
          body: JSON.stringify({ currentClientSecret }),
          headers: { 'Content-Type': 'application/json' },
        });
        return (await res.json()).client_secret;
      },
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[400px]" />;
}
```

```python
# Backend: FastAPI Route Handler
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
import os
import httpx

router = APIRouter()

async def get_current_user(request: Request):
    """Extract user from JWT token in request"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Unauthorized')

    token = auth_header[7:]  # Remove "Bearer " prefix
    # Validate token with Better Auth...
    return user

@router.post('/api/chatkit/start')
async def chatkit_start(request: Request, user = Depends(get_current_user)):
    """Generate initial client secret"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.openai.com/v1/chat.completions',  # OpenAI API endpoint for secrets
            headers={
                'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'gpt-4',
                'messages': [{'role': 'user', 'content': 'Generate secret'}],
            }
        )

    # Extract client_secret from response (exact format per OpenAI docs)
    client_secret = response.json()['client_secret']

    return JSONResponse({
        'client_secret': client_secret,
        'expires_in': 3600  # 1 hour
    })

@router.post('/api/chatkit/refresh')
async def chatkit_refresh(
    request: Request,
    body: dict,
    user = Depends(get_current_user)
):
    """Refresh expired client secret"""
    current_secret = body.get('currentClientSecret')

    # Validate current secret belongs to user...

    # Generate new secret
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/refresh',
            headers={
                'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                'Content-Type': 'application/json',
            },
            json={'current_secret': current_secret},
        )

    return JSONResponse({
        'client_secret': response.json()['client_secret'],
        'expires_in': 3600
    })
```

**Security Model**:
- Backend validates JWT before issuing secret
- Secret is short-lived (typically 1 hour)
- Only authenticated users get secrets
- Refresh endpoint can implement additional validation

**When to use**:
- ✅ Secure applications with authentication
- ✅ Backend available to call
- ✅ Need per-user conversation isolation
- ✅ Phase 3 chatbot with Better Auth

---

## Flow 2: Direct Client Token

**Best for**: Simple setups, public chats, development

```typescript
// Frontend: React Component
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function ChatInterface({ clientToken }: { clientToken: string }) {
  const { control } = useChatKit({
    api: { clientToken }  // Token passed as prop
  });

  return <ChatKit control={control} className="h-[600px] w-[400px]" />;
}

// Usage: Pass token from environment
export default function Page() {
  return (
    <ChatInterface
      clientToken={process.env.NEXT_PUBLIC_OPENAI_CHATKIT_TOKEN}
    />
  );
}
```

**Security Model**:
- Token visible in frontend code/environment variables
- No per-request validation
- Token should be public (ChatKit tokens are designed for public use)

**When to use**:
- ✅ Public chats (no authentication needed)
- ✅ Development/testing
- ✅ Simple MVP
- ❌ NOT for Phase 3 (requires authentication)

---

## Flow 3: Custom Fetch with JWT Injection

**Best for**: Custom backend, non-OpenAI API, MCP integration

```typescript
// Frontend: React Component
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useAuth } from '@/lib/auth';  // Better Auth hook

export function ChatInterface() {
  const { user } = useAuth();

  const { control } = useChatKit({
    api: {
      url: '/api/chat',  // Your custom endpoint
      domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
      fetch: async (input: string, init?: RequestInit) => {
        // Get JWT token from Better Auth
        const token = await getAuthToken();

        return fetch(input, {
          ...init,
          headers: {
            ...init?.headers,
            'Authorization': `Bearer ${token}`,
            'X-User-Id': user.id,  // Optional: Pass user ID
          },
          credentials: 'include',  // Include cookies if needed
        });
      },
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[400px]" />;
}
```

```python
# Backend: FastAPI Custom Chat Endpoint
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

router = APIRouter()

async def verify_token(request: Request):
    """Verify JWT token from Authorization header"""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Unauthorized')

    token = auth_header[7:]
    # Validate with Better Auth secret...
    return decoded_token

@router.post('/api/chat')
async def chat(request: Request, user = Depends(verify_token)):
    """Custom chat endpoint for ChatKit"""
    body = await request.json()

    # Extract messages from ChatKit request
    messages = body.get('messages', [])

    # Your custom logic:
    # - Use MCP tools
    # - Query database
    # - Call custom AI model
    # - Process with business logic

    # Example: Call OpenAI via MCP or direct API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'gpt-4',
                'messages': messages,
                'stream': True,
            },
            stream=True,
        )

    # Return streaming response compatible with ChatKit
    async def generate():
        async for line in response.aiter_lines():
            if line.startswith('data: '):
                yield line + '\n'

    return StreamingResponse(generate(), media_type='text/event-stream')
```

**Security Model**:
- JWT token validated on every request
- Backend can implement custom authorization
- Endpoint can call any backend service
- Full control over request/response

**When to use**:
- ✅ Custom backend (FastAPI, Express, etc.)
- ✅ MCP tool integration (Phase 3)
- ✅ Custom AI logic or database queries
- ✅ Non-OpenAI APIs
- ✅ Phase 3 chatbot with MCP

---

## Comparison Table

| Aspect | Client Secret | Direct Token | Custom Fetch |
|--------|---|---|---|
| **Security** | High (backend validates) | Low (public token) | Highest (full control) |
| **Complexity** | Medium (2 endpoints) | Low (1 endpoint) | High (custom backend) |
| **Best For** | OpenAI API directly | Public/demo | Custom backend/MCP |
| **Per-user isolation** | Yes | No | Yes |
| **Token refresh** | Automatic | Manual | Automatic |
| **Phase 3 fit** | ✅ Good | ❌ No | ✅✅ Best |

---

## Domain Allowlist

All ChatKit setups require domain registration for production:

1. Go to: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Click "Add domain"
3. Enter your frontend domain: `https://yourdomain.com` (no trailing slash)
4. Receive `domainKey` from OpenAI
5. Add to ChatKit configuration:

```typescript
const { control } = useChatKit({
  api: {
    domainKey: process.env.NEXT_PUBLIC_CHATKIT_DOMAIN_KEY,
    // ... other config
  },
});
```

**Notes**:
- Localhost (http://localhost:3000) usually works without allowlist
- Production deployments (Vercel) MUST be registered
- Each domain needs separate allowlist entry
- Subdomains must be added separately
- Domain key is environment-specific

---

## Environment Variables

```bash
# For Client Secret flow
OPENAI_API_KEY=sk-...  # Backend only

# For Direct Token flow
NEXT_PUBLIC_OPENAI_CHATKIT_TOKEN=pk_...  # Public

# For Custom Fetch flow
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=dk_...  # Public
OPENAI_API_KEY=sk-...  # Backend (if calling OpenAI)

# Phase 3 Setup (Custom Fetch)
NEXT_PUBLIC_CHATKIT_DOMAIN_KEY=dk_...
NEXT_PUBLIC_API_URL=http://localhost:8000  # FastAPI backend
```

