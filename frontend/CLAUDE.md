# Frontend Development Guide

This guide defines development standards for the Next.js frontend application.

## Code Generation Standards

### TypeScript Requirements
- **Strict Mode**: Always use TypeScript strict mode (enabled in tsconfig.json)
- **Explicit Types**: Never use `any` type - use `unknown` for truly dynamic data, then narrow with type guards
- **Type Imports**: Use `import type` for type-only imports
- **Return Types**: Always specify return types for functions
- **Null Safety**: Handle null/undefined explicitly, avoid `!` assertions unless absolutely necessary

### React Patterns
- **Functional Components**: Use functional components exclusively, never class components
- **Props Typing**: Define explicit interface/type for all component props
- **Hooks**: Follow hooks rules - only call at top level, only in React functions
- **Event Handlers**: Type event handlers explicitly (e.g., `React.MouseEvent<HTMLButtonElement>`)
- **State Types**: Type `useState` explicitly: `useState<Type>(initialValue)`

### Tailwind CSS Usage
- **Utility-First**: Use Tailwind utility classes, avoid custom CSS unless necessary
- **Responsive Design**: Mobile-first approach - use responsive prefixes (sm:, md:, lg:)
- **Dark Mode**: Prepare for dark mode support using Tailwind's dark: prefix
- **Component Composition**: Compose complex styles using className utilities

### React Hook Form + Zod Integration
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// 1. Define Zod schema
const schema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Minimum 8 characters'),
});

type FormData = z.infer<typeof schema>;

// 2. Use in component
const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(schema),
});

// 3. Handle submit
const onSubmit = (data: FormData) => {
  // data is type-safe and validated
};
```

## File Organization

### Directory Structure
```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Route groups for auth pages
│   ├── dashboard/         # Protected dashboard area
│   └── api/               # API routes
├── components/            # React components
│   ├── auth/             # Authentication components
│   ├── tasks/            # Task management components
│   └── ui/               # Reusable UI components
├── hooks/                # Custom React hooks
├── lib/                  # Library code
│   ├── validations/      # Zod schemas
│   ├── constants/        # App constants
│   └── utils/            # Utility functions
├── middleware/           # Request/response interceptors
├── providers/            # React Context providers
├── styles/              # Global styles
├── types/               # TypeScript type definitions
└── tests/               # Test configuration and mocks
```

### Naming Conventions
- **Components**: PascalCase, descriptive names (e.g., `SignInForm.tsx`, `TaskList.tsx`)
- **Hooks**: Prefix with `use`, verb-based (e.g., `useTasks.ts`, `useNetworkError.ts`)
- **Files**: Match component name (e.g., `TaskItem.tsx` exports `TaskItem`)
- **Test Files**: Co-located with source, `.test.tsx` suffix (e.g., `TaskItem.test.tsx`)

### Import Order
1. React and Next.js imports
2. Third-party library imports
3. Local component imports
4. Hook imports
5. Type imports
6. Utility/constant imports

```typescript
// Good example
import React from 'react';
import Link from 'next/link';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { Button } from '@/components/ui/Button';
import { useTasks } from '@/hooks/useTasks';

import type { Task } from '@/types';
import { API_ENDPOINTS } from '@/lib/constants/api';
```

## Testing Requirements

### Coverage Target
- **Minimum**: 70% coverage for all files
- **Measured By**: Jest coverage reports
- **Enforced**: Jest config (`coverageThreshold`)

### Testing Philosophy
- **Test User Behavior**: Test what users see and do, not implementation details
- **Avoid Implementation Testing**: Don't test internal state or private methods
- **User-Centric**: Use `screen.getByRole`, `screen.getByLabelText` over test IDs

### MSW Setup for API Mocking
```typescript
// src/tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/api/todos', () => {
    return HttpResponse.json([
      { id: '1', title: 'Test Task', completed: false },
    ]);
  }),
];

// src/tests/setup.ts
import '@testing-library/jest-dom';
import { server } from './mocks/server';

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Better Auth Mocking
```typescript
// Mock Better Auth client in tests
jest.mock('@/lib/auth-client', () => ({
  authClient: {
    getSession: jest.fn(() => Promise.resolve({
      user: { id: 'user-1', email: 'test@example.com' },
      accessToken: 'mock-token',
    })),
    signIn: jest.fn(),
    signOut: jest.fn(),
  },
}));
```

### Component Testing Pattern
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { TaskForm } from './TaskForm';

describe('TaskForm', () => {
  it('submits valid task data', async () => {
    const onSubmit = jest.fn();
    const user = userEvent.setup();

    render(<TaskForm onSubmit={onSubmit} />);

    await user.type(screen.getByLabelText(/title/i), 'New Task');
    await user.click(screen.getByRole('button', { name: /create/i }));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        title: 'New Task',
        description: '',
      });
    });
  });
});
```

## Error Handling Patterns

### Network Errors
Use the `useNetworkError` hook for consistent error handling:
```typescript
const { handleError, retry } = useNetworkError();

