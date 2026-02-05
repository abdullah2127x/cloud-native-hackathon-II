PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\frontend> npm run build

> frontend@0.1.0 build
> next build

▲ Next.js 16.1.3 (Turbopack)
- Environments: .env.local, .env

  Creating an optimized production build ...
✓ Compiled successfully in 29.8s
  Running TypeScript  ..Failed to compile.

./src/components/chat/ChatContainer.tsx:91:21
Type error: Property 'token' does not exist on type '{ user: { id: string; createdAt: Date; updatedAt: Date; email: string; emailVerified: boolean; name: string; image?: string | null | undefined; }; session: { id: string; createdAt: Date; ... 5 more ...; userAgent?: string | ... 1 more ... | undefined; }; }'.

  89 |   const customFetch = useCallback(      
  90 |     async (input: RequestInfo | URL, init?: RequestInit) => {
> 91 |       if (!session?.token) {
     |                     ^
  92 |         throw new Error('No authentication token available');
  93 |       }
  94 |
Next.js build worker exited with code: 1 and signal: null
PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\frontend>