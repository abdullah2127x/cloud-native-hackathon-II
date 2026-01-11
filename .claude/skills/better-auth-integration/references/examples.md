# Better Auth Integration - Additional Examples

## Complete Example: Full Stack Authentication Setup

### Backend Setup (FastAPI + Better Auth)

#### Project Structure
```
backend/
├── main.py                 # FastAPI app
├── auth/
│   ├── __init__.py
│   ├── jwt.py             # JWT utilities
│   └── middleware.py      # Auth middleware
├── api/
│   ├── __init__.py
│   ├── auth.py            # Auth routes
│   └── protected.py       # Protected routes
├── models/
│   ├── __init__.py
│   └── user.py            # User models
└── config/
    ├── __init__.py
    └── settings.py         # Configuration
```

#### Main FastAPI Application
```python
# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from auth.jwt import get_current_user
from api.auth import router as auth_router
from api.protected import router as protected_router
from config.settings import settings
import uvicorn

app = FastAPI(title="My API with Better Auth")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(protected_router)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/me")
async def get_profile(request: Request):
    """Get current user profile"""
    try:
        user = await get_current_user(request)
        return {
            "user": {
                "id": user["user_id"],
                "email": user["email"],
                "name": user["name"]
            }
        }
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"error": e.detail}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### Authentication API Routes
```python
# api/auth.py
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any
import httpx

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/verify-token")
async def verify_auth_token(request: Request) -> Dict[str, Any]:
    """
    Verify if the provided auth token is valid
    This connects with Better Auth to verify the session
    """
    try:
        # Forward the request to Better Auth verification endpoint
        # This is a simplified example - in practice, you'd integrate with Better Auth's session system
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="No valid authorization header")

        token = auth_header.split(" ")[1]

        # In a real implementation, you'd verify this token against Better Auth's session store
        # For now, we'll simulate the verification
        # This would typically be done via a call to your Next.js auth API

        # Simulate verification
        import os
        from jose import jwt

        try:
            payload = jwt.decode(token, os.getenv("BETTER_AUTH_SECRET"), algorithms=["HS256"])

            return {
                "valid": True,
                "user": {
                    "id": payload.get("id"),
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token verification failed: {str(e)}")

@router.get("/session")
async def get_session(request: Request) -> Dict[str, Any]:
    """
    Get session information from Better Auth
    """
    try:
        # This would typically be handled by Better Auth's client-side session management
        # Here we simulate checking for a session token in cookies
        session_token = request.cookies.get("better-auth.session_token")

        if not session_token:
            raise HTTPException(status_code=401, detail="No active session")

        # Verify the session token
        import os
        from jose import jwt

        try:
            payload = jwt.decode(session_token, os.getenv("BETTER_AUTH_SECRET"), algorithms=["HS256"])

            return {
                "authenticated": True,
                "user": {
                    "id": payload.get("id"),
                    "email": payload.get("email"),
                    "name": payload.get("name")
                }
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid session")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session check failed: {str(e)}")
```

#### Protected API Routes
```python
# api/protected.py
from fastapi import APIRouter, Request, Depends
from typing import Dict, Any
from auth.jwt import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/data")
async def get_protected_data(request: Request, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Example of a protected endpoint that requires authentication
    """
    return {
        "message": "This is protected data",
        "user": {
            "id": current_user["user_id"],
            "email": current_user["email"],
            "name": current_user["name"]
        },
        "data": [
            {"id": 1, "title": "Protected Item 1", "content": "This content is only visible to authenticated users"},
            {"id": 2, "title": "Protected Item 2", "content": "More protected content"}
        ]
    }

@router.post("/create-item")
async def create_protected_item(
    request: Request,
    item_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create an item that belongs to the authenticated user
    """
    # In a real implementation, you would save this to a database
    # associated with the current user

    new_item = {
        "id": len([]) + 1,  # This would come from DB
        "user_id": current_user["user_id"],
        "data": item_data,
        "created_at": "2024-01-01T00:00:00Z"  # This would be generated
    }

    return {
        "message": "Item created successfully",
        "item": new_item
    }

@router.get("/user-info")
async def get_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get detailed information about the authenticated user
    """
    return {
        "user": {
            "id": current_user["user_id"],
            "email": current_user["email"],
            "name": current_user["name"],
            "role": current_user.get("role", "user"),
            "permissions": current_user.get("permissions", [])
        }
    }
```

## Frontend Setup (Next.js + Better Auth)

### Project Structure
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   │   └── page.tsx
│   ├── signup/
│   │   └── page.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   └── api/
│       └── auth/
│           └── [...auth]/
│               └── route.ts
├── lib/
│   └── auth.ts
├── components/
│   ├── auth/
│   │   ├── sign-in-form.tsx
│   │   ├── sign-up-form.tsx
│   │   └── session-provider.tsx
│   └── ui/
│       └── ...
└── middleware.ts
```

### Better Auth Client Setup
```typescript
// lib/auth.ts
import { createAuthClient } from "@better-auth/react";

export const {
  useSession,
  signIn,
  signOut,
  signUp,
  getClientSession,
} = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  // Add any additional client configuration here
});

// Export utility functions for session management
export const checkAuthStatus = async () => {
  try {
    const session = await getClientSession();
    return { isAuthenticated: !!session, user: session?.user };
  } catch (error) {
    console.error("Error checking auth status:", error);
    return { isAuthenticated: false, user: null };
  }
};
```

### Next.js API Routes for Better Auth
```typescript
// app/api/auth/[...auth]/route.ts
import { initBetterAuth } from "better-auth";
import { nextJs } from "better-auth/next-js";
import { drizzleAdapter } from "@better-auth/dizzle-adapter"; // if using Drizzle
import { Pool } from "@neondatabase/serverless";

// Initialize Better Auth
export const {
  GET,
  POST,
  auth: serverAuth,
  signIn: serverSignIn,
  signOut: serverSignOut
} = initBetterAuth(
  nextJs({
    auth: {
      secret: process.env.BETTER_AUTH_SECRET!,
      trustHost: true,
      database: {
        provider: "postgresql",
        url: process.env.DATABASE_URL!,
      },
      emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
      },
      socialProviders: {
        // Add social providers if needed
      },
    },
    session: {
      expiresIn: 7 * 24 * 60 * 60, // 7 days
      updateAge: 24 * 60 * 60, // 24 hours
    },
  })
);

// Export the server auth instance for use in other parts of the app
export { serverAuth };
```

### Login Page Component
```typescript
// app/login/page.tsx
"use client";

import { useState } from "react";
import { signIn } from "@/lib/auth";
import { useRouter, useSearchParams } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await signIn.email({
        email,
        password,
        callbackURL: callbackUrl,
      });

      if (result.error) {
        setError(result.error.message);
      } else {
        // Successful login - user is redirected automatically
        router.push(callbackUrl);
      }
    } catch (err) {
      setError("An error occurred during sign in");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl">Sign in to your account</CardTitle>
          <CardDescription>
            Enter your email and password to access your account
          </CardDescription>
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
          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? "Signing In..." : "Sign In"}
            </Button>
            <p className="text-sm text-muted-foreground">
              Don't have an account?{" "}
              <a href="/signup" className="text-primary hover:underline">
                Sign up
              </a>
            </p>
            <p className="text-sm text-muted-foreground">
              <a href="/forgot-password" className="text-primary hover:underline">
                Forgot your password?
              </a>
            </p>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
```

### Protected Dashboard Page
```typescript
// app/dashboard/page.tsx
import { serverAuth } from "../api/auth/[...auth]/route";
import { redirect } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { signOut } from "@/lib/auth";

export default async function DashboardPage() {
  const session = await serverAuth.getSession();

  if (!session) {
    redirect("/login?callbackUrl=/dashboard");
  }

  const handleLogout = async () => {
    "use server";
    await serverAuth.signOut();
    redirect("/login");
  };

  return (
    <div className="container py-8">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Dashboard</CardTitle>
          <form action={handleLogout}>
            <Button type="submit" variant="outline">Sign Out</Button>
          </form>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">Welcome, {session.user.name}!</h2>
            <p>Email: {session.user.email}</p>
            <p>User ID: {session.user.id}</p>

            <div className="mt-6">
              <h3 className="font-medium mb-2">Protected Content</h3>
              <p>This content is only visible to authenticated users.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Client-side session usage */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Client Session Info</CardTitle>
        </CardHeader>
        <CardContent>
          <ClientSessionInfo />
        </CardContent>
      </Card>
    </div>
  );
}

// Client component to show session info
import { useSession } from "@/lib/auth";

function ClientSessionInfo() {
  const { data: session, isLoading } = useSession();

  if (isLoading) {
    return <p>Loading session...</p>;
  }

  if (!session) {
    return <p>No active session</p>;
  }

  return (
    <div>
      <p>Client session loaded:</p>
      <p>Name: {session.user.name}</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

### Next.js Middleware for Route Protection
```typescript
// middleware.ts
import { serverAuth } from "./app/api/auth/[...auth]/route";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  // Get session from request
  const session = await serverAuth.getSession({
    headers: request.headers,
  });

  // Define protected paths
  const protectedPaths = [
    "/dashboard",
    "/profile",
    "/api/protected",
    "/admin", // Add admin routes if needed
  ];

  const isProtected = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Public paths that don't require authentication
  const publicPaths = [
    "/login",
    "/signup",
    "/api/auth",
    "/api/trpc", // If using tRPC
  ];

  const isPublic = publicPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // If it's a protected path and user is not authenticated
  if (isProtected && !session) {
    // Redirect to login with callback URL
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("callbackUrl", request.nextUrl.toString());
    return NextResponse.redirect(loginUrl);
  }

  // If user is logged in and trying to access login/signup, redirect to dashboard
  if ((request.nextUrl.pathname === "/login" || request.nextUrl.pathname === "/signup") && session) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes except auth)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - manifest.json (app manifest file)
     */
    "/((?!api/auth|_next/static|_next/image|favicon.ico|manifest.json).*)",
  ],
};
```

## Advanced Authentication Patterns

### Role-Based Access Control (RBAC)
```typescript
// lib/auth/rbac.ts
import { serverAuth } from "@/app/api/auth/[...auth]/route";
import { NextRequest } from "next/server";

export type UserRole = "admin" | "moderator" | "user" | "guest";

export interface UserWithRole {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  permissions: string[];
}

export async function getUserWithRole(request: NextRequest): Promise<UserWithRole | null> {
  const session = await serverAuth.getSession({
    headers: request.headers,
  });

  if (!session) {
    return null;
  }

  // In a real implementation, you would fetch the user's role from your database
  // Here we're simulating it based on email
  const email = session.user.email;
  let role: UserRole = "user";
  let permissions: string[] = ["read:own", "update:own"];

  if (email.endsWith("@admin.com")) {
    role = "admin";
    permissions = ["read:*", "create:*", "update:*", "delete:*"];
  } else if (email.endsWith("@mod.com")) {
    role = "moderator";
    permissions = ["read:*", "update:others", "moderate:*"];
  }

  return {
    id: session.user.id,
    email: session.user.email,
    name: session.user.name,
    role,
    permissions,
  };
}

export async function checkPermission(
  request: NextRequest,
  requiredPermission: string
): Promise<boolean> {
  const user = await getUserWithRole(request);

  if (!user) {
    return false;
  }

  return user.permissions.includes(requiredPermission);
}

// Middleware for role-based access
export async function requireRole(
  request: NextRequest,
  requiredRole: UserRole
): Promise<UserWithRole | null> {
  const user = await getUserWithRole(request);

  if (!user) {
    return null;
  }

  // Admins can access everything
  if (user.role === "admin") {
    return user;
  }

  // Check if user has required role or higher
  const roleHierarchy: UserRole[] = ["guest", "user", "moderator", "admin"];
  const userRoleIndex = roleHierarchy.indexOf(user.role);
  const requiredRoleIndex = roleHierarchy.indexOf(requiredRole);

  if (userRoleIndex >= requiredRoleIndex) {
    return user;
  }

  return null;
}
```

### Usage in Next.js Route Handler
```typescript
// app/api/admin/users/route.ts
import { NextRequest } from "next/server";
import { requireRole, checkPermission, UserWithRole } from "@/lib/auth/rbac";
import { serverAuth } from "../../auth/[...auth]/route";

export async function GET(request: NextRequest) {
  // Require admin role for this endpoint
  const user = await requireRole(request, "admin");

  if (!user) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), {
      status: 401,
      headers: { "Content-Type": "application/json" },
    });
  }

  // At this point, we know the user is an admin
  // Fetch and return all users
  const allUsers = await fetchAllUsers(); // Your implementation

  return new Response(JSON.stringify({ users: allUsers }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}

async function fetchAllUsers() {
  // Implementation to fetch all users from database
  // This is just a placeholder
  return [
    { id: "1", email: "user@example.com", name: "Regular User", role: "user" },
    { id: "2", email: "admin@example.com", name: "Admin User", role: "admin" },
  ];
}
```

### Custom JWT Claims
```typescript
// app/api/auth/[...auth]/custom-config.ts
import { initBetterAuth } from "better-auth";

export const authWithCustomClaims = initBetterAuth({
  // ... other config
  hooks: {
    sessionCreated: async (session) => {
      // Add custom claims to the session JWT
      const extendedSession = {
        ...session,
        customClaims: {
          role: await getUserRole(session.user.id),
          permissions: await getUserPermissions(session.user.id),
          department: await getUserDepartment(session.user.id),
        },
      };

      return extendedSession;
    },
  },
});

async function getUserRole(userId: string) {
  // Fetch user role from your database
  // This is a placeholder implementation
  return "user";
}

async function getUserPermissions(userId: string) {
  // Fetch user permissions from your database
  // This is a placeholder implementation
  return ["read:own", "update:own"];
}

async function getUserDepartment(userId: string) {
  // Fetch user department from your database
  // This is a placeholder implementation
  return "engineering";
}
```

## Security Best Practices Implementation

### Secure Session Management
```typescript
// lib/auth/security.ts
import { serverAuth } from "@/app/api/auth/[...auth]/route";

export async function invalidateAllUserSessions(userId: string) {
  // In Better Auth, you might need to implement custom session management
  // to invalidate all sessions for a user
  // This is a conceptual example
  console.log(`Invalidating all sessions for user: ${userId}`);

  // In practice, you would:
  // 1. Delete all session records for the user from the database
  // 2. Implement a mechanism to notify all devices about session invalidation
  // 3. Possibly use a session versioning system
}

export async function rotateSessionToken(request: Request) {
  // Better Auth handles token rotation automatically
  // This function would be used if you need custom rotation
  const session = await serverAuth.getSession({
    headers: new Headers(request.headers),
  });

  if (!session) {
    throw new Error("No active session to rotate");
  }

  // Return the current session - Better Auth manages rotation internally
  return session;
}

export async function getSessionSecurityInfo(request: Request) {
  const session = await serverAuth.getSession({
    headers: new Headers(request.headers),
  });

  if (!session) {
    return null;
  }

  return {
    userId: session.user.id,
    sessionId: session.sessionId,
    expiresAt: session.expiresAt,
    userAgent: request.headers.get("user-agent"),
    ip: request.headers.get("x-forwarded-for") || request.headers.get("x-real-ip"),
    createdAt: session.createdAt,
  };
}
```

### Rate Limiting for Auth Endpoints
```typescript
// lib/auth/rate-limit.ts
import { kv } from "@vercel/kv"; // or your preferred key-value store
import { NextRequest } from "next/server";

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetTime: number;
}

export async function checkRateLimit(
  identifier: string, // e.g., IP address or user ID
  windowMs: number = 15 * 60 * 1000, // 15 minutes
  maxRequests: number = 5
): Promise<RateLimitResult> {
  const key = `rate_limit:${identifier}`;
  const windowEndTimestamp = Date.now() + windowMs;

  // Use a sliding window counter
  const result = await kv.multi()
    .get(key)
    .expire(key, Math.ceil(windowMs / 1000))
    .exec();

  const current = result[0]?.[1] || 0;
  const remaining = Math.max(maxRequests - current, 0);

  if (current >= maxRequests) {
    // Rate limit exceeded
    return {
      allowed: false,
      remaining: 0,
      resetTime: Date.now() + windowMs,
    };
  }

  // Increment the counter
  await kv.incr(key);

  return {
    allowed: true,
    remaining: remaining - 1,
    resetTime: Date.now() + windowMs,
  };
}

// Usage in login endpoint
export async function rateLimitedLogin(request: NextRequest) {
  const ip = request.headers.get("x-forwarded-for") || "unknown";
  const rateLimitResult = await checkRateLimit(`${ip}:login`);

  if (!rateLimitResult.allowed) {
    return new Response(
      JSON.stringify({
        error: "Too many login attempts. Please try again later.",
        resetTime: rateLimitResult.resetTime,
      }),
      { status: 429, headers: { "Content-Type": "application/json" } }
    );
  }

  // Proceed with login logic
}
```