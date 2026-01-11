---
name: better-auth-integration
description: |
  This skill should be used when implementing authentication, user sessions, JWT tokens, or protected routes.
  Use for signup/signin flows and auth verification with Better Auth.
---

# Better Auth Integration Skill

Auto-invoke when implementing authentication, user sessions, JWT tokens, or protected routes. Use for signup/signin flows and auth verification.

## Better Auth Setup in Next.js (lib/auth.ts)

Setting up Better Auth client for Next.js applications:

### Client Setup (lib/auth.ts)
```typescript
import { createAuthClient } from "@better-auth/react";

export const {
  useSession,
  signIn,
  signOut,
  signUp,
  getClientSession,
} = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  fetch: globalThis.fetch,
  plugins: [
    // Add plugins here if needed
  ]
});
```

### Server-Side Setup (app/api/auth/[...auth]/route.ts)
```typescript
import { initBetterAuth } from "better-auth";
import { nextJs } from "better-auth/next-js";

export const {
  GET,
  POST,
  auth: serverAuth,
  signIn: serverSignIn,
  signOut: serverSignOut
} = initBetterAuth(
  nextJs({
    auth: {
      // Authentication configuration
      secret: process.env.BETTER_AUTH_SECRET!,
      trustHost: true,
      database: {
        provider: "postgresql", // or "mysql", "sqlite"
        url: process.env.DATABASE_URL!,
      },
      emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
      },
      socialProviders: {
        // Add social providers if needed
        // google: {
        //   clientId: process.env.GOOGLE_CLIENT_ID!,
        //   clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        // },
      },
    },
    session: {
      expiresIn: 7 * 24 * 60 * 60, // 7 days
      updateAge: 24 * 60 * 60, // 24 hours
    },
    account: {
      accountLinking: {
        enabled: true,
        trustedProviders: ["google"], // providers that can be linked
      },
    },
  })
);
```

## Email/Password Authentication Config

Configuring email and password authentication with Better Auth:

### Basic Email/Password Setup
```typescript
import { initBetterAuth } from "better-auth";

export const auth = initBetterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true, // Set to true for email verification
    sendVerificationEmail: async (user, url) => {
      // Send verification email using your email service
      console.log(`Verification email sent to ${user.email} with URL: ${url}`);
    },
    password: {
      enabled: true,
      // Minimum password requirements
      minLength: 8,
      requireSpecialChar: false,
      requireNumbers: true,
      requireUppercase: false,
      requireLowercase: false,
    },
  },
});
```

### Advanced Email/Password Configuration
```typescript
export const auth = initBetterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
    sendVerificationEmail: async (user, url) => {
      // Implementation for sending verification email
      await sendEmail({
        to: user.email,
        subject: "Verify your email address",
        html: `<p>Click <a href="${url}">here</a> to verify your email.</p>`,
      });
    },
    sendResetPassword: async (user, url) => {
      // Implementation for sending password reset email
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `<p>Click <a href="${url}">here</a> to reset your password.</p>`,
      });
    },
    password: {
      enabled: true,
      minLength: 12,
      requireSpecialChar: true,
      requireNumbers: true,
      requireUppercase: true,
      requireLowercase: true,
    },
  },
  // Additional validation
  hooks: {
    createUser: {
      before: async (user) => {
        // Validate user data before creation
        if (user.email.includes("temp-email.com")) {
          throw new Error("Temporary emails are not allowed");
        }
        return user;
      },
    },
  },
});
```

## JWT Token Generation and Verification

Better Auth handles JWT tokens automatically, but you can customize the process:

### Custom JWT Claims
```typescript
import { initBetterAuth } from "better-auth";

export const auth = initBetterAuth({
  // ... other config
  jwt: {
    secret: process.env.BETTER_AUTH_SECRET!,
    expiresIn: "7d", // 7 days
  },
  hooks: {
    // Add custom claims to JWT
    sessionCreated: async (session) => {
      // Add custom claims to the session
      return {
        ...session,
        customClaims: {
          role: session.user.role || "user",
          permissions: session.user.permissions || [],
        },
      };
    },
  },
});
```

### Manual JWT Verification (if needed)
```typescript
import { jwtVerify, SignJWT } from "jose";

const JWT_SECRET = new TextEncoder().encode(
  process.env.BETTER_AUTH_SECRET!
);

// Verify JWT token
export async function verifyToken(token: string) {
  try {
    const verified = await jwtVerify(token, JWT_SECRET);
    return verified.payload;
  } catch (error) {
    console.error("Token verification failed:", error);
    return null;
  }
}

// Create custom JWT (not recommended, use Better Auth's built-in tokens)
export async function createToken(payload: any) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("7d")
    .sign(JWT_SECRET);
}
```

