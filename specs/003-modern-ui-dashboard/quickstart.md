# Quickstart: Modern UI Dashboard Implementation

**Feature**: 003-modern-ui-dashboard
**Date**: 2026-01-29
**Purpose**: Get started building the UI transformation

## Prerequisites

- Node.js 18+ and npm/pnpm installed
- Frontend running: `npm run dev` from `frontend/` directory
- Backend running: `python -m uvicorn main:app --reload` from `backend/` directory
- PostgreSQL (Neon) accessible with environment variables set

## Project Structure

```
frontend/src/
├── app/
│   ├── (landing)/
│   │   ├── page.tsx                    # NEW: Landing page
│   │   ├── layout.tsx                  # NEW: Optional landing layout
│   │   └── components/
│   │       ├── Hero.tsx                # NEW
│   │       ├── Features.tsx            # NEW
│   │       ├── Navigation.tsx          # NEW
│   │       └── Footer.tsx              # NEW
│   ├── (auth)/
│   │   ├── sign-in/page.tsx            # EXISTING: Reuse
│   │   ├── sign-up/page.tsx            # EXISTING: Reuse
│   │   └── components/
│   │       ├── SignInForm.tsx          # EXISTING: Reuse
│   │       └── SignUpForm.tsx          # EXISTING: Reuse
│   ├── dashboard/
│   │   ├── layout.tsx                  # UPDATE: Add sidebar + navigation
│   │   ├── page.tsx                    # MODIFY: Redirect to /dashboard/overview
│   │   ├── overview/page.tsx           # NEW: Overview with stats
│   │   ├── todos/page.tsx              # UPDATE: Reuse existing, enhance with shadcn
│   │   ├── priority/page.tsx           # NEW: Priority organization
│   │   ├── tags/page.tsx               # NEW: Tags organization
│   │   ├── loading.tsx                 # NEW: Route-level loading skeleton
│   │   └── components/
│   │       ├── Sidebar.tsx             # NEW
│   │       ├── DashboardNav.tsx        # NEW
│   │       ├── MobileMenu.tsx          # NEW
│   │       ├── StatCard.tsx            # NEW
│   │       └── ...
│   ├── layout.tsx                      # UPDATE: Keep AuthProvider, <Toaster/>
│   └── page.tsx                        # EXISTING: Keep redirect logic
└── components/
    ├── ui/                             # EXISTING: All shadcn components
    ├── auth/                           # EXISTING: Auth forms
    ├── tasks/                          # EXISTING: Task components
    └── common/                         # NEW: Shared dashboard components
```

## File Modification Summary

### Files to CREATE (New functionality)

**Landing Page Components**:
1. `app/(landing)/page.tsx` - Landing page root
2. `app/(landing)/layout.tsx` - Optional layout wrapper
3. `app/(landing)/components/Hero.tsx` - Hero section
4. `app/(landing)/components/Features.tsx` - Features grid
5. `app/(landing)/components/Navigation.tsx` - Top navigation
6. `app/(landing)/components/Footer.tsx` - Footer section

**Dashboard Pages**:
7. `app/dashboard/overview/page.tsx` - Overview page with stats
8. `app/dashboard/priority/page.tsx` - Priority-based organization
9. `app/dashboard/tags/page.tsx` - Tag-based organization

**Dashboard Components**:
10. `app/dashboard/components/Sidebar.tsx` - Sidebar navigation
11. `app/dashboard/components/DashboardNav.tsx` - Top navigation variant
12. `app/dashboard/components/MobileMenu.tsx` - Mobile hamburger drawer
13. `app/dashboard/components/StatCard.tsx` - Statistics card wrapper
14. `app/dashboard/components/PriorityTabs.tsx` - Priority tabs/sections
15. `app/dashboard/components/TagsList.tsx` - Tags badge list

**Shared Components**:
16. `app/dashboard/components/DashboardHeader.tsx` - Page header with title
17. `app/dashboard/components/EmptyState.tsx` - Generic empty state

**Loading/Styling**:
18. `app/dashboard/loading.tsx` - Route-level loading skeleton

### Files to MODIFY (Existing functionality)

1. `app/layout.tsx` - No changes (already has AuthProvider + Toaster)
2. `app/page.tsx` - No changes (keep existing redirect logic)
3. `app/dashboard/layout.tsx` - ADD sidebar/navigation, keep existing auth guard
4. `app/dashboard/page.tsx` - MODIFY to redirect to `/dashboard/overview`
5. `app/dashboard/todos/page.tsx` - ENHANCE: Wrap existing logic in shadcn Cards/Dialogs

**Component Reuse**:
- `components/auth/SignInForm.tsx` - No changes, reuse in `/sign-in`
- `components/auth/SignUpForm.tsx` - No changes, reuse in `/sign-up`
- `components/tasks/TaskForm.tsx` - REUSE in dashboard todos
- `components/tasks/TaskItem.tsx` - UPDATE styling with shadcn cards
- `hooks/useTasks.ts` - No changes, continue using for data
- `lib/auth-client.ts` - No changes, reuse for session

### Files to DELETE

None - only additions and enhancements

## Implementation Phases

### Phase A: Landing Page (P1)
Estimated components: 4-5 files
Tasks:
1. Create landing page with Hero section (headline, description, CTA buttons)
2. Add Features section with 3-4 feature cards
3. Add responsive Navigation bar
4. Add Footer section
5. Implement responsive layout (mobile, tablet, desktop)

### Phase B: Dashboard Layout (P2)
Estimated components: 4-5 files
Tasks:
1. Create Sidebar with navigation sections
2. Create MobileMenu (Sheet component) for hamburger menu
3. Update dashboard layout.tsx with sidebar + navigation
4. Add user info display in navigation
5. Implement logout functionality

### Phase C: Overview Page (P2)
Estimated components: 2-3 files
Tasks:
1. Create StatCard component
2. Create Overview page with stat cards (total, completed, pending, today)
3. Add loading skeleton
4. Implement responsive stat grid

### Phase D: Priority & Tags Pages (P3)
Estimated components: 3-4 files
Tasks:
1. Create Priority page with tabs/sections
2. Create Tags page with clickable badges
3. Reuse todo cards from existing implementation
4. Implement filtering logic

### Phase E: Todo Page Enhancement (P1)
Estimated components: 1-2 files
Tasks:
1. Refactor existing todos/page.tsx to use shadcn components
2. Wrap todo items in shadcn Card components
3. Use shadcn Dialog/Sheet for Add/Edit forms
4. Use shadcn AlertDialog for delete confirmation
5. Add shadcn Separators between items
6. Keep existing filter/search/sort logic

## Component Dependencies

```
Landing Page
├── Hero (standalone)
├── Features (Card x 3-4)
├── Navigation (Button for CTAs)
└── Footer (standalone)

Dashboard Layout
├── Sidebar
│   ├── NavigationLinks (Button / nav link)
│   ├── UserInfo (avatar, email, logout button)
│   └── Logo
├── MobileMenu (Sheet)
│   └── Same as Sidebar content
└── Main Content
    ├── Page-specific components
    └── Navigation header

Overview Page
└── StatCard x 4 (Card wrapper)

Priority Page
└── Tabs (Tabs component)
    └── TodoCard[] x 3 (one per priority)

Tags Page
└── Badge[] (clickable)
    └── TodoCard[] (filtered by tag)

Todos Page
└── TodoCard[] (Card wrapper)
    ├── Checkbox (completion)
    ├── Dropdown Menu (Edit/Delete)
    ├── Badge (priority, tags)
    └── Dialog (Add/Edit form)

All Pages
└── Toast (Sonner) for notifications
```

## Key shadcn Components to Use

**Essential**:
- `Card` - Todo cards, stat cards, feature cards
- `Button` - All clickable actions
- `Input` - Form inputs (title, search, tag)
- `Textarea` - Todo description
- `Select` - Priority dropdown
- `Checkbox` - Completion toggle
- `Badge` - Priority, tags display
- `Dialog` - Add/Edit todo forms
- `Sheet` - Mobile menu drawer
- `AlertDialog` - Delete confirmation
- `Tabs` - Priority sections
- `Separator` - Visual dividers between todos

**Optional**:
- `Skeleton` - Loading states
- `Spinner` - Button/form loading
- `Progress` - Completion percentage
- `Dropdown-Menu` - Edit/Delete menu

## Data Flow Architecture

```
User Action
    ↓
Component Event Handler
    ↓
useTasks() hook method (existing)
    ↓
Axios + JWT interceptor (existing)
    ↓
Backend API (existing)
    ↓
Database (existing)
    ↓
Response + optimistic UI update
    ↓
Toast notification (Sonner)
    ↓
UI reflects changes
```

## Development Workflow

1. **Start both services**:
   ```bash
   # Terminal 1: Frontend
   cd frontend
   npm run dev

   # Terminal 2: Backend
   cd backend
   python -m uvicorn main:app --reload
   ```

2. **Create components in feature branches** (already on `003-modern-ui-dashboard`)

3. **Test as you go**:
   - Visit landing page: `http://localhost:3000/`
   - Sign in: `http://localhost:3000/sign-in`
   - Dashboard: `http://localhost:3000/dashboard/overview`

4. **Use browser DevTools**:
   - Network tab to monitor API calls
   - Console for errors
   - Device toolbar for responsive testing

5. **Check TypeScript**: Components should be type-safe

## Common Patterns

### Using shadcn Components

```typescript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Title</CardTitle>
      </CardHeader>
      <CardContent>
        <Badge variant="default">Label</Badge>
        <Button onClick={() => {}}>Click me</Button>
      </CardContent>
    </Card>
  );
}
```

### Using Existing Hooks

```typescript
"use client";

import { useTasks } from "@/hooks/useTasks";
import { useSession } from "@/lib/auth-client";

export function MyPage() {
  const { session } = useSession();
  const { tasks, createTask, updateTask } = useTasks();

  // Use existing functionality
}
```

### Protected Route

```typescript
// In dashboard/layout.tsx
"use client";

import { useRouter } from "next/navigation";
import { useSession } from "@/lib/auth-client";

export default function DashboardLayout({ children }) {
  const { session, isLoading } = useSession();
  const router = useRouter();

  if (isLoading) return <LoadingSpinner />;
  if (!session) return router.push("/sign-in");

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

### Responsive Sidebar

```typescript
// Show on desktop, hide on mobile
<aside className="hidden md:flex md:w-64 bg-slate-900 text-white p-6">
  {/* Desktop sidebar */}
</aside>

// Show on mobile as drawer
<Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
  <SheetTrigger className="md:hidden">
    <MenuIcon />
  </SheetTrigger>
  <SheetContent side="left">
    {/* Mobile menu content */}
  </SheetContent>
</Sheet>
```

## Testing the Implementation

### Landing Page
1. Visit `http://localhost:3000/`
2. Verify hero section displays with text and illustration
3. Verify "Get Started" button redirects to `/sign-up`
4. Verify "Sign In" button redirects to `/sign-in`
5. Test responsive: Use DevTools responsive mode to test mobile/tablet/desktop

### Authentication
1. Visit `/sign-up`, create account
2. Verify redirects to `/dashboard/overview`
3. Visit `/sign-in`, sign in with existing account
4. Verify redirects to `/dashboard/overview`

### Dashboard Navigation
1. In dashboard, verify all navigation sections are clickable
2. Verify active section is highlighted
3. Verify logout button signs out and redirects to `/sign-in`
4. Test mobile: Verify hamburger menu works on small screens

### Overview Page
1. Create several todos with different priorities and completion statuses
2. Verify stat cards show correct counts (total, completed, pending, today)
3. Verify loading skeleton displays while data fetches

### Todo Pages
1. **All Todos**: Verify todos display as cards with all details
2. **Priority**: Verify todos grouped by priority
3. **Tags**: Verify todos grouped by tags

### CRUD Operations
1. Create todo: Verify dialog opens, form submits, todo appears in list
2. Edit todo: Verify dialog pre-populates, changes save
3. Delete todo: Verify confirmation dialog appears, deletion works
4. Complete todo: Verify checkbox works, visual state changes

### Notifications
1. All CRUD operations should show Toast notification (success/error)

## Troubleshooting

### Components not importing
- Check import paths start with `@/components/ui/`
- Verify shadcn component is installed: `npx shadcn-ui@latest list`

### API calls failing
- Check backend is running on port 8000
- Check JWT token in localStorage (DevTools Application tab)
- Check browser console for CORS or network errors

### Responsive issues
- Use DevTools responsive mode to test different screen sizes
- Check Tailwind breakpoints: `sm` (640px), `md` (768px), `lg` (1024px)
- Verify `hidden md:flex` and similar responsive classes

### State not updating
- Check `useTasks` hook is imported correctly
- Verify API calls complete before UI update
- Check browser console for errors

## Next Steps

After implementation:
1. Run `/sp.tasks` to generate task checklist for development
2. Follow TDD workflow: write tests, implement, verify
3. Create git commits with Feature/Task IDs: `Implement FR-001: Landing page hero section`
4. Run tests with `npm run test` to verify 70%+ coverage
5. Create PR when feature complete

## Files Summary

**Total new files**: ~18
**Total modified files**: ~5
**Total deleted files**: 0
**Estimated implementation time**: Phased approach (P1 -> P2 -> P3)

---

**Ready to proceed?** Run `/sp.tasks` to generate implementation task checklist.
