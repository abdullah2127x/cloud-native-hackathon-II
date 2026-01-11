# Better Auth Integration - Best Practices and Common Patterns

## Security Best Practices

### ✅ DO: Use Strong Secret Keys
```python
# Good: Generate strong secret keys
import secrets

def generate_secret_key():
    # Generate a random 32-byte (256-bit) secret key
    return secrets.token_urlsafe(32)

# In your environment setup
BETTER_AUTH_SECRET = generate_secret_key()  # Or load from secure storage
```

### ❌ AVOID: Weak or Predictable Secrets
```python
# Avoid: Weak secrets
BETTER_AUTH_SECRET = "123456"  # Very weak
BETTER_AUTH_SECRET = "my-secret"  # Too predictable
BETTER_AUTH_SECRET = "password123"  # Common pattern
```

### ✅ DO: Validate Secrets at Startup
```typescript
// Good: Validate secrets at application startup
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

// Validate secret strength
if (process.env.BETTER_AUTH_SECRET!.length < 32) {
  throw new Error("BETTER_AUTH_SECRET should be at least 32 characters long");
}

if (process.env.NODE_ENV === "production" && process.env.BETTER_AUTH_SECRET!.startsWith("dev-")) {
  throw new Error("Do not use development secrets in production");
}
```

## Authentication Flow Best Practices

### ✅ DO: Implement Proper Error Handling
```typescript
// Good: Comprehensive error handling for auth operations
import { signIn, signUp } from "@/lib/auth";

export async function handleSignIn(email: string, password: string) {
  try {
    const result = await signIn.email({
      email,
      password,
      callbackURL: "/dashboard",
    });

    if (result.error) {
      // Handle specific error types
      switch (result.error.code) {
        case "INVALID_CREDENTIALS":
          return { success: false, message: "Invalid email or password" };
        case "EMAIL_NOT_VERIFIED":
          return { success: false, message: "Please verify your email address" };
        default:
          return { success: false, message: result.error.message };
      }
    }

    return { success: true, data: result.data };
  } catch (error) {
    console.error("Sign in error:", error);
    return { success: false, message: "An unexpected error occurred" };
  }
}

export async function handleSignUp(email: string, password: string, name: string) {
  try {
    const result = await signUp.email({
      email,
      password,
      name,
    });

    if (result.error) {
      // Handle specific error types
      switch (result.error.code) {
        case "EMAIL_USED":
          return { success: false, message: "Email already registered" };
        case "WEAK_PASSWORD":
          return { success: false, message: "Password is too weak" };
        default:
          return { success: false, message: result.error.message };
      }
    }

    return { success: true, data: result.data };
  } catch (error) {
    console.error("Sign up error:", error);
    return { success: false, message: "An unexpected error occurred" };
  }
}
```

### ✅ DO: Validate User Input
```typescript
// Good: Input validation before auth operations
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function validatePassword(password: string): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Password must be at least 8 characters long");
  }

  if (!/[A-Z]/.test(password)) {
    errors.push("Password must contain at least one uppercase letter");
  }

  if (!/[a-z]/.test(password)) {
    errors.push("Password must contain at least one lowercase letter");
  }

  if (!/\d/.test(password)) {
    errors.push("Password must contain at least one number");
  }

  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    errors.push("Password must contain at least one special character");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

// Usage in form handlers
export async function handleSignUpWithValidation(email: string, password: string, name: string) {
  // Validate inputs first
  if (!validateEmail(email)) {
    return { success: false, message: "Please enter a valid email address" };
  }

  const passwordValidation = validatePassword(password);
  if (!passwordValidation.isValid) {
    return { success: false, message: passwordValidation.errors.join(", ") };
  }

  if (!name.trim()) {
    return { success: false, message: "Name is required" };
  }

  // Proceed with sign up
  return await handleSignUp(email, password, name);
}
```

## Session Management Best Practices

### ✅ DO: Implement Proper Session Timeout
```typescript
// Good: Configurable session settings
export const authConfig = {
  session: {
    expiresIn: process.env.NODE_ENV === "production"
      ? 7 * 24 * 60 * 60 // 7 days in production
      : 24 * 60 * 60,    // 1 day in development
    updateAge: 24 * 60 * 60, // Update session every 24 hours
  },
  // Other auth config...
};
```