## Protected Route Patterns (Middleware)

Implementing protected routes with Better Auth middleware:

### Next.js Middleware (middleware.ts)
```typescript
import { serverAuth } from "./app/api/auth/[...auth]/route";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  // Get session from request
  const session = await serverAuth.getSession({
    headers: request.headers,
  });

  // Define protected routes
  const protectedPaths = [
    "/dashboard",
    "/profile",
    "/api/protected",
    // Add more protected routes as needed
  ];

  const isProtected = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  if (isProtected && !session) {
    // Redirect to login if not authenticated
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", request.url);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
};
```

### API Route Protection
```typescript
// app/api/protected/route.ts
import { serverAuth } from "../auth/[...auth]/route";
import { NextResponse } from "next/server";

export async function GET(request: Request) {
  try {
    // Get session from request
    const session = await serverAuth.getSession({
      headers: new Headers(request.headers),
    });

    if (!session) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    // User is authenticated, return protected data
    return NextResponse.json({
      message: "This is protected data",
      user: {
        id: session.user.id,
        email: session.user.email,
        name: session.user.name,
      },
    });
  } catch (error) {
    console.error("Auth error:", error);
    return NextResponse.json(
      { error: "Authentication failed" },
      { status: 500 }
    );
  }
}
```

### Server Component Protection
```typescript
// app/protected-page/page.tsx
import { serverAuth } from "../api/auth/[...auth]/route";
import { redirect } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function ProtectedPage() {
  const session = await serverAuth.getSession();

  if (!session) {
    redirect("/login?callbackUrl=/protected-page");
  }

  return (
    <div className="container py-8">
      <Card>
        <CardHeader>
          <CardTitle>Protected Content</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Hello {session.user.name}! You are viewing protected content.</p>
          <p>Your email: {session.user.email}</p>
        </CardContent>
      </Card>
    </div>
  );
}
```

## Session Management

Managing user sessions with Better Auth:

### Session Hooks and Management
```typescript
import { initBetterAuth } from "better-auth";

export const auth = initBetterAuth({
  // ... other config
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  hooks: {
    // Called when session is created
    sessionCreated: async (session) => {
      console.log(`Session created for user: ${session.user.id}`);
      // Update last login time in database
      await updateUserLastLogin(session.user.id);
      return session;
    },
    // Called when session is deleted
    sessionDeleted: async (sessionId) => {
      console.log(`Session deleted: ${sessionId}`);
      return sessionId;
    },
  },
});
```

### Session Validation
```typescript
// utils/session-validation.ts
import { serverAuth } from "@/app/api/auth/[...auth]/route";

export async function requireAuth(headers: Headers) {
  const session = await serverAuth.getSession({ headers });

  if (!session) {
    throw new Error("Authentication required");
  }

  return session;
}

export async function getUserFromSession(headers: Headers) {
  const session = await serverAuth.getSession({ headers });

  if (!session) {
    return null;
  }

  return session.user;
}
```

## Frontend Auth Client Usage

Using Better Auth client in frontend components:

### Sign Up Component
```typescript
// components/auth/signup-form.tsx
"use client";

import { useState } from "react";
import { signUp } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export function SignUpForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signUp.email({
        email,
        password,
        name,
      });

      if (result.error) {
        setError(result.error.message);
      } else {
        // Handle successful sign up
        console.log("Sign up successful", result.data);
        // Redirect or show success message
      }
    } catch (err) {
      setError("An error occurred during sign up");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Sign Up</CardTitle>
        <CardDescription>Create a new account</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && <p className="text-red-500 text-sm">{error}</p>}

          <div className="space-y-2">
            <Label htmlFor="name">Full Name</Label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={8}
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Creating Account..." : "Sign Up"}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
```

### Sign In Component
```typescript
// components/auth/signin-form.tsx
"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export function SignInForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signIn.email({
        email,
        password,
        callbackURL: "/dashboard", // Redirect after login
      });

      if (result.error) {
        setError(result.error.message);
      }
    } catch (err) {
      setError("An error occurred during sign in");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Sign In</CardTitle>
        <CardDescription>Sign in to your account</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && <p className="text-red-500 text-sm">{error}</p>}

          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-2">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Signing In..." : "Sign In"}
          </Button>
          <p className="text-sm text-muted-foreground">
            Don't have an account?{" "}
            <a href="/signup" className="text-primary hover:underline">
              Sign up
            </a>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
```

