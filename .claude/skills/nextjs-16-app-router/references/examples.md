# Next.js 16 App Router - Additional Examples and Patterns

## Advanced Data Fetching Patterns

### Parallel Data Fetching

When you need to fetch multiple data sources simultaneously:

```typescript
// app/dashboard/page.tsx
import { fetchSales, fetchOrders, fetchCustomers } from '@/lib/dashboard'

// All functions execute in parallel automatically
export default async function Dashboard() {
  const [sales, orders, customers] = await Promise.all([
    fetchSales(),
    fetchOrders(),
    fetchCustomers()
  ])

  return (
    <div>
      <SalesCard data={sales} />
      <OrdersCard data={orders} />
      <CustomersCard data={customers} />
    </div>
  )
}
```

### Streaming with Suspense

For better perceived performance with slow data:

```typescript
// app/streaming-example/page.tsx
import { Suspense } from 'react'
import { SalesReport } from './components/sales-report'
import { OrdersSummary } from './components/orders-summary'

export default function StreamingPage() {
  return (
    <div>
      <header>
        <h1>Dashboard</h1>
      </header>

      <div className="grid grid-cols-2 gap-4">
        <Suspense fallback={<div>Loading sales report...</div>}>
          <SalesReport />
        </Suspense>

        <Suspense fallback={<div>Loading orders summary...</div>}>
          <OrdersSummary />
        </Suspense>
      </div>
    </div>
  )
}
```

```typescript
// app/streaming-example/components/sales-report.tsx
// This component might take longer to load
export async function SalesReport() {
  const data = await fetchSlowSalesData()

  return (
    <div className="border p-4">
      <h2>Sales Report</h2>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  )
}
```

## Advanced Server Actions

### Server Action with Zod Validation

```typescript
// app/actions.ts
'use server'

import { z } from 'zod'
import { revalidatePath } from 'next/cache'

const ContactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
})

export type FormState = {
  errors?: {
    name?: string[]
    email?: string[]
    message?: string[]
  }
  message?: string
}

export async function contactUs(prevState: FormState, formData: FormData): Promise<FormState> {
  const validatedFields = ContactSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  })

  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: 'Missing Fields. Failed to create contact.',
    }
  }

  const { name, email, message } = validatedFields.data

  try {
    // Save to database or send email
    await saveContactMessage({ name, email, message })
  } catch (error) {
    return {
      message: 'Database Error: Failed to save contact message.',
    }
  }

  revalidatePath('/contact')
  return { message: 'Successfully submitted contact form!' }
}
```

### Server Action with Authentication Check

```typescript
// app/actions.ts
'use server'

import { auth } from '@/auth'
import { revalidatePath } from 'next/cache'

export async function deletePost(postId: string) {
  // Check if user is authenticated
  const session = await auth()
  if (!session) {
    return { error: 'Unauthorized' }
  }

  // Check if user owns the post
  const post = await getPostById(postId)
  if (post.userId !== session.user.id) {
    return { error: 'Forbidden' }
  }

  try {
    await deletePostFromDB(postId)
    revalidatePath('/posts')
    return { success: true }
  } catch (error) {
    return { error: 'Failed to delete post' }
  }
}
```

## Advanced Route Handler Patterns

### Middleware Integration with Route Handlers

```typescript
// app/api/protected/route.ts
import { auth } from '@/auth'

export async function GET(request: Request) {
  // Check authentication
  const session = await auth()
  if (!session) {
    return new Response('Unauthorized', { status: 401 })
  }

  // Return protected data
  return Response.json({ message: 'Protected data', user: session.user })
}
```

### File Upload with Route Handlers

```typescript
// app/api/upload/route.ts
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json(
        { error: 'No file uploaded' },
        { status: 400 }
      )
    }

    // Process file upload
    const buffer = Buffer.from(await file.arrayBuffer())
    const fileName = `${Date.now()}-${file.name}`

    // Save to cloud storage
    await saveToCloudStorage(buffer, fileName)

    return NextResponse.json({
      message: 'File uploaded successfully',
      fileName,
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to upload file' },
      { status: 500 }
    )
  }
}
```

## Advanced Metadata Patterns

### Dynamic Metadata with Search Parameters

```typescript
// app/search/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; category?: string }>
}): Promise<Metadata> {
  const { q = '', category = '' } = await searchParams
  const query = q || category

  return {
    title: query ? `Search results for "${query}"` : 'Search',
    description: query
      ? `Search results for ${query} in our catalog`
      : 'Search our entire product catalog',
  }
}
```

### Metadata with Internationalization

```typescript
// app/[locale]/products/[id]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({
  params,
}: {
  params: { locale: string; id: string }
}): Promise<Metadata> {
  const product = await getProduct(params.id, params.locale)

  return {
    title: product.title,
    description: product.description,
    alternates: {
      canonical: `/en/products/${params.id}`,
      languages: {
        en: `/en/products/${params.id}`,
        es: `/es/products/${params.id}`,
        fr: `/fr/products/${params.id}`,
      },
    },
  }
}
```

## Performance Optimization Patterns

### Lazy Loading Client Components

```typescript
// app/products/[id]/page.tsx
import { Suspense } from 'react'
import dynamic from 'next/dynamic'

// Dynamically import heavy client components
const ProductReviews = dynamic(() => import('./components/product-reviews'), {
  loading: () => <p>Loading reviews...</p>,
  ssr: false, // Only render on client if needed
})

const ProductRecommendations = dynamic(
  () => import('./components/product-recommendations'),
  {
    loading: () => <p>Loading recommendations...</p>,
  }
)

export default async function ProductPage({ params }: { params: { id: string } }) {
  const product = await getProduct(params.id)

  return (
    <div>
      <ProductDetails product={product} />

      <Suspense fallback={<div>Loading reviews...</div>}>
        <ProductReviews productId={params.id} />
      </Suspense>

      <Suspense fallback={<div>Loading recommendations...</div>}>
        <ProductRecommendations productId={params.id} />
      </Suspense>
    </div>
  )
}
```

### Conditional Server/Client Rendering

```typescript
// Sometimes you need to conditionally render based on server data
// app/user-profile/page.tsx
import { getServerSession } from 'next-auth'
import { UserProfileClient } from './components/user-profile-client'

export default async function UserProfilePage() {
  const session = await getServerSession()

  // Pass server data to client component
  return <UserProfileClient session={session} />
}
```

```typescript
// app/user-profile/components/user-profile-client.tsx
'use client'

import { useEffect, useState } from 'react'

interface Session {
  user?: {
    name?: string | null
    email?: string | null
    image?: string | null
  }
}

export function UserProfileClient({ session }: { session: Session | null }) {
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  if (!isClient || !session?.user) {
    return <div>Loading...</div>
  }

  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  )
}
```