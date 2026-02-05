# ChatKit Event Handling Patterns

## Event System Overview

ChatKit emits events throughout the chat lifecycle. Events enable:
- Analytics and monitoring
- Error tracking
- Performance measurement
- State synchronization
- Custom logging

---

## Core Events

### onReady
**When**: ChatKit component initialized and ready to receive messages

```typescript
const { control } = useChatKit({
  api: { ... },
  onReady: () => {
    console.log('ChatKit is ready');
    analytics.track('chatkit_initialized');
  },
});
```

**Use cases**:
- Set loading state to false
- Enable chat input
- Log initialization event
- Trigger welcome message

---

### onError
**When**: Error occurs (network, API, permissions)

```typescript
const { control } = useChatKit({
  api: { ... },
  onError: ({ error }) => {
    console.error('ChatKit error:', error);

    // Send to error tracking service
    Sentry.captureException(error, {
      tags: { component: 'chatkit' },
      extra: { message: error.message },
    });

    // Show user-friendly error
    toast.error('Chat error. Please try again.');
  },
});
```

**Error types**:
- Network errors (connection failed)
- API errors (rate limit, invalid token)
- Validation errors (malformed request)
- Permission errors (unauthorized)

**Best practices**:
- Always log to error tracking service
- Show user-friendly message (not technical details)
- Implement retry logic
- Don't let errors crash the app

---

### onResponseStart
**When**: AI begins generating response

```typescript
const [isLoading, setIsLoading] = useState(false);

const { control } = useChatKit({
  api: { ... },
  onResponseStart: () => {
    setIsLoading(true);
    const startTime = Date.now();
  },
});
```

**Use cases**:
- Show loading indicator
- Disable input temporarily
- Measure response time (start timer)
- Clear error state

---

### onResponseEnd
**When**: AI finishes generating response

```typescript
let responseStartTime = 0;

const { control } = useChatKit({
  api: { ... },
  onResponseStart: () => {
    responseStartTime = Date.now();
  },
  onResponseEnd: () => {
    const responseTime = Date.now() - responseStartTime;
    setIsLoading(false);

    // Track performance
    analytics.track('ai_response_time', {
      duration_ms: responseTime,
      timestamp: new Date().toISOString(),
    });
  },
});
```

**Use cases**:
- Hide loading indicator
- Re-enable input
- Measure latency
- Auto-scroll to latest message

---

### onThreadChange
**When**: User switches conversation (thread ID changes)

```typescript
const { control } = useChatKit({
  api: { ... },
  onThreadChange: ({ threadId }) => {
    console.log('Thread changed to:', threadId);

    // Track in analytics
    analytics.track('conversation_switched', {
      thread_id: threadId,
      timestamp: new Date().toISOString(),
    });

    // Update UI state
    setCurrentThreadId(threadId);
  },
});
```

**Use cases**:
- Track conversation switches
- Update sidebar/navigation
- Save current thread ID
- Sync with database

---

### onThreadLoadStart / onThreadLoadEnd
**When**: Loading existing conversation thread

```typescript
const { control } = useChatKit({
  api: { ... },
  onThreadLoadStart: ({ threadId }) => {
    console.log('Loading thread:', threadId);
    setIsLoadingThread(true);
  },
  onThreadLoadEnd: ({ threadId }) => {
    console.log('Thread loaded:', threadId);
    setIsLoadingThread(false);
  },
});
```

**Use cases**:
- Show loading state for history
- Track thread load performance
- Measure conversation history size impact

---

### onLog
**When**: Detailed logging events (most flexible)

```typescript
const { control } = useChatKit({
  api: { ... },
  onLog: ({ name, data }) => {
    console.log('ChatKit log:', name, data);

    // Track specific events
    if (name === 'message.send') {
      analytics.track('message_sent', {
        message_length: data.content?.length || 0,
        timestamp: new Date().toISOString(),
      });
    }

    if (name === 'tool.called') {
      analytics.track('tool_invoked', {
        tool_name: data.tool_name,
        timestamp: new Date().toISOString(),
      });
    }

    if (name === 'thread.created') {
      analytics.track('new_conversation', {
        thread_id: data.threadId,
        timestamp: new Date().toISOString(),
      });
    }
  },
});
```

**Common log events**:
- `message.send` - User sent message
- `tool.called` - Client tool was invoked
- `thread.created` - New conversation started
- `thread.loaded` - Existing conversation opened
- `error` - Error occurred

---

## Complete Event Handler Example