### ✅ DO: Secure Session Storage
```typescript
// Good: Secure session configuration
import { initBetterAuth } from "better-auth";

export const auth = initBetterAuth({
  // ... other config
  session: {
    cookie: {
      // Use secure cookies in production
      secure: process.env.NODE_ENV === "production",
      // Prevent XSS attacks
      httpOnly: true,
      // Prevent CSRF attacks
      sameSite: "lax" as const,
      // Set appropriate max age
      maxAge: 7 * 24 * 60 * 60, // 7 days
    },
  },
});
```

## JWT Token Best Practices

### ✅ DO: Implement Token Rotation
```python
# Good: Token rotation in FastAPI
from datetime import datetime, timedelta
import jwt
import os
from fastapi import Request

class TokenManager:
    def __init__(self):
        self.secret = os.getenv("BETTER_AUTH_SECRET")
        self.algorithm = "HS256"
        self.access_token_expire = timedelta(minutes=15)  # 15 minutes
        self.refresh_token_expire = timedelta(days=7)     # 7 days

    def create_access_token(self, data: dict) -> str:
        """Create short-lived access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + self.access_token_expire
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        """Create long-lived refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + self.refresh_token_expire
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def verify_access_token(self, token: str) -> dict:
        """Verify access token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise jwt.JWTError("Invalid token type")
            return payload
        except jwt.JWTError:
            raise ValueError("Invalid access token")

    def verify_refresh_token(self, token: str) -> dict:
        """Verify refresh token"""
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "refresh":
                raise jwt.JWTError("Invalid token type")
            return payload
        except jwt.JWTError:
            raise ValueError("Invalid refresh token")
```

### ✅ DO: Validate Token Claims
```python
# Good: Token claim validation
def validate_token_claims(payload: dict) -> bool:
    """Validate additional token claims"""
    # Check required claims
    required_claims = ["sub", "exp", "iat", "user_id"]
    for claim in required_claims:
        if claim not in payload:
            return False

    # Check if token is expired
    exp = payload.get("exp")
    if exp and datetime.fromtimestamp(exp) < datetime.utcnow():
        return False

    # Check if token was issued in the future (clock skew)
    iat = payload.get("iat")
    if iat and datetime.fromtimestamp(iat) > datetime.utcnow() + timedelta(minutes=5):
        return False

    return True
```

## Protected Route Best Practices

### ✅ DO: Use Role-Based Access Control
```typescript
// Good: Role-based access control for protected routes
import { serverAuth } from "@/app/api/auth/[...auth]/route";
import { NextRequest } from "next/server";

export type UserRole = "admin" | "moderator" | "user" | "guest";

export async function requireRole(
  request: NextRequest,
  requiredRole: UserRole
): Promise<boolean> {
  const session = await serverAuth.getSession({
    headers: request.headers,
  });

  if (!session) {
    return false;
  }

  // In a real implementation, you would fetch the user's role from your database
  // Here we're simulating it based on email domain
  const email = session.user.email;
  let userRole: UserRole = "user";

  if (email.endsWith("@admin.com")) {
    userRole = "admin";
  } else if (email.endsWith("@mod.com")) {
    userRole = "moderator";
  }

  // Define role hierarchy
  const roleHierarchy: UserRole[] = ["guest", "user", "moderator", "admin"];
  const userRoleIndex = roleHierarchy.indexOf(userRole);
  const requiredRoleIndex = roleHierarchy.indexOf(requiredRole);

  return userRoleIndex >= requiredRoleIndex;
}

// Usage in middleware
export async function adminOnlyMiddleware(request: NextRequest) {
  const hasAccess = await requireRole(request, "admin");

  if (!hasAccess) {
    // Redirect to unauthorized page or return 403
    const url = new URL("/unauthorized", request.url);
    return Response.redirect(url);
  }

  return null; // Continue with the request
}
```

### ✅ DO: Implement Permission-Based Access
```typescript
// Good: Permission-based access control
interface UserPermissions {
  userId: string;
  permissions: string[];
}

export async function hasPermission(
  request: NextRequest,
  requiredPermission: string
): Promise<boolean> {
  const session = await serverAuth.getSession({
    headers: request.headers,
  });

  if (!session) {
    return false;
  }

  // Fetch user permissions from database
  // This is a simplified example
  const userPermissions: UserPermissions = await fetchUserPermissions(session.user.id);

  return userPermissions.permissions.includes(requiredPermission);
}

async function fetchUserPermissions(userId: string): Promise<UserPermissions> {
  // Implementation to fetch user permissions from your database
  // This is a placeholder
  return {
    userId,
    permissions: ["read:own", "update:own", "read:profile"], // Default permissions
  };
}
```