### Session Context Provider
```typescript
// components/auth/session-provider.tsx
"use client";

import { useSession } from "@/lib/auth";
import { ReactNode, createContext, useContext } from "react";

interface SessionContextType {
  session: any;
  isLoading: boolean;
}

const SessionContext = createContext<SessionContextType | undefined>(undefined);

export function SessionProvider({ children }: { children: ReactNode }) {
  const { data: session, isLoading } = useSession();

  return (
    <SessionContext.Provider value={{ session, isLoading }}>
      {children}
    </SessionContext.Provider>
  );
}

export function useSessionContext() {
  const context = useContext(SessionContext);
  if (context === undefined) {
    throw new Error("useSessionContext must be used within a SessionProvider");
  }
  return context;
}

// Usage in layout.tsx
export function AuthenticatedLayout({ children }: { children: ReactNode }) {
  const { session, isLoading } = useSessionContext();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!session) {
    return <div>Please sign in to continue</div>;
  }

  return <>{children}</>;
}
```

## Backend JWT Validation in FastAPI

Validating Better Auth JWT tokens in FastAPI backend:

### JWT Validation Dependency
```python
# auth/jwt.py
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional, Dict, Any
import os
from datetime import datetime

security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify JWT token from Better Auth and return user information
    """
    token = credentials.credentials

    try:
        # Decode the token using Better Auth secret
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )

        # Check if token is expired
        if payload.get("exp") and datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")

        # Return user information from token
        return {
            "user_id": payload.get("id"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "role": payload.get("role", "user")
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")

# Alternative: Extract user from request headers (Better Auth compatible)
async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Extract user information from Better Auth session cookie or header
    """
    # Better Auth typically stores session in cookies
    auth_cookie = request.cookies.get("better-auth.session_token")

    if not auth_cookie:
        # Try authorization header as fallback
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            auth_cookie = auth_header.split(" ")[1]

    if not auth_cookie:
        raise HTTPException(status_code=401, detail="No authentication token provided")

    try:
        payload = jwt.decode(
            auth_cookie,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )

        return {
            "user_id": payload.get("id"),
            "email": payload.get("email"),
            "name": payload.get("name"),
            "role": payload.get("role", "user")
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
```

### Protected Route Example
```python
# api/protected.py
from fastapi import APIRouter, Depends
from typing import Dict, Any
from auth.jwt import get_current_user

router = APIRouter(prefix="/api", tags=["protected"])

@router.get("/protected-data")
async def get_protected_data(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Example of a protected route that requires authentication
    """
    return {
        "message": "This is protected data",
        "user": {
            "id": current_user["user_id"],
            "email": current_user["email"],
            "name": current_user["name"]
        }
    }

@router.post("/create-item")
async def create_item(
    item_data: dict,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Example of creating an item that requires authentication
    """
    # Use current_user to associate the item with the authenticated user
    item = {
        "id": len(items) + 1,  # Simple ID generation
        "data": item_data,
        "user_id": current_user["user_id"],
        "created_at": datetime.utcnow().isoformat()
    }

    # Save to database (implementation depends on your setup)
    # await save_item_to_db(item)

    return {"message": "Item created successfully", "item_id": item["id"]}
```

### Authentication Middleware for FastAPI
```python
# middleware/auth_middleware.py
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt
import os

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Define protected paths
        protected_paths = ["/api/protected", "/api/user", "/api/admin"]

        # Check if the current path requires authentication
        is_protected = any(
            request.url.path.startswith(path) for path in protected_paths
        )

        if is_protected:
            # Extract token from cookies or headers
            token = None
            if "better-auth.session_token" in request.cookies:
                token = request.cookies["better-auth.session_token"]
            elif "authorization" in request.headers:
                auth_header = request.headers["authorization"]
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]

            if not token:
                raise HTTPException(status_code=401, detail="Authentication required")

            try:
                # Verify token
                payload = jwt.decode(
                    token,
                    os.getenv("BETTER_AUTH_SECRET"),
                    algorithms=["HS256"]
                )

                # Add user info to request state
                request.state.user = {
                    "id": payload.get("id"),
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
            except jwt.JWTError:
                raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response
```

## Shared Secret Configuration (BETTER_AUTH_SECRET)