```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useState, useRef } from 'react';
import { useAnalytics } from '@/lib/analytics';
import { useSentryClient } from '@/lib/sentry';

export function ChatWithFullEventHandling() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const responseStartTime = useRef(0);

  const analytics = useAnalytics();
  const sentry = useSentryClient();

  const { control } = useChatKit({
    api: {
      async getClientSecret() {
        const res = await fetch('/api/chatkit/start', { method: 'POST' });
        return (await res.json()).client_secret;
      },
    },

    // Component ready
    onReady: () => {
      console.log('ChatKit is ready');
      analytics.track('chatkit_ready', {
        timestamp: new Date().toISOString(),
      });
    },

    // Error handling
    onError: ({ error: chatError }) => {
      console.error('ChatKit error:', chatError);
      setError(chatError.message);

      sentry.captureException(chatError, {
        tags: { component: 'chatkit' },
        level: 'error',
      });

      // Optionally notify user
      setTimeout(() => setError(null), 5000);
    },

    // Response timing
    onResponseStart: () => {
      setIsLoading(true);
      setError(null);
      responseStartTime.current = Date.now();
    },

    onResponseEnd: () => {
      setIsLoading(false);
      const duration = Date.now() - responseStartTime.current;

      analytics.track('ai_response_complete', {
        duration_ms: duration,
        timestamp: new Date().toISOString(),
      });
    },

    // Conversation tracking
    onThreadChange: ({ threadId }) => {
      analytics.track('conversation_switched', {
        thread_id: threadId,
        timestamp: new Date().toISOString(),
      });
    },

    onThreadLoadStart: ({ threadId }) => {
      console.log('Loading thread:', threadId);
    },

    onThreadLoadEnd: ({ threadId }) => {
      console.log('Thread loaded:', threadId);
      analytics.track('conversation_loaded', {
        thread_id: threadId,
        timestamp: new Date().toISOString(),
      });
    },

    // Detailed logging
    onLog: ({ name, data }) => {
      console.log('[ChatKit]', name, data);

      // Track different event types
      switch (name) {
        case 'message.send':
          analytics.track('user_message', {
            length: data.content?.length || 0,
          });
          break;

        case 'tool.called':
          analytics.track('tool_invoked', {
            tool_name: data.tool_name,
          });
          break;

        case 'thread.created':
          analytics.track('new_conversation_created', {
            thread_id: data.threadId,
          });
          break;

        case 'error':
          sentry.captureMessage(`ChatKit error: ${data.message}`, {
            level: 'warning',
          });
          break;
      }
    },
  });

  return (
    <div className="relative h-[600px]">
      {isLoading && (
        <div className="absolute top-4 left-4 text-sm text-gray-500 z-10">
          AI is thinking...
        </div>
      )}
      {error && (
        <div className="absolute top-4 right-4 bg-red-100 text-red-800 p-3 rounded z-10">
          {error}
        </div>
      )}
      <ChatKit
        control={control}
        className="h-full w-full rounded-lg border"
      />
    </div>
  );
}
```

---

## Analytics Integration Patterns

### Pattern 1: Basic Metrics

```typescript
// Track key metrics
const metrics = {
  conversations_started: 0,
  messages_sent: 0,
  errors_encountered: 0,
  avg_response_time: 0,
};

onLog: ({ name }) => {
  if (name === 'thread.created') metrics.conversations_started++;
  if (name === 'message.send') metrics.messages_sent++;
  if (name === 'error') metrics.errors_encountered++;
}
```

### Pattern 2: User Behavior

```typescript
// Track user journey
const userSession = {
  session_id: generateId(),
  started_at: new Date(),
  conversations: [],
  total_messages: 0,
  total_errors: 0,
};

onThreadChange: ({ threadId }) => {
  userSession.conversations.push({
    thread_id: threadId,
    started_at: new Date(),
  });
},

onLog: ({ name, data }) => {
  if (name === 'message.send') {
    userSession.total_messages++;
  }
}
```

### Pattern 3: Performance Monitoring

```typescript
// Track performance
const performance = {
  chatkit_init_time: 0,
  first_response_time: 0,
  avg_response_time: 0,
  response_times: [],
};

let firstResponse = true;

onReady: () => {
  performance.chatkit_init_time = Date.now() - pageLoadTime;
},

onResponseEnd: () => {
  const responseTime = Date.now() - responseStartTime;
  performance.response_times.push(responseTime);

  if (firstResponse) {
    performance.first_response_time = responseTime;
    firstResponse = false;
  }

  performance.avg_response_time =
    performance.response_times.reduce((a, b) => a + b) /
    performance.response_times.length;
}
```

---

## Error Recovery Strategies

### Automatic Retry
```typescript
const retryWithBackoff = async (fn, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
    }
  }
};

onError: async ({ error }) => {
  // Retry getting client secret
  try {
    const secret = await retryWithBackoff(async () => {
      const res = await fetch('/api/chatkit/start', { method: 'POST' });
      if (!res.ok) throw new Error('Failed to get secret');
      return (await res.json()).client_secret;
    });
    // Reinitialize with new secret
  } catch (e) {
    setError('Unable to recover. Please refresh the page.');
  }
}
```

### Graceful Degradation
```typescript
onError: ({ error }) => {
  if (error.message.includes('rate limit')) {
    setError('Chat is busy. Please try again in a moment.');
  } else if (error.message.includes('unauthorized')) {
    setError('Your session expired. Please refresh.');
  } else {
    setError('Chat error. Please try again.');
  }
}
```