## Error Handling Best Practices

### ✅ DO: Handle Authentication Errors Gracefully
```typescript
// Good: Comprehensive error handling
export async function handleAuthOperation<T>(
  operation: () => Promise<T>,
  operationName: string
): Promise<{ success: boolean; data?: T; error?: string }> {
  try {
    const result = await operation();
    return { success: true, data: result };
  } catch (error: any) {
    console.error(`${operationName} failed:`, error);

    // Handle different types of errors
    if (error.message?.includes("Network Error")) {
      return {
        success: false,
        error: "Network error. Please check your connection and try again."
      };
    }

    if (error.status === 401) {
      return {
        success: false,
        error: "Authentication required. Please sign in."
      };
    }

    if (error.status === 429) {
      return {
        success: false,
        error: "Too many requests. Please try again later."
      };
    }

    return {
      success: false,
      error: "An unexpected error occurred. Please try again."
    };
  }
}

// Usage
export async function safeSignIn(email: string, password: string) {
  return await handleAuthOperation(
    () => signIn.email({ email, password }),
    "Sign in"
  );
}
```

## Common Anti-Patterns to Avoid

### ❌ Anti-pattern: Exposing Sensitive Information
```python
# Avoid: Exposing sensitive information in error messages
@app.post("/api/login")
async def login(request: Request):
    try:
        # ... auth logic
        pass
    except Exception as e:
        # Don't expose internal error details
        return {"error": str(e)}  # Bad: exposes internal details
```

### ✅ Solution: Generic Error Messages
```python
# Good: Generic error messages
@app.post("/api/login")
async def login(request: Request):
    try:
        # ... auth logic
        pass
    except Exception as e:
        # Log the actual error for debugging
        logger.error(f"Login error: {e}")
        # Return generic error message to client
        return {"error": "Authentication failed"}
```

### ❌ Anti-pattern: Storing Secrets in Code
```typescript
// Avoid: Hardcoding secrets
export const auth = initBetterAuth({
  secret: "my-secret-key", // Bad: hardcoded secret
  // ... other config
});
```

### ✅ Solution: Use Environment Variables
```typescript
// Good: Use environment variables
export const auth = initBetterAuth({
  secret: process.env.BETTER_AUTH_SECRET!, // Good: from environment
  // ... other config
});
```

### ❌ Anti-pattern: Weak Password Requirements
```typescript
// Avoid: Weak password requirements
emailAndPassword: {
  password: {
    minLength: 4, // Too short
    requireSpecialChar: false, // Not requiring special characters
    requireNumbers: false, // Not requiring numbers
  },
},
```

### ✅ Solution: Strong Password Requirements
```typescript
// Good: Strong password requirements
emailAndPassword: {
  password: {
    minLength: 12, // Reasonable length
    requireSpecialChar: true, // Require special characters
    requireNumbers: true, // Require numbers
    requireUppercase: true, // Require uppercase
    requireLowercase: true, // Require lowercase
  },
},
```

## Performance Optimization Patterns

### ✅ DO: Cache Session Validation
```python
# Good: Cache session validation results
from functools import lru_cache
import time

class CachedTokenValidator:
    def __init__(self, cache_ttl: int = 300):  # 5 minutes cache
        self.cache_ttl = cache_ttl
        self.cache = {}

    def is_valid(self, token: str) -> bool:
        current_time = time.time()

        # Check cache first
        if token in self.cache:
            cached_time, is_valid = self.cache[token]
            if current_time - cached_time < self.cache_ttl:
                return is_valid

        # Validate token (this would call your actual validation)
        is_valid = self._validate_token(token)

        # Update cache
        self.cache[token] = (current_time, is_valid)
        return is_valid

    def _validate_token(self, token: str) -> bool:
        # Actual token validation logic
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return True
        except jwt.JWTError:
            return False
```

