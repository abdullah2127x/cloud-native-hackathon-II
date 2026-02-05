# ChatKit Client Tools

## What are Client Tools?

Client tools are frontend-side functions that ChatKit AI can invoke. Unlike MCP tools (server-side), client tools execute in the user's browser and can:
- Navigate (open links, change pages)
- Modify DOM (update UI, show modals)
- Access browser APIs (localStorage, clipboard)
- Trigger local actions (send emails via backend, update UI state)

**Key difference from MCP tools**:
- **MCP tools**: Server-side, stateless, manage data (create tasks, fetch lists)
- **Client tools**: Frontend-side, stateful, trigger actions (open link, show toast)

---

## Implementing Client Tools

### Step 1: Define Tool Types

```typescript
// Define all possible client tools as a discriminated union
type ClientToolCall =
  | {
      name: 'open_url';
      params: { url: string; target?: '_blank' | '_self' };
    }
  | {
      name: 'copy_to_clipboard';
      params: { text: string };
    }
  | {
      name: 'show_notification';
      params: { title: string; message: string; type: 'success' | 'error' | 'info' };
    }
  | {
      name: 'navigate_to';
      params: { path: string };
    }
  | {
      name: 'scroll_to';
      params: { elementId: string };
    }
  | {
      name: 'update_ui_state';
      params: { key: string; value: unknown };
    };
```

### Step 2: Implement Handler

```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useRouter } from 'next/navigation';
import { useToast } from '@/lib/toast';

export function ChatWithClientTools() {
  const router = useRouter();
  const toast = useToast();

  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        const res = await fetch('/api/chatkit/start', { method: 'POST' });
        return (await res.json()).client_secret;
      },
    },

    // Handle client tool calls
    onClientTool: async (toolCall) => {
      const call = toolCall as ClientToolCall;

      try {
        switch (call.name) {
          case 'open_url':
            window.open(call.params.url, call.params.target || '_blank');
            return { success: true, message: 'URL opened' };

          case 'copy_to_clipboard':
            await navigator.clipboard.writeText(call.params.text);
            return { success: true, message: 'Copied to clipboard' };

          case 'show_notification':
            toast[call.params.type](call.params.title, call.params.message);
            return { success: true };

          case 'navigate_to':
            router.push(call.params.path);
            return { success: true, message: `Navigated to ${call.params.path}` };

          case 'scroll_to':
            const element = document.getElementById(call.params.elementId);
            element?.scrollIntoView({ behavior: 'smooth' });
            return { success: true };

          case 'update_ui_state':
            // Update React state or global state
            dispatch({ type: 'UPDATE_STATE', payload: call.params });
            return { success: true };

          default:
            throw new Error(`Unknown tool: ${call.name}`);
        }
      } catch (error) {
        return {
          success: false,
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    },
  });

  return <ChatKit control={control} className="h-[600px] w-[400px]" />;
}
```

---

## Common Client Tool Patterns

### Pattern 1: Navigation & Links

```typescript
type NavTool =
  | {
      name: 'open_url';
      params: { url: string; label: string };
    }
  | {
      name: 'navigate_to';
      params: { path: string; label: string };
    };

onClientTool: async (toolCall) => {
  const call = toolCall as NavTool;

  if (call.name === 'open_url') {
    window.open(call.params.url, '_blank', 'noopener');
    return { opened: true, url: call.params.url };
  }

  if (call.name === 'navigate_to') {
    router.push(call.params.path);
    return { navigated: true, path: call.params.path };
  }
}
```

### Pattern 2: Notifications & Feedback

```typescript
type FeedbackTool =
  | {
      name: 'show_toast';
      params: { message: string; type: 'success' | 'error' | 'info' | 'warning' };
    }
  | {
      name: 'show_modal';
      params: { title: string; content: string; action?: string };
    };

onClientTool: async (toolCall) => {
  const call = toolCall as FeedbackTool;

  if (call.name === 'show_toast') {
    toast[call.params.type](call.params.message);
    return { shown: true };
  }

  if (call.name === 'show_modal') {
    setModalContent({
      title: call.params.title,
      content: call.params.content,
    });
    setShowModal(true);
    return { shown: true };
  }
}
```

### Pattern 3: Data Operations

```typescript
type DataTool =
  | {
      name: 'update_task';
      params: { taskId: number; status: string };
    }
  | {
      name: 'refresh_tasks';
      params: { userId: string };
    };

onClientTool: async (toolCall) => {
  const call = toolCall as DataTool;

  if (call.name === 'update_task') {
    // Call backend API to update task
    const res = await fetch(`/api/tasks/${call.params.taskId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status: call.params.status }),
      headers: { 'Content-Type': 'application/json' },
    });
    return { updated: true, taskId: call.params.taskId };
  }

  if (call.name === 'refresh_tasks') {
    // Refetch tasks from backend
    const res = await fetch(`/api/tasks?userId=${call.params.userId}`);
    const tasks = await res.json();
    dispatch({ type: 'SET_TASKS', payload: tasks });
    return { refreshed: true, count: tasks.length };
  }
}
```

### Pattern 4: Clipboard & Text Operations

```typescript
type TextTool =
  | {
      name: 'copy_to_clipboard';
      params: { text: string; label: string };
    }
  | {
      name: 'generate_code_snippet';
      params: { language: string; code: string };
    };

