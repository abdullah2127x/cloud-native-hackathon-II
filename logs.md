PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\frontend> npm run build

> frontend@0.1.0 build
> next build

▲ Next.js 16.1.3 (Turbopack)
- Environments: .env.local, .env

  Creating an optimized production build ...
✓ Compiled successfully in 34.9s
  Running TypeScript  ..Failed to compile.

./src/components/chat/MessageList.tsx:73:7
Type error: Type '{ ref: RefObject<VirtuosoHandle | null>; data: Message[]; initialTopMostItemIndex: number; followOutput: "smooth"; className: string; itemContent: (index: number, message: Message) => Element; footer: () => Element | null; }' is not assignable to type 'IntrinsicAttributes & VirtuosoProps<Message, any> & { ref?: Ref<VirtuosoHandle> | undefined; }'.
  Property 'footer' does not exist on type 'IntrinsicAttributes & VirtuosoProps<Message, any> & { ref?: Ref<VirtuosoHandle> | undefined; }'. 

  71 |         <MessageBubble key={message.id} message={message} />
  72 |       )}
> 73 |       footer={() =>
     |       ^
  74 |         isLoading ? (
  75 |           <div className="flex w-full px-4 py-3">
  76 |             <div className="flex items-center gap-1 rounded-lg bg-muted px-4 py-2">    
Next.js build worker exited with code: 1 and signal: null
PS D:\AbdullahQureshi\workspace\Hackathon-2025\hackathon-2\todo-in-memory-console-app\frontend>