### ✅ DO: Use Connection Pooling for Database
```typescript
// Good: Use connection pooling for database operations
import { Pool } from "pg"; // PostgreSQL example

const dbPool = new Pool({
  connectionString: process.env.DATABASE_URL,
  min: 2,
  max: 10,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Use the pool in your auth functions
export async function getUserByEmail(email: string) {
  const client = await dbPool.connect();
  try {
    const result = await client.query(
      "SELECT * FROM users WHERE email = $1",
      [email]
    );
    return result.rows[0];
  } finally {
    client.release();
  }
}
```

## Testing Best Practices

### ✅ DO: Test Authentication Flows
```typescript
// Good: Comprehensive auth tests
import { describe, it, expect, beforeEach, afterEach } from "vitest";

describe("Authentication", () => {
  beforeEach(async () => {
    // Setup test database
    await setupTestDatabase();
  });

  afterEach(async () => {
    // Clean up test database
    await cleanupTestDatabase();
  });

  it("should allow valid user to sign in", async () => {
    // Create a test user
    const testUser = {
      email: "test@example.com",
      password: "SecurePassword123!",
      name: "Test User"
    };

    // Sign up the user
    const signUpResult = await signUp.email(testUser);
    expect(signUpResult.error).toBeNull();

    // Sign in with the same credentials
    const signInResult = await signIn.email({
      email: testUser.email,
      password: testUser.password
    });

    expect(signInResult.error).toBeNull();
    expect(signInResult.data).toBeDefined();
  });

  it("should reject invalid credentials", async () => {
    const signInResult = await signIn.email({
      email: "nonexistent@example.com",
      password: "wrongpassword"
    });

    expect(signInResult.error).toBeDefined();
    expect(signInResult.error?.code).toBe("INVALID_CREDENTIALS");
  });

  it("should validate email format", () => {
    const isValid = validateEmail("invalid-email");
    expect(isValid).toBe(false);
  });
});
```

### ✅ DO: Mock External Dependencies
```typescript
// Good: Mock external auth services for testing
import { vi, describe, it, expect } from "vitest";

vi.mock("@/lib/auth", () => ({
  signIn: {
    email: vi.fn()
  },
  signUp: {
    email: vi.fn()
  }
}));

describe("Login Form", () => {
  it("should handle sign in errors gracefully", async () => {
    const { signIn } = await import("@/lib/auth");
    (signIn.email as Mock).mockResolvedValue({
      error: { code: "INVALID_CREDENTIALS", message: "Invalid credentials" }
    });

    // Test your component with the mocked function
    // ...
  });
});
```

## Monitoring and Logging Best Practices

### ✅ DO: Log Authentication Events
```python
# Good: Log authentication events
import logging

logger = logging.getLogger(__name__)

async def log_auth_event(event_type: str, user_id: str = None, success: bool = True, details: dict = None):
    """Log authentication events for monitoring and security"""
    log_data = {
        "event_type": event_type,
        "user_id": user_id,
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }

    if success:
        logger.info(f"Auth event: {event_type}", extra=log_data)
    else:
        logger.warning(f"Auth event failed: {event_type}", extra=log_data)

# Usage in auth functions
async def authenticate_user(email: str, password: str):
    try:
        user = await validate_credentials(email, password)
        if user:
            await log_auth_event("login", user.id, success=True)
            return user
        else:
            await log_auth_event("login", success=False, details={"email": email})
            return None
    except Exception as e:
        await log_auth_event("login", success=False, details={"email": email, "error": str(e)})
        raise
```

### ✅ DO: Monitor for Suspicious Activity
```python
# Good: Monitor for suspicious authentication patterns
from collections import defaultdict
import time

class AuthMonitor:
    def __init__(self):
        self.failed_attempts = defaultdict(list)  # email -> [timestamps]
        self.max_attempts = 5
        self.time_window = 300  # 5 minutes

    def is_rate_limited(self, email: str) -> bool:
        """Check if an email is rate limited due to failed attempts"""
        current_time = time.time()
        # Remove old attempts outside the time window
        self.failed_attempts[email] = [
            timestamp for timestamp in self.failed_attempts[email]
            if current_time - timestamp < self.time_window
        ]

        # Check if too many failed attempts
        if len(self.failed_attempts[email]) >= self.max_attempts:
            return True

        return False

    def record_failed_attempt(self, email: str):
        """Record a failed authentication attempt"""
        self.failed_attempts[email].append(time.time())

    def record_successful_attempt(self, email: str):
        """Clear failed attempts after successful authentication"""
        if email in self.failed_attempts:
            del self.failed_attempts[email]
```