onClientTool: async (toolCall) => {
  const call = toolCall as TextTool;

  if (call.name === 'copy_to_clipboard') {
    try {
      await navigator.clipboard.writeText(call.params.text);
      toast.success(`Copied: ${call.params.label}`);
      return { copied: true, length: call.params.text.length };
    } catch (e) {
      return { copied: false, error: 'Copy failed' };
    }
  }

  if (call.name === 'generate_code_snippet') {
    setCodeSnippet({
      language: call.params.language,
      code: call.params.code,
    });
    return { generated: true, language: call.params.language };
  }
}
```

---

## Error Handling in Client Tools

```typescript
onClientTool: async (toolCall) => {
  const call = toolCall as ClientToolCall;

  try {
    // Execute tool
    const result = await executeClientTool(call);

    // Return success
    return {
      success: true,
      result,
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    // Log error
    console.error('Client tool error:', {
      tool: call.name,
      error: error instanceof Error ? error.message : 'Unknown',
    });

    // Return error response (AI will see this)
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Operation failed',
      tool_name: call.name,
    };
  }
}
```

---

## Client Tools vs MCP Tools

### Client Tools (Frontend)
```
User: "Open the documentation"
↓
ChatKit AI receives tool call
↓
onClientTool handler: window.open('https://docs.com')
↓
Link opens in browser
```

### MCP Tools (Backend/Server)
```
User: "Create a task to buy groceries"
↓
ChatKit sends to backend (/api/chat)
↓
Backend AI agent invokes add_task MCP tool
↓
MCP tool calls database: INSERT INTO tasks...
↓
Database updated, AI responds
```

### When to use which?

| Need | Tool Type | Why |
|------|-----------|-----|
| Open links, navigate | Client | Browser control, instant |
| Show notifications | Client | UI updates, user feedback |
| Create/modify data | MCP | Persistent, secure, auditable |
| Fetch data | MCP | Consistency, server authority |
| Copy to clipboard | Client | Browser API only |
| Backend operations | MCP | Data integrity, security |

---

## Security Considerations

### ❌ Avoid
- Client tools that modify critical data directly (always go through backend)
- Tools that expose secrets (API keys, tokens)
- Tools that bypass authentication
- Unvalidated tool parameters

### ✅ Do This
- Always validate tool parameters on frontend before execution
- Route data operations through secured backend APIs
- Require authentication before sensitive operations
- Log tool invocations for audit trail
- Handle tool failures gracefully

### Validation Example
```typescript
const validateClientTool = (toolCall: unknown): ClientToolCall => {
  // Validate tool call structure
  if (!toolCall || typeof toolCall !== 'object') {
    throw new Error('Invalid tool call');
  }

  const call = toolCall as any;

  if (!call.name || typeof call.name !== 'string') {
    throw new Error('Missing or invalid tool name');
  }

  if (!call.params || typeof call.params !== 'object') {
    throw new Error('Missing or invalid parameters');
  }

  // Validate specific tool parameters
  if (call.name === 'open_url' && !isValidUrl(call.params.url)) {
    throw new Error('Invalid URL');
  }

  return call as ClientToolCall;
};

onClientTool: async (toolCall) => {
  try {
    const validatedCall = validateClientTool(toolCall);
    // Execute validated call...
  } catch (e) {
    return { success: false, error: (e as Error).message };
  }
}
```

---

## Example: Task Management Client Tools

```typescript
type TaskClientTool =
  | {
      name: 'mark_task_complete';
      params: { taskId: number };
    }
  | {
      name: 'show_task_details';
      params: { taskId: number };
    }
  | {
      name: 'refresh_task_list';
      params: {};
    };

export function ChatWithTaskTools() {
  const [tasks, setTasks] = useState<Task[]>([]);

  const { control } = useChatKit({
    api: { /* ... */ },

    onClientTool: async (toolCall) => {
      const call = toolCall as TaskClientTool;

      switch (call.name) {
        case 'mark_task_complete':
          // Call backend to update
          const updateRes = await fetch(
            `/api/tasks/${call.params.taskId}/complete`,
            { method: 'PATCH' }
          );
          const updatedTask = await updateRes.json();

          // Update local state
          setTasks(tasks.map(t =>
            t.id === updatedTask.id ? updatedTask : t
          ));

          return { completed: true, taskId: call.params.taskId };

        case 'show_task_details':
          const task = tasks.find(t => t.id === call.params.taskId);
          setSelectedTask(task);
          return { shown: true, task };

        case 'refresh_task_list':
          const listRes = await fetch('/api/tasks');
          const refreshedTasks = await listRes.json();
          setTasks(refreshedTasks);
          return { refreshed: true, count: refreshedTasks.length };

        default:
          return { success: false, error: 'Unknown tool' };
      }
    },
  });

  return (
    <div className="grid grid-cols-2 gap-4">
      <div className="h-[600px]">
        <ChatKit control={control} className="h-full w-full" />
      </div>
      <div className="space-y-4">
        <div>Tasks ({tasks.length})</div>
        {tasks.map(task => (
          <div key={task.id} className="p-2 border rounded">
            <h3>{task.title}</h3>
            <p className="text-sm text-gray-600">{task.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