try {
  await apiCall();
} catch (error) {
  handleError(error); // Shows toast, logs error
}
```

### Form Validation
Zod schemas handle validation, React Hook Form displays errors:
```typescript
{errors.email && (
  <span className="text-sm text-red-600">{errors.email.message}</span>
)}
```

### API Error Responses
Handle specific HTTP status codes:
- **401**: Redirect to sign-in
- **422**: Show validation errors
- **500**: Show generic error message, log details

### Session Expiry Handling
When API returns 401 during edit:
1. Save draft to localStorage
2. Redirect to sign-in with returnUrl
3. After sign-in, restore draft and return to page

```typescript
// In api interceptor
if (error.response?.status === 401) {
  // Save current state
  localStorage.setItem('draft', JSON.stringify(currentData));
  // Redirect with return URL
  window.location.href = `/sign-in?returnUrl=${window.location.pathname}`;
}
```

## Performance Guidelines

### Code Splitting
- **Route-based**: Automatic with Next.js App Router
- **Component-based**: Use dynamic imports for modals and heavy components
```typescript
const DeleteConfirmDialog = dynamic(() => import('./DeleteConfirmDialog'));
```

### React Optimization
- **useMemo**: Memoize expensive calculations
- **useCallback**: Memoize event handlers passed to child components
- **React.memo**: Memoize components that receive same props frequently

### API Optimization
- **Debounce**: Debounce search/filter inputs (300ms)
- **Request Cancellation**: Cancel pending requests on unmount
- **Optimistic Updates**: Update UI immediately, rollback on error

## Security Best Practices

### Input Validation
- **Always Validate**: Use Zod schemas for all user input
- **Server-side Too**: Never rely solely on client validation

### XSS Prevention
- **Never Use**: `dangerouslySetInnerHTML` unless absolutely necessary
- **Sanitize**: If HTML must be rendered, use DOMPurify

### JWT Handling
- **Memory Only**: JWT tokens in memory, not localStorage
- **HTTP-only Cookies**: Better Auth uses HTTP-only cookies
- **Automatic Refresh**: Better Auth handles token refresh

### HTTPS Enforcement
- **Production**: Always use HTTPS in production
- **Development**: HTTP OK for localhost only

## Common Patterns

### Creating a New Component
1. Create file: `src/components/<category>/<ComponentName>.tsx`
2. Define props interface
3. Implement component with TypeScript strict typing
4. Create test file: `<ComponentName>.test.tsx`
5. Export from component file

### Adding a New API Endpoint
1. Define Zod schema in `src/lib/validations/`
2. Add endpoint to `src/lib/constants/api.ts`
3. Create/update hook in `src/hooks/`
4. Add MSW handler in `src/tests/mocks/handlers.ts`
5. Write integration test

### Adding a Form
1. Define Zod schema for validation
2. Infer TypeScript type from schema
3. Use React Hook Form with zodResolver
4. Render form with field errors
5. Handle submission with type-safe data

## What NOT to Do

### File Creation
- ❌ Don't create files unless directly requested or necessary
- ❌ Don't create documentation files (*.md) proactively
- ✅ Prefer editing existing files

### Code Quality
- ❌ Don't add comments to unchanged code
- ❌ Don't refactor unrelated code
- ❌ Don't use `any` type
- ❌ Don't bypass validation
- ❌ Don't ignore TypeScript errors

### Testing
- ❌ Don't test implementation details
- ❌ Don't use `getByTestId` unless no semantic alternative
- ❌ Don't mock what you don't own (except external APIs)

### Security
- ❌ Don't store sensitive data in localStorage
- ❌ Don't trust client-side validation alone
- ❌ Don't expose API keys in frontend code

## Testing Scripts

Add these to package.json:
```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --ci --coverage --maxWorkers=2"
  }
}
```

## Quick Reference

### File Paths by Feature
- **Auth**: `src/components/auth/`, `src/lib/validations/auth.ts`
- **Tasks**: `src/components/tasks/`, `src/hooks/useTasks.ts`
- **UI Components**: `src/components/ui/`
- **API Client**: `src/middleware/api-interceptor.ts`
- **Constants**: `src/lib/constants/`
- **Types**: `src/types/index.ts`

### Key Libraries
- **Forms**: react-hook-form + @hookform/resolvers/zod
- **Validation**: zod
- **Auth**: better-auth
- **Styling**: tailwindcss
- **Testing**: jest + @testing-library/react + msw
- **HTTP**: axios (in api-interceptor)

---

**Version**: 1.0.0
**Created**: 2026-01-17
**Updated**: 2026-01-17
**Related**: See root CLAUDE.md for project-wide standards
