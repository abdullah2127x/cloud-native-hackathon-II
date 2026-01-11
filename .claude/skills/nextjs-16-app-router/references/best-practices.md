# Next.js 16 App Router - Best Practices and Common Pitfalls

## Server Component Best Practices

### ✅ DO: Leverage Server Components for Data Fetching
Server Components can directly fetch data without needing client-side JavaScript:

```typescript
// Good: Direct data fetching in Server Component
export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await fetchProduct(params.id) // Runs on server, no client JS

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

### ❌ AVOID: Unnecessary Client Components for Static Content
Don't use Client Components when Server Components would suffice:

```typescript
// Avoid: Unnecessary Client Component for static content
'use client'

export default function ProductPage({ params }: { params: { id: string } }) {
  const [product, setProduct] = useState(null)

  useEffect(() => {
    fetchProduct(params.id).then(setProduct)
  }, [params.id])

  if (!product) return <div>Loading...</div>

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
    </div>
  )
}
```

## Client Component Best Practices

### ✅ DO: Use 'use client' Sparingly
Only add `'use client'` when you actually need client-side interactivity:

```typescript
// Good: Only client when needed
'use client'

import { useState } from 'react'

export function InteractiveCounter() {
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  )
}
```

### ✅ DO: Minimize Client Component Size
Keep Client Components small and focused:

```typescript
// Good: Small, focused Client Component
'use client'

import { useState } from 'react'

export function LikeButton({ initialLikes }: { initialLikes: number }) {
  const [likes, setLikes] = useState(initialLikes)
  const [isLoading, setIsLoading] = useState(false)

  const handleLike = async () => {
    if (isLoading) return

    setIsLoading(true)
    try {
      await likePost()
      setLikes(likes + 1)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button
      onClick={handleLike}
      disabled={isLoading}
      className={isLoading ? 'opacity-50' : ''}
    >
      👍 {likes} {isLoading ? '(Saving...)' : ''}
    </button>
  )
}
```

## Data Fetching Best Practices

### ✅ DO: Use Appropriate Cache Strategies
Choose the right caching strategy for your data:

```typescript
// Static data (cached until build or manual revalidation)
const staticData = await fetch('https://api.example.com/static-content')

// Dynamic data (fetched on every request)
const dynamicData = await fetch('https://api.example.com/user-data', {
  cache: 'no-store'
})

// Revalidated data (cached but refreshed periodically)
const trendingData = await fetch('https://api.example.com/trending', {
  next: { revalidate: 3600 } // Revalidate every hour
})
```

### ✅ DO: Handle Errors Gracefully
Always handle potential fetch errors:

```typescript
// Good: Error handling
export default async function DataComponent() {
  let data
  try {
    const response = await fetch('https://api.example.com/data')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    data = await response.json()
  } catch (error) {
    console.error('Failed to fetch data:', error)
    // Render fallback UI
    return <div>Failed to load data</div>
  }

  return <div>{JSON.stringify(data)}</div>
}
```

## Server Actions Best Practices

### ✅ DO: Validate Input in Server Actions
Always validate input in Server Actions since they're exposed to clients:

```typescript
// Good: Input validation
'use server'

export async function createComment(formData: FormData) {
  const content = formData.get('content') as string
  const postId = formData.get('postId') as string

  // Validate input
  if (!content || content.length > 500) {
    return { error: 'Comment must be 1-500 characters' }
  }

  if (!postId) {
    return { error: 'Post ID is required' }
  }

  // Process the action
  const comment = await saveComment({ content, postId })

  revalidatePath(`/posts/${postId}`)
  return { success: true, comment }
}
```

### ✅ DO: Handle Authentication in Server Actions
Check authentication when needed:

```typescript
// Good: Authentication check
'use server'

import { auth } from '@/auth'

export async function updateProfile(formData: FormData) {
  const session = await auth()
  if (!session?.user) {
    return { error: 'Unauthorized' }
  }

  const userId = session.user.id
  const name = formData.get('name') as string

  if (!name) {
    return { error: 'Name is required' }
  }

  const updatedUser = await updateUser(userId, { name })

  revalidatePath('/profile')
  return { success: true, user: updatedUser }
}
```

## Performance Best Practices

### ✅ DO: Use Streaming for Large Data Sets
Break up large data loads with streaming:

```typescript
// Good: Streaming for large datasets
import { Suspense } from 'react'

export default function Dashboard() {
  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Suspense fallback={<CardSkeleton />}>
          <SummaryStats />
        </Suspense>

        <Suspense fallback={<CardSkeleton />}>
          <RecentActivity />
        </Suspense>

        <Suspense fallback={<CardSkeleton />}>
          <PopularItems />
        </Suspense>
      </div>

      <div className="mt-8">
        <Suspense fallback={<TableSkeleton />}>
          <FullDataTable />
        </Suspense>
      </div>
    </div>
  )
}
```

### ✅ DO: Optimize Images
Use Next.js Image component with proper sizing:

```typescript
// Good: Optimized images
import Image from 'next/image'

export function ProductImage({ src, alt, width, height }: {
  src: string;
  alt: string;
  width: number;
  height: number;
}) {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      priority={false} // Only set true for above-the-fold images
      placeholder="blur" // Use blur placeholder for progressive loading
      blurDataURL="data:image/jpeg;base64..." // Optional blur placeholder
    />
  )
}
```

## Common Pitfalls to Avoid

### ❌ Pitfall: Forgetting 'use client' When Needed
```typescript
// This will cause an error if you use client-side hooks
import { useState } from 'react' // Error: Cannot use useState in Server Component

export default function Counter() {
  const [count, setCount] = useState(0) // This won't work without 'use client'

  return <button onClick={() => setCount(count + 1)}>{count}</button>
}
```

### ❌ Pitfall: Trying to Import Server Code in Client Components
```typescript
// client-component.tsx
'use client'

// This will cause an error
import { connectToDatabase } from './server-utils' // Error: Cannot import server code in client

export function MyComponent() {
  // This would try to run database connection in browser
  const db = connectToDatabase() // Won't work in browser
}
```

### ❌ Pitfall: Not Handling Async Components Properly
```typescript
// This will cause hydration errors
export default function Page() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/data').then(res => res.json()).then(setData)
  }, [])

  // This creates a mismatch between server and client
  return <div>{data?.name || 'Loading...'}</div>
}
```

### ✅ Solution: Use Server Components for Initial Data
```typescript
// This avoids hydration issues
export default async function Page() {
  const data = await fetchData() // Server fetch

  return <div>{data.name}</div>
}
```

## Security Considerations

### ✅ DO: Sanitize User Input
Always sanitize user input before displaying or storing:

```typescript
import DOMPurify from 'isomorphic-dompurify'

'use server'

export async function saveArticle(formData: FormData) {
  const content = formData.get('content') as string

  // Sanitize HTML content
  const sanitizedContent = DOMPurify.sanitize(content)

  return await saveToDatabase(sanitizedContent)
}
```

### ✅ DO: Use CSRF Protection
For forms that modify data, consider CSRF protection:

```typescript
// This is handled automatically by Next.js Server Actions
// but you can add additional validation
'use server'

export async function deleteItem(formData: FormData) {
  // Server Actions provide CSRF protection by default
  const itemId = formData.get('itemId') as string
  const session = await auth()

  if (!session?.user) {
    return { error: 'Unauthorized' }
  }

  // Additional validation can be added here
  await deleteFromDatabase(itemId)
  revalidatePath('/items')

  return { success: true }
}
```