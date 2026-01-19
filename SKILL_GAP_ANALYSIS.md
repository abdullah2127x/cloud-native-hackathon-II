# Skill Gap Analysis - Better Auth Integration

**Date:** January 19, 2026
**Project:** Todo Web Application (Phase 2 Implementation)
**Skill Analyzed:** `better-auth-integration`
**Related Skills:** `fastapi-sqlmodel-patterns`, `integration-pattern-finder`

---

## Executive Summary

During Phase 2 implementation using the `better-auth-integration` skill, **7 critical errors occurred** that could have been prevented with better skill documentation and implementation. This analysis identifies the gaps in skill design and provides **actionable improvements** for future agents.

### Key Findings

| Finding | Impact | Priority |
|---------|--------|----------|
| JWT plugin not configured for separate backend | **CRITICAL** - Complete auth failure | 🔴 HIGH |
| Missing dependency documentation | **HIGH** - Build failures | 🟠 HIGH |
| Environment variable setup incomplete | **MEDIUM** - Migration failures | 🟡 MEDIUM |
| Database-specific configurations not handled | **MEDIUM** - Runtime errors | 🟡 MEDIUM |
| Form state management not documented | **LOW** - UX issues | 🟢 LOW |

---

## Table of Contents

1. [Error-by-Error Analysis](#error-by-error-analysis)
2. [Skill Documentation Gaps](#skill-documentation-gaps)
3. [Recommended Skill Improvements](#recommended-skill-improvements)
4. [Updated Skill Specification](#updated-skill-specification)
5. [Agent Checklist for Future Use](#agent-checklist-for-future-use)

---

## Error-by-Error Analysis

### Error 1: PostgreSQL Connection Configuration ❌

**Error:** `psycopg2.ProgrammingError: invalid dsn: invalid connection option "check_same_thread"`

**Related Skill:** `fastapi-sqlmodel-patterns`

#### What the Skill Should Have Done

The `fastapi-sqlmodel-patterns` skill should have generated database connection code that:
1. Detects database type from connection string
2. Conditionally applies database-specific options
3. Provides examples for SQLite, PostgreSQL, and MySQL

#### What the Skill Actually Did

Generated generic SQLModel code without database-type awareness:

```python
# SKILL OUTPUT (WRONG)
engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args={"check_same_thread": False},  # ❌ SQLite-only
)
```

#### What Should Have Been Generated

```python
# SKILL OUTPUT (CORRECT)
# Determine connect_args based on database type
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif settings.database_url.startswith("postgresql"):
    # PostgreSQL-specific options can go here
    pass

engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args,
)
```

#### Skill Gap Identified

**Missing:** Database-type detection and conditional configuration

**Recommendation:**
- Add database detection logic to `fastapi-sqlmodel-patterns` skill
- Include examples for all major databases (SQLite, PostgreSQL, MySQL)
- Document database-specific connection options

---

### Error 2: Missing Neon Database Package ❌

**Error:** `Module not found: Can't resolve '@neondatabase/serverless'`

**Related Skill:** `better-auth-integration`

#### What the Skill Should Have Done

The `better-auth-integration` skill documentation states:

> "Generates frontend/src/lib/auth.ts (server config)"
> "Configures database schema for user tables"

It should have:
1. Detected database type (Neon, Supabase, Turso, vanilla PostgreSQL)
2. **Listed ALL required npm packages** based on database choice
3. Provided installation commands
4. Updated `package.json` automatically or shown commands

#### What the Skill Actually Did

Generated `auth.ts` with Neon import but didn't:
- Add `@neondatabase/serverless` to dependencies
- Warn about missing package
- Provide installation command

```typescript
// SKILL OUTPUT (INCOMPLETE)
import { Pool } from "@neondatabase/serverless";  // ❌ Not in package.json

export const auth = betterAuth({
  database: pool,
  // ...
});
```

#### What Should Have Been Generated

**Option A: Update package.json automatically**
```json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",  // ✅ Added
    "better-auth": "^1.4.14",
    // ...
  }
}
```

**Option B: Provide clear installation steps**
```markdown
## Installation Required

After generating files, install required dependencies:

### For Neon Serverless PostgreSQL:
```bash
npm install @neondatabase/serverless
```

### For Supabase:
```bash
npm install @supabase/supabase-js
```

### For Turso (LibSQL):
```bash
npm install @libsql/client
```
```

#### Skill Gap Identified

**Missing:** Database-specific dependency management

**Recommendation:**
- **Add dependency detection** based on database choice
- **Auto-update package.json** or provide explicit installation commands
- **Validate dependencies** before generating code
- **Create a dependencies checklist** for each database type

---

### Error 3: Better Auth Migration Environment Variable ❌

**Error:** `No database host or connection string was set` (during migration)

**Related Skill:** `better-auth-integration`

#### What the Skill Should Have Done

The skill should have:
1. Explained that Better Auth CLI reads `.env`, NOT `.env.local`
2. Provided migration setup instructions
3. Warned about environment file loading differences
4. Documented the workaround

#### What the Skill Actually Did

Generated `.env.local` file but didn't document CLI tool behavior:

```env
# SKILL OUTPUT (INCOMPLETE)
# .env.local
DATABASE_URL="postgresql://..."
BETTER_AUTH_SECRET="..."
```

**Missing documentation:**
- How to run migrations
- Which env file to use
- CLI tool behavior differences

#### What Should Have Been Generated

**Better documentation:**

```markdown
## Environment Setup

### Development (.env.local)
Next.js automatically loads `.env.local` for the application:

\`\`\`env
DATABASE_URL="postgresql://..."
BETTER_AUTH_SECRET="..."
\`\`\`

### Migration Setup (.env)
**IMPORTANT:** Better Auth CLI only reads `.env` files, not `.env.local`.

Before running migrations, create a `.env` file:

\`\`\`bash
# Option 1: Copy .env.local to .env (temporary)
cp .env.local .env

# Option 2: Create .env with same variables
cat > .env << EOF
DATABASE_URL="your-database-url"
BETTER_AUTH_SECRET="your-secret"
EOF
\`\`\`

### Run Migration

\`\`\`bash
npx @better-auth/cli@latest migrate
\`\`\`

**Security Note:**
- Add `.env` to `.gitignore` (already configured)
- Only commit `.env.example` with placeholder values
- Delete temporary `.env` after migration if desired
\`\`\`
```

#### Skill Gap Identified

**Missing:** CLI tool environment file documentation

**Recommendation:**
- **Document all CLI tools** used by the skill and their env file behavior
- **Provide setup scripts** to automate env file creation
- **Add warnings** about file loading differences
- **Create .env.example** automatically with documented placeholders

---

### Error 4: Better Auth Database Tables Missing ❌

**Error:** `relation "account" does not exist`

**Related Skill:** `better-auth-integration`

#### What the Skill Should Have Done

The skill documentation states:

> "Database migration commands"

It should have:
1. **Automatically run migration** after generating files
2. Or **provide clear step-by-step instructions**
3. **Verify tables exist** before considering setup complete
4. **Rollback instructions** if migration fails

#### What the Skill Actually Did

Generated files but didn't:
- Run migration automatically
- Provide migration command clearly
- Verify table creation
- Document expected database schema

#### What Should Have Been Generated

**Option A: Automated migration (if possible)**
```bash
# Skill runs automatically:
npx @better-auth/cli@latest migrate --yes
```

**Option B: Clear step-by-step guide**
```markdown
## Database Migration (REQUIRED)

Better Auth requires specific database tables. Run migration:

### Step 1: Ensure DATABASE_URL is set

Check that your `.env` file contains:
\`\`\`env
DATABASE_URL="postgresql://..."
\`\`\`

### Step 2: Run migration

\`\`\`bash
cd frontend
npx @better-auth/cli@latest migrate
\`\`\`

### Step 3: Verify tables created

Expected tables:
- ✅ `user` - User accounts
- ✅ `session` - Active sessions
- ✅ `account` - OAuth providers
- ✅ `verification` - Email verification tokens

### Troubleshooting

**Error: "No database connection"**
- Ensure DATABASE_URL is in `.env` (not just `.env.local`)
- CLI tools don't read `.env.local`

**Error: "Migration failed"**
- Check database permissions
- Verify connection string format
- Run with --verbose flag for details:
  \`\`\`bash
  npx @better-auth/cli@latest migrate --verbose
  \`\`\`

### Rollback (if needed)

\`\`\`bash
npx @better-auth/cli@latest rollback
\`\`\`
\`\`\`
```

#### Skill Gap Identified

**Missing:** Migration execution and verification

**Recommendation:**
- **Automate migration** if possible (prompt user for confirmation)
- **Verify table creation** before marking setup complete
- **Provide troubleshooting steps** for common migration errors
- **Document rollback procedures**

---

### Error 5: Import/Export Mismatch ❌

**Error:** `Export api doesn't exist in target module`

**Related Skill:** General coding patterns (not skill-specific)

#### What Should Have Been Done

1. Use consistent export patterns across all generated files
2. Document import/export conventions in CLAUDE.md
3. Validate imports when generating code

#### Skill Gap Identified

**Missing:** Import/export convention enforcement

**Recommendation:**
- **Standardize exports** - use default exports OR named exports consistently
- **Generate import examples** with each file
- **Add linting rules** to catch mismatches early

---

### Error 6: JWT Authentication Failure (CRITICAL) 🚨

**Error:** 401 Unauthorized on API calls after successful sign-in

**Root Cause:** Better Auth configured for **cookie-based sessions**, but separate backend needs **JWT tokens**

**Related Skill:** `better-auth-integration` + `integration-pattern-finder`

---

#### The Critical Architecture Question

This is the **MOST IMPORTANT** error that the skill failed to address.

**Question the skill should ask:**

> "Is your backend on a **separate domain** or **same domain** as your frontend?"

**Impact:**
- Same domain → Cookie-based auth works ✅
- Separate domain → **JWT tokens required** ✅

---

#### What the Skill Should Have Done

The `better-auth-integration` skill should have:

1. **Asked about architecture**:
   - "Is your backend separate from Next.js?" (Yes/No)
   - "Backend URL?" (e.g., `http://localhost:8000`)

2. **Configured appropriately**:

**For SEPARATE backend (our case):**
```typescript
// ✅ CORRECT - JWT Plugin Required
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";  // 🔑 Critical

export const auth = betterAuth({
  database: pool,
  emailAndPassword: { enabled: true },
  plugins: [
    jwt({  // 🔑 This enables JWT tokens for separate backends
      jwks: {
        jwksPath: "/.well-known/jwks.json",
      },
    }),
  ],
});
```

**For SAME domain (monolithic):**
```typescript
// ✅ CORRECT - Cookies work fine
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: pool,
  emailAndPassword: { enabled: true },
  // No JWT plugin needed - cookies work
});
```

---

#### What the Skill Actually Did

Generated cookie-based configuration without asking about architecture:

```typescript
// ❌ WRONG - No JWT plugin for separate backend
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: pool,
  emailAndPassword: { enabled: true },
  // Missing JWT plugin! 🚨
});
```

**This caused:**
1. Sign-in worked (cookies set) ✅
2. But API interceptor couldn't access token ❌
3. Backend received no JWT ❌
4. All API calls returned 401 Unauthorized ❌

---

#### Complete JWT Setup That Was Missing

**1. Server Configuration (auth.ts)**
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";  // ✅ Add this
import { Pool } from "@neondatabase/serverless";

export const auth = betterAuth({
  database: pool,
  emailAndPassword: { enabled: true },
  plugins: [
    jwt({
      jwks: {
        jwksPath: "/.well-known/jwks.json",
      },
    }),
  ],
});
```

**2. Client Configuration (auth-client.ts)**
```typescript
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";  // ✅ Add this

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
  plugins: [
    jwtClient({  // ✅ Add this
      jwks: {
        jwksPath: "/.well-known/jwks.json",
      },
    }),
  ],
});

// ✅ Add JWT helper functions
export async function fetchAndStoreJwt() {
  const { data } = await authClient.token();
  if (data?.token) {
    localStorage.setItem("jwt_token", data.token);
    return data.token;
  }
  return null;
}

export function getJwtToken() {
  return localStorage.getItem("jwt_token");
}
```

**3. API Interceptor (api-interceptor.ts)**
```typescript
import axios from 'axios';
import { getJwtToken } from '@/lib/auth-client';

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

// ✅ Add JWT to all requests
apiClient.interceptors.request.use((config) => {
  const token = getJwtToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

**4. Sign-In Form Updates**
```typescript
import { signIn, fetchAndStoreJwt } from "@/lib/auth-client";

const onSubmit = async (data) => {
  await signIn.email(data);
  await fetchAndStoreJwt();  // ✅ Fetch JWT after sign-in
  router.push("/dashboard");
};
```

**5. Backend JWT Verification (jwt_handler.py)**
```python
import jwt
from jwt import PyJWKClient

# ✅ JWKS URL must match Better Auth setup
jwks_url = f"{settings.better_auth_url}/api/auth/.well-known/jwks.json"
jwks_client = PyJWKClient(jwks_url)

def verify_jwt(token: str):
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["EdDSA"],  # ✅ Better Auth uses EdDSA by default
        audience=settings.better_auth_url,
    )
    return payload
```

---

#### Skill Gap Identified

**CRITICAL GAPS:**

1. **No architecture detection** - Skill doesn't ask about separate backend
2. **No JWT configuration** - Skill defaults to cookie-only auth
3. **No backend integration guide** - Skill doesn't explain how backend verifies tokens
4. **No algorithm documentation** - Skill doesn't mention EdDSA vs RS256 vs ES256
5. **No JWKS URL guidance** - Skill doesn't explain API route structure

---

#### Recommendation: Interactive Skill Flow

The skill should use **interactive prompts** to determine architecture:

```markdown
## Better Auth Integration Skill

### Step 1: Detect Architecture

**Question 1:** Is your backend separate from your Next.js frontend?
- [ ] Yes - Backend on different domain (e.g., FastAPI, Express on another port)
- [ ] No - Backend is Next.js API routes (monolithic)

**If YES (separate backend):**

**Question 2:** What backend framework?
- [ ] FastAPI (Python)
- [ ] Express (Node.js)
- [ ] Nest.js (Node.js)
- [ ] Spring Boot (Java)
- [ ] Other: ________

**Question 3:** Backend URL?
- Example: `http://localhost:8000` (development)
- Example: `https://api.example.com` (production)

---

### Step 2: Generate Configuration

**For SEPARATE backend:**
- ✅ JWT plugin enabled
- ✅ jwtClient plugin enabled
- ✅ Backend verification code generated
- ✅ API interceptor with JWT
- ✅ Sign-in/sign-up with token fetching

**For MONOLITHIC (Next.js API routes):**
- ✅ Cookie-based auth (default)
- ✅ No JWT plugin needed
- ✅ Middleware for protected routes

---

### Step 3: Generate Backend Integration

**For FastAPI backend:**

Generates:
1. `backend/src/auth/jwt_handler.py` - JWT verification
2. `backend/src/middleware/auth.py` - Auth middleware
3. `backend/src/config.py` - JWT settings (algorithm, audience)
4. Example protected endpoint

**For Express backend:**

Generates:
1. `backend/src/middleware/jwt.ts` - JWT verification
2. `backend/src/config.ts` - JWT settings
3. Example protected endpoint

---

### Step 4: Documentation

Generates comprehensive docs explaining:
- How authentication flow works
- JWT token lifecycle
- Token storage (localStorage vs memory)
- Security considerations
- Common errors and troubleshooting
\`\`\`
```

---

### Error 7: TaskForm Validation State Not Clearing ❌

**Error:** Validation errors persist after form submission, fields don't clear

**Related Skill:** React Hook Form patterns (not a specific skill, but should be documented)

#### What Should Have Been Documented

**In frontend/CLAUDE.md:**

```markdown
## React Hook Form Patterns

### Form Reset Pattern

**Problem:** `reset()` doesn't always clear validation state properly.

**Solution:** Use React key prop to force remount.

\`\`\`typescript
// Parent component
const [formKey, setFormKey] = useState(0);

const handleSubmit = async (data) => {
  await saveTodo(data);
  setFormKey(prev => prev + 1);  // Force remount
};

return (
  <TodoForm
    key={formKey}  // ✅ Forces fresh instance
    onSubmit={handleSubmit}
    defaultValues={{ title: "", description: "" }}
  />
);
\`\`\`

**Why this works:**
- Key change triggers React to unmount old component
- New component has fresh form state
- All validation errors cleared automatically

**When to use:**
- Forms with complex validation
- Forms that need frequent resets
- Forms where reset() fails

**When NOT to use:**
- Simple forms (reset() works fine)
- Forms that maintain state between submissions
\`\`\`
```

#### Skill Gap Identified

**Missing:** React Hook Form best practices in CLAUDE.md

**Recommendation:**
- Add **React Hook Form patterns** section to frontend CLAUDE.md template
- Include **form reset strategies** with trade-offs
- Document **key prop pattern** for difficult cases
- Provide **troubleshooting guide** for common form issues

---

## Skill Documentation Gaps

### Overall Analysis

The `better-auth-integration` skill has **good intentions** but **critical gaps** in:

1. **Architecture Awareness** - Doesn't detect monolithic vs microservices
2. **Dependency Management** - Doesn't handle database-specific packages
3. **Migration Automation** - Doesn't run or verify migrations
4. **Backend Integration** - No guidance for separate backends
5. **Error Prevention** - Doesn't anticipate common mistakes

---

### Gap Summary Table

| Gap Category | Severity | Impact | Fix Complexity |
|--------------|----------|--------|----------------|
| JWT configuration for separate backend | 🔴 CRITICAL | Auth failure | HIGH |
| Database-specific dependencies | 🟠 HIGH | Build failure | MEDIUM |
| Migration documentation | 🟡 MEDIUM | Setup failure | LOW |
| Environment file behavior | 🟡 MEDIUM | CLI failure | LOW |
| Database connection options | 🟡 MEDIUM | Runtime error | MEDIUM |
| Import/export conventions | 🟢 LOW | Code error | LOW |
| Form state management | 🟢 LOW | UX issue | LOW |

---

## Recommended Skill Improvements

### 1. Add Architecture Detection 🏗️

**Current:** Skill generates one-size-fits-all configuration

**Improved:** Skill asks questions and adapts output

```markdown
## Skill Execution Flow (NEW)

### Phase 1: Context Gathering

Ask user:
1. Backend architecture? (Monolithic / Separate)
2. If separate: Backend framework? (FastAPI / Express / Other)
3. If separate: Backend URL? (http://localhost:8000)
4. Database type? (Neon / Supabase / PostgreSQL / MySQL / SQLite)
5. Auth features? (Email/Password, OAuth, 2FA, Magic Links)

### Phase 2: Configuration Generation

Based on answers:
- Generate auth.ts with appropriate plugins
- Generate auth-client.ts with appropriate plugins
- Generate backend verification code (if separate backend)
- Generate API interceptor (if separate backend)
- Update package.json with database-specific packages

### Phase 3: Setup Automation

- Create .env and .env.local with correct variables
- Run npm install (if packages added)
- Run migration (with user confirmation)
- Verify tables created

### Phase 4: Documentation

Generate:
- Setup guide (step-by-step)
- Architecture diagram
- Authentication flow diagram
- Troubleshooting guide
- Testing guide
\`\`\`
```

---

### 2. Enhance Dependency Management 📦

**Current:** Generates imports without ensuring packages exist

**Improved:** Detects and installs dependencies

```markdown
## Dependency Detection (NEW)

### Step 1: Analyze Required Packages

Based on database choice:
- Neon → @neondatabase/serverless
- Supabase → @supabase/supabase-js
- Turso → @libsql/client
- Vanilla PostgreSQL → pg

### Step 2: Check package.json

\`\`\`typescript
// Skill checks if packages exist
const packageJson = JSON.parse(fs.readFileSync('package.json'));
const missing = requiredPackages.filter(
  pkg => !packageJson.dependencies[pkg]
);
\`\`\`

### Step 3: Update or Prompt

**Option A:** Auto-update package.json (safer)
\`\`\`json
{
  "dependencies": {
    "@neondatabase/serverless": "^1.0.2",  // Added
    "better-auth": "^1.4.14"
  }
}
\`\`\`

Then prompt user:
> "I've added @neondatabase/serverless to package.json. Run `npm install` to install it."

**Option B:** Provide install command
> "Please run: `npm install @neondatabase/serverless`"

### Step 4: Verify Installation

After user confirms, verify package exists:
\`\`\`bash
npm list @neondatabase/serverless
\`\`\`
\`\`\`
```

---

### 3. Automate Migration with Verification ✅

**Current:** Mentions migration but doesn't run it

**Improved:** Runs migration and verifies tables

```markdown
## Migration Automation (NEW)

### Step 1: Setup Environment

1. Check if .env exists
2. If not, copy .env.local to .env (with user permission)
3. Verify DATABASE_URL is set

### Step 2: Run Migration

\`\`\`bash
# Prompt user first
"About to run Better Auth migration. This will create tables in your database. Continue? (y/n)"

# If yes:
npx @better-auth/cli@latest migrate
\`\`\`

### Step 3: Verify Tables

Query database to confirm tables exist:
\`\`\`sql
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN ('user', 'session', 'account', 'verification');
\`\`\`

### Step 4: Report Results

✅ Success:
> "Migration complete! Created tables: user, session, account, verification"

❌ Failure:
> "Migration failed. Check DATABASE_URL in .env file."
> "Error: [specific error message]"
> "Troubleshooting: [link to docs]"

### Step 5: Cleanup (optional)

Prompt user:
> "Delete temporary .env file? Next.js will use .env.local. (y/n)"
\`\`\`
```

---

### 4. Generate Backend Integration Code 🔗

**Current:** No backend integration guidance

**Improved:** Generates backend verification code

```markdown
## Backend Integration Generation (NEW)

### For FastAPI Backend

Generates these files:

**1. backend/src/auth/jwt_handler.py**
\`\`\`python
"""JWT verification using JWKS from Better Auth"""
import jwt
from jwt import PyJWKClient
from typing import Dict
from src.config import settings

# JWKS client for Better Auth
jwks_url = f"{settings.better_auth_url}/api/auth/.well-known/jwks.json"
jwks_client = PyJWKClient(jwks_url)

def verify_jwt(token: str) -> Dict:
    """Verify JWT token using JWKS"""
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["EdDSA"],  # Better Auth default
        audience=settings.better_auth_url,
    )
    return payload

def get_user_id(token: str) -> str:
    """Extract user ID from token"""
    payload = verify_jwt(token)
    return payload.get("sub")
\`\`\`

**2. backend/src/middleware/auth.py**
\`\`\`python
"""Authentication middleware"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.jwt_handler import verify_jwt, get_user_id

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """Dependency to get current user ID from JWT"""
    try:
        token = credentials.credentials
        user_id = get_user_id(token)
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
\`\`\`

**3. backend/src/config.py (additions)**
\`\`\`python
class Settings(BaseSettings):
    # Better Auth JWT settings
    better_auth_url: str = "http://localhost:3000"
    jwt_algorithm: str = "EdDSA"  # Better Auth default
    jwt_audience: str = "http://localhost:3000"
\`\`\`

**4. Example protected endpoint**
\`\`\`python
from fastapi import APIRouter, Depends
from src.middleware.auth import get_current_user_id

router = APIRouter()

@router.get("/api/todos")
async def get_todos(user_id: str = Depends(get_current_user_id)):
    """Get todos for authenticated user"""
    # user_id is automatically extracted from JWT
    return {"user_id": user_id, "todos": []}
\`\`\`

### For Express Backend

Generates similar files for Express/TypeScript
\`\`\`
```

---

### 5. Create Comprehensive Documentation 📚

**Current:** Basic setup instructions

**Improved:** Complete guides with diagrams

```markdown
## Documentation Generation (NEW)

### Files Generated:

**1. SETUP_GUIDE.md**
- Step-by-step installation
- Environment setup
- Migration process
- Verification steps
- Troubleshooting

**2. AUTHENTICATION_FLOW.md**
- Architecture diagram
- Flow diagrams (sign-up, sign-in, API calls)
- Token lifecycle
- Security considerations

**3. TROUBLESHOOTING.md**
- Common errors with solutions
- Database connection issues
- Migration failures
- JWT verification problems
- CORS issues

**4. TESTING_GUIDE.md**
- How to mock Better Auth in tests
- Test examples (unit, integration)
- MSW setup for API mocking

**5. SECURITY_CONSIDERATIONS.md**
- Token storage best practices
- XSS prevention
- CSRF protection
- Rate limiting
- Password policies
\`\`\`
```

---

## Updated Skill Specification

### Proposed: `better-auth-integration-v2` Skill

**Purpose:** Generate complete Better Auth setup with architecture awareness and backend integration

---

### Input Parameters

```yaml
skill: better-auth-integration
version: 2.0

parameters:
  # Required
  framework:
    type: enum
    values: [next-app-router, next-pages-router]
    description: "Next.js routing approach"

  database:
    type: enum
    values: [neon, supabase, turso, postgres, mysql, sqlite]
    description: "Database provider/type"

  # New - Architecture detection
  architecture:
    type: enum
    values: [monolithic, microservices]
    description: "Is backend separate from Next.js?"
    prompt: "Is your backend on a separate domain/port?"

  # New - Backend details (if microservices)
  backend:
    type: object
    required_if: architecture == "microservices"
    properties:
      framework:
        type: enum
        values: [fastapi, express, nestjs, spring-boot, other]
      url:
        type: string
        example: "http://localhost:8000"
      language:
        type: enum
        values: [python, typescript, javascript, java]

  # Optional
  features:
    type: array
    values: [email-password, oauth-google, oauth-github, magic-link, 2fa, passkey]
    default: [email-password]

  srcDir:
    type: boolean
    default: false
    description: "Using src/ directory?"

  typescript:
    type: boolean
    default: true
```

---

### Output Files

```yaml
outputs:
  frontend:
    - src/lib/auth.ts                    # Server config (with JWT if needed)
    - src/lib/auth-client.ts             # Client config (with jwtClient if needed)
    - src/app/api/auth/[...all]/route.ts # API handler
    - src/middleware/api-interceptor.ts  # With JWT logic (if microservices)
    - .env.local                         # Environment variables
    - .env.example                       # Example values

  backend:  # Only if architecture == "microservices"
    fastapi:
      - src/auth/jwt_handler.py          # JWT verification
      - src/middleware/auth.py           # Auth middleware
      - src/config.py                    # JWT settings (append)
    express:
      - src/middleware/jwt.ts            # JWT verification
      - src/middleware/auth.ts           # Auth middleware
      - src/config.ts                    # JWT settings (append)

  documentation:
    - SETUP_GUIDE.md                     # Step-by-step setup
    - AUTHENTICATION_FLOW.md             # Architecture and flow diagrams
    - TROUBLESHOOTING.md                 # Common issues and solutions
    - TESTING_GUIDE.md                   # Test patterns

  package_updates:
    - frontend/package.json              # Add database-specific deps
    - backend/requirements.txt           # Add PyJWT, cryptography (FastAPI)
    - backend/package.json               # Add jose, jwks-rsa (Express)
```

---

### Execution Flow

```yaml
execution:
  phase_1_context:
    - Ask architecture questions
    - Detect existing files
    - Validate database connection

  phase_2_dependencies:
    - Detect required packages
    - Update package.json / requirements.txt
    - Prompt for npm install / pip install

  phase_3_generation:
    - Generate frontend auth files
    - Generate backend auth files (if microservices)
    - Generate API interceptor (if microservices)
    - Update configuration files

  phase_4_migration:
    - Setup .env for CLI
    - Run Better Auth migration (with confirmation)
    - Verify tables created
    - Cleanup temporary files

  phase_5_documentation:
    - Generate setup guide
    - Generate architecture diagrams
    - Generate troubleshooting guide
    - Generate testing guide

  phase_6_verification:
    - Check all files created
    - Check dependencies installed
    - Check tables exist
    - Run health check (optional)

  phase_7_report:
    - Summary of what was created
    - Next steps for user
    - Links to documentation
    - Troubleshooting tips
```

---

## Agent Checklist for Future Use

When an agent uses the `better-auth-integration` skill in the future, follow this checklist:

### ✅ Pre-Execution Checklist

- [ ] **Determine architecture**: Is backend separate from Next.js?
- [ ] **If separate backend**:
  - [ ] What framework? (FastAPI, Express, etc.)
  - [ ] What's the backend URL?
  - [ ] What language?
- [ ] **Database type**: Neon, Supabase, PostgreSQL, MySQL, SQLite?
- [ ] **Check existing files**: Don't overwrite without confirmation
- [ ] **Verify environment**: Node.js, npm/yarn/pnpm, database client installed?

### ✅ During Execution Checklist

- [ ] **Dependencies**: Check if database-specific packages are installed
- [ ] **If missing**: Update package.json or provide install command
- [ ] **JWT configuration**: Add JWT plugin if backend is separate
- [ ] **Environment files**: Create both .env and .env.local
- [ ] **Run migration**: With user confirmation
- [ ] **Verify tables**: Query database to confirm

### ✅ Post-Execution Checklist

- [ ] **Test sign-up**: Can user create account?
- [ ] **Test sign-in**: Can user log in?
- [ ] **Test API call**: Does backend accept JWT token?
- [ ] **Check logs**: Any errors in frontend or backend?
- [ ] **Documentation**: Did we generate setup guide?
- [ ] **Next steps**: Did we tell user what to do next?

### ✅ Error Prevention Checklist

**Database Connection:**
- [ ] Used conditional `connect_args` based on database type?
- [ ] Not applying SQLite options to PostgreSQL?

**Dependencies:**
- [ ] All imported packages exist in package.json?
- [ ] Database driver package installed?

**Environment:**
- [ ] .env.local for Next.js app?
- [ ] .env for CLI tools?
- [ ] Both have same DATABASE_URL?

**JWT Configuration:**
- [ ] JWT plugin added if backend is separate?
- [ ] jwtClient plugin added to auth-client?
- [ ] Backend configured to verify EdDSA tokens?
- [ ] JWKS URL matches API route structure?

**Migration:**
- [ ] Migration ran successfully?
- [ ] All required tables created?
- [ ] User, session, account, verification tables exist?

**Backend Integration:**
- [ ] Backend has JWT verification code?
- [ ] Backend has auth middleware?
- [ ] Backend configured with correct algorithm (EdDSA)?
- [ ] Backend configured with correct audience?

**Testing:**
- [ ] Can sign up successfully?
- [ ] Can sign in successfully?
- [ ] JWT token fetched after sign-in?
- [ ] API calls include Authorization header?
- [ ] Backend returns 200 (not 401)?

---

## Summary and Recommendations

### Critical Improvements Needed

1. **Architecture Detection** 🚨
   - **Priority:** CRITICAL
   - **Impact:** Prevents complete auth failure
   - **Action:** Add interactive prompts to detect monolithic vs microservices

2. **JWT Configuration** 🚨
   - **Priority:** CRITICAL
   - **Impact:** Enables separate backend authentication
   - **Action:** Auto-configure JWT plugin when backend is separate

3. **Dependency Management** ⚠️
   - **Priority:** HIGH
   - **Impact:** Prevents build failures
   - **Action:** Detect and install database-specific packages

4. **Migration Automation** ⚠️
   - **Priority:** HIGH
   - **Impact:** Ensures database setup completes
   - **Action:** Run migration and verify table creation

5. **Backend Integration** ⚠️
   - **Priority:** HIGH
   - **Impact:** Provides complete end-to-end solution
   - **Action:** Generate backend JWT verification code

### Next Steps

**For Skill Developers:**
1. Update `better-auth-integration` skill to v2 specification
2. Add architecture detection logic
3. Implement JWT configuration branching
4. Add migration automation with verification
5. Generate backend integration code
6. Create comprehensive documentation templates

**For Future Agents:**
1. Use the "Agent Checklist" before, during, and after skill execution
2. Always verify architecture (monolithic vs microservices)
3. Always check dependencies before generating imports
4. Always run and verify migrations
5. Always test the complete authentication flow

**For Project Teams:**
1. Review this analysis for future project planning
2. Consider creating project-specific skill templates
3. Document architecture decisions early
4. Test authentication end-to-end before proceeding

---

**Document Version:** 1.0
**Date:** January 19, 2026
**Status:** Analysis Complete - Ready for Skill Improvements
**Next Review:** After skill v2 implementation