Proper configuration of shared secrets for Better Auth:

### Environment Configuration
```bash
# .env
BETTER_AUTH_SECRET="your-super-secret-jwt-signing-key-here-make-it-long-and-random"
NEXT_PUBLIC_BASE_URL="http://localhost:3000"
DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
```

### Secret Generation
```typescript
// scripts/generate-secret.ts
import { randomBytes } from "crypto";

function generateSecret(length: number = 32): string {
  return randomBytes(length).toString("hex");
}

// Generate a new secret
const newSecret = generateSecret(64); // 64 bytes = 128 hex characters
console.log("New secret:", newSecret);

// For production, you might want to generate it once and store it securely
```

### Configuration Validation
```typescript
// lib/auth/config.ts
import { initBetterAuth } from "better-auth";

// Validate required environment variables
const requiredEnvVars = [
  "BETTER_AUTH_SECRET",
  "DATABASE_URL",
  "NEXT_PUBLIC_BASE_URL"
];

for (const envVar of requiredEnvVars) {
  if (!process.env[envVar]) {
    throw new Error(`Missing required environment variable: ${envVar}`);
  }
}

// Validate secret length
if (process.env.BETTER_AUTH_SECRET!.length < 32) {
  throw new Error("BETTER_AUTH_SECRET should be at least 32 characters long");
}

export const auth = initBetterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  trustHost: true,
  // ... rest of config
});
```

## Token Refresh Patterns

Implementing token refresh mechanisms:

### Client-Side Token Refresh
```typescript
// lib/auth/refresh.ts
import { serverAuth } from "@/app/api/auth/[...auth]/route";

// Better Auth handles token refresh automatically, but you can customize if needed
export async function refreshSessionIfNeeded() {
  try {
    // Better Auth automatically handles refresh, but you can check session status
    const session = await serverAuth.getSession();

    if (!session) {
      // Session is invalid, redirect to login
      window.location.href = "/login";
      return null;
    }

    return session;
  } catch (error) {
    console.error("Error refreshing session:", error);
    // Handle error appropriately
    return null;
  }
}

// For API calls, Better Auth will automatically refresh tokens when needed
// But you can implement custom refresh logic if needed
export async function apiRequest<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...options,
    credentials: "include", // Include cookies for auth
  });

  if (response.status === 401) {
    // Session expired, redirect to login
    window.location.href = "/login";
    throw new Error("Session expired");
  }

  if (!response.ok) {
    throw new Error(`API request failed: ${response.statusText}`);
  }

  return response.json();
}
```

### Server-Side Token Management
```python
# auth/token_manager.py
from datetime import datetime, timedelta
import jwt
import os
from typing import Dict, Any, Optional

class TokenManager:
    def __init__(self):
        self.secret = os.getenv("BETTER_AUTH_SECRET")
        self.algorithm = "HS256"

    def is_token_expired(self, token: str) -> bool:
        """Check if token is expired"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            exp = payload.get("exp")

            if exp:
                return datetime.fromtimestamp(exp) < datetime.utcnow()
            return False
        except jwt.JWTError:
            return True  # If we can't decode, treat as expired

    def refresh_token_if_needed(self, token: str) -> Optional[str]:
        """Refresh token if needed (in Better Auth context)"""
        # In Better Auth, token refresh is handled automatically
        # This is just for demonstration of the concept
        if self.is_token_expired(token):
            return None  # Indicate that re-authentication is needed

        return token

# Usage in FastAPI dependencies
from fastapi import Request

async def get_valid_user(request: Request):
    """Get user with token validation"""
    token = None

    # Try to get token from cookies first
    if "better-auth.session_token" in request.cookies:
        token = request.cookies["better-auth.session_token"]
    elif "authorization" in request.headers:
        auth_header = request.headers["authorization"]
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        raise HTTPException(status_code=401, detail="No authentication token provided")

    # Validate token
    token_manager = TokenManager()

    if token_manager.is_token_expired(token):
        raise HTTPException(status_code=401, detail="Token has expired")

    # Decode and return user info
    try:
        payload = jwt.decode(token, token_manager.secret, algorithms=[token_manager.algorithm])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing auth setup, user models, Next.js configuration, FastAPI structure |
| **Conversation** | User's specific requirements for auth flows, protected routes, token handling |
| **Skill References** | Better Auth patterns from `references/` (setup, validation, security) |
| **User Guidelines** | Project-specific conventions, security requirements, deployment needs |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).