---
name: nextjs-16-app-router
description: |
  This skill should be used when working with Next.js 16 App Router, Server Components, Server Actions, or React 19 features.
  Use when creating routes, components, or API endpoints in Next.js 16 App Router.
---

# Next.js 16 App Router Skill

Auto-invoke when working with Next.js 16 App Router, Server Components, Server Actions, or React 19 features. Use when creating routes, components, or API endpoints in Next.js.

## Next.js 16 App Router File Structure

The Next.js 16 App Router follows a file-based routing system located in the `app/` directory:

```
app/
├── layout.tsx          # Root layout component
├── page.tsx           # Default page for the root route
├── globals.css        # Global styles
├── error.tsx          # Error boundary component
├── loading.tsx        # Loading UI component
├── not-found.tsx      # Not found page component
├── api/
│   └── route.ts       # API route handlers
├── [dynamic]/
│   └── page.tsx       # Dynamic route segment
├── (group)/
│   └── page.tsx       # Route groups
└── @slot/
    └── page.tsx       # Parallel routes
```

### Special Files in App Router

- `layout.tsx` - Wraps all components in a route segment
- `page.tsx` - Defines the main content of a route
- `loading.tsx` - Loading UI for Suspense boundaries
- `error.tsx` - Error boundary for nested routes
- `not-found.tsx` - Custom 404 page
- `global-error.tsx` - Global error boundary
- `route.ts` - API endpoints using route handlers
- `template.tsx` - Layout wrapper that recreates on navigation
- `default.tsx` - Fallback for parallel routes

## Server Components vs Client Components

### Server Components (Default)

Server Components are the default in Next.js App Router. They run only on the server and have access to server-side resources:

```typescript
// app/products/[id]/page.tsx
import { getProduct } from '@/lib/products'

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

Benefits of Server Components:
- Smaller bundle sizes (no client-side JavaScript for server logic)
- Direct database/file system access
- Better initial load performance
- Streaming capabilities

### Client Components ('use client')

Client Components run in the browser and enable interactivity:

```typescript
'use client'

import { useState, useEffect } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  )
}
```

Rules for Client Components:
- Must be placed at the top of the file, before imports
- Can only be imported by other Client Components or Server Components
- Cannot be imported by Server Components directly

## Server Actions Best Practices

Server Actions allow you to execute server-side logic directly from Client Components:

### Defining Server Actions

```typescript
// app/actions.ts
'use server'

import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createTodo(formData: FormData) {
  const title = formData.get('title') as string

  // Perform server-side validation
  if (!title) {
    return { message: 'Title is required' }
  }

  // Create todo in database
  await createTodoInDB(title)

  // Revalidate the path to show the new todo
  revalidatePath('/')

  // Redirect after successful creation
  redirect('/todos')
}
```

### Using Server Actions in Client Components

```typescript
'use client'

import { useFormState, useFormStatus } from 'react-dom'
import { createTodo } from '@/app/actions'

const initialState = {
  message: '',
}

function SubmitButton() {
  const { pending } = useFormStatus()

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Adding...' : 'Add'}
    </button>
  )
}

export function AddForm() {
  const [state, formAction] = useFormState(createTodo, initialState)

  return (
    <form action={formAction}>
      <label htmlFor="todo">Enter Task</label>
      <input type="text" id="todo" name="todo" required />
      <SubmitButton />
      <p aria-live="polite" role="status">
        {state?.message}
      </p>
    </form>
  )
}
```

### Passing Server Actions as Props

```typescript
// Parent component (can be a Server Component)
import { updateItem } from './actions'
import { ClientComponent } from './client-component'

export default function Page() {
  return <ClientComponent updateItemAction={updateItem} />
}
```

```typescript
// Client component
'use client'

export default function ClientComponent({
  updateItemAction,
}: {
  updateItemAction: (formData: FormData) => void
}) {
  return <form action={updateItemAction}>{/* ... */}</form>
}
```

## Data Fetching Patterns

Next.js 16 App Router uses native `fetch` for data retrieval without needing `useEffect`:

### Static Data (Cached by Default)

```typescript
// This request is cached until manually invalidated
// Similar to getStaticProps
export default async function Page() {
  const staticData = await fetch(`https://api.example.com/data`)
  const data = await staticData.json()

  return <div>{JSON.stringify(data)}</div>
}
```

### Dynamic Data (No Cache)

```typescript
// This request is refetched on every request
// Similar to getServerSideProps
export default async function Page() {
  const dynamicData = await fetch(`https://api.example.com/data`, {
    cache: 'no-store'
  })
  const data = await dynamicData.json()

  return <div>{JSON.stringify(data)}</div>
}
```

### Revalidated Data

```typescript
// This request is cached with a lifetime of 10 seconds
// Similar to getStaticProps with revalidate
export default async function Page() {
  const revalidatedData = await fetch(`https://api.example.com/data`, {
    next: { revalidate: 10 },
  })
  const data = await revalidatedData.json()

  return <div>{JSON.stringify(data)}</div>
}
```

## Route Handlers (route.ts)

Create API endpoints using route handlers in the app directory:

```typescript
// app/api/users/route.ts
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  const user = await getUser(id)

  return NextResponse.json({ user })
}

export async function POST(request: Request) {
  const body = await request.json()
  const user = await createUser(body)

  return NextResponse.json({ user }, { status: 201 })
}

export async function PUT(request: Request) {
  const body = await request.json()
  const user = await updateUser(body)

  return NextResponse.json({ user })
}

export async function DELETE(request: Request) {
  const { searchParams } = new URL(request.url)
  const id = searchParams.get('id')

  await deleteUser(id)

  return new Response(null, { status: 204 })
}
```

Supported HTTP methods: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS

## Metadata API Usage

Define metadata for SEO and social sharing:

### Static Metadata

```typescript
// app/page.tsx
export const metadata = {
  title: 'My App',
  description: 'Welcome to My App',
}
```

### Dynamic Metadata

```typescript
// app/posts/[slug]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  params
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await getPost(params.slug)

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [
        {
          url: post.coverImage,
          width: 1200,
          height: 630,
        },
      ],
      type: 'article',
      publishedTime: post.date,
      authors: [post.author.name],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  }
}
```

## Error Handling

### Local Error Boundaries (error.tsx)

```typescript
// app/error.tsx
'use client'

import { useEffect } from 'react'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  useEffect(() => {
    console.error(error)
  }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

### Not Found Pages (not-found.tsx)

```typescript
// app/not-found.tsx
import Link from 'next/link'

export default function NotFound() {
  return (
    <div>
      <h2>Not Found</h2>
      <p>Could not find requested resource</p>
      <Link href="/">Return Home</Link>
    </div>
  )
}
```

### Programmatic Not Found

```typescript
// In a page component
import { notFound } from 'next/navigation'

export default async function Post({ params }: { params: { id: string } }) {
  const post = await getPost(params.id)

  if (!post) {
    notFound()
  }

  return <article>{post.content}</article>
}
```

## Loading States

### Global Loading UI (loading.tsx)

```typescript
// app/loading.tsx
export default function Loading() {
  return (
    <div className="loading">
      <div className="spinner"></div>
      <p>Loading...</p>
    </div>
  )
}
```

### Component-Level Loading

```typescript
// Using suspense for specific components
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      <Suspense fallback={<div>Loading feed...</div>}>
        <Feed />
      </Suspense>
      <Suspense fallback={<div>Loading sidebar...</div>}>
        <Sidebar />
      </Suspense>
    </div>
  )
}
```

## Common Patterns for Forms with Server Actions

### Form with Validation and Error Handling

```typescript
'use client'

import { useActionState } from 'react'
import { createUser } from '@/app/actions'

const initialState = {
  message: '',
  errors: {},
}

export function SignupForm() {
  const [state, formAction, pending] = useActionState(createUser, initialState)

  return (
    <form action={formAction}>
      <label htmlFor="email">Email</label>
      <input
        type="email"
        id="email"
        name="email"
        required
      />
      {state.errors?.email && (
        <p className="error">{state.errors.email}</p>
      )}

      <label htmlFor="password">Password</label>
      <input
        type="password"
        id="password"
        name="password"
        required
      />
      {state.errors?.password && (
        <p className="error">{state.errors.password}</p>
      )}

      <p aria-live="polite">{state?.message}</p>
      <button disabled={pending}>Sign up</button>
    </form>
  )
}
```

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing Next.js project structure, routing patterns, component conventions |
| **Conversation** | User's specific requirements for routes, components, or API endpoints |
| **Skill References** | Next.js 16 patterns from `references/` (file structure, server components, data fetching, etc.) |
| **User Guidelines** | Project-specific conventions, team standards, performance requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).