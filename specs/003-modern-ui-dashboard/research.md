# Research: Modern UI Dashboard Transformation

**Feature**: 003-modern-ui-dashboard
**Date**: 2026-01-29
**Purpose**: Resolve technical unknowns and identify best practices for UI transformation

## Research Questions

### Q1: shadcn/ui Component Architecture Best Practices

**Question**: What is the recommended approach for organizing and using shadcn/ui components in a Next.js App Router application?

**Findings**:
- shadcn/ui components are installed in `components/ui/` directory
- Components are built on Radix UI primitives with Tailwind CSS styling
- Import components directly from `@/components/ui/*`
- Component composition pattern: combine multiple shadcn components for complex UI
- Theme configuration via CSS variables in `globals.css`
- Tailwind config integrated with `components.json`

**Decision**: Use existing shadcn component structure with direct imports

**Rationale**:
- 58 shadcn components already installed and configured
- Existing `components.json` and Tailwind v4 setup working correctly
- No additional configuration needed

**Alternatives Considered**:
- Creating custom component wrappers: Rejected - adds unnecessary abstraction
- Using a different UI library: Rejected - violates requirement to use shadcn/ui exclusively

---

### Q2: Next.js App Router Routing Structure for Dashboard

**Question**: What is the best routing structure for a multi-section dashboard in Next.js 14+ App Router?

**Findings**:
- App Router uses file-system based routing in `app/` directory
- Route groups with `(name)` for organization without URL segments
- Nested layouts for persistent UI elements (sidebar, nav)
- Dynamic segments with `[param]` for variable routes
- Parallel routes with `@folder` for complex layouts
- Intercepting routes with `(.)` for modals

**Current Structure**:
```
app/
├── (auth)/
│   ├── sign-in/page.tsx
│   └── sign-up/page.tsx
└── dashboard/
    ├── layout.tsx
    └── page.tsx
```

**Decision**: Extend dashboard with nested routes and shared layout

**Proposed Structure**:
```
app/
├── (landing)/
│   ├── page.tsx                    # Landing page at /
│   ├── components/                 # Landing-specific components
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   ├── Navigation.tsx
│   │   └── Footer.tsx
│   └── layout.tsx                  # Optional landing layout
├── (auth)/
│   ├── sign-in/page.tsx
│   ├── sign-up/page.tsx
│   └── components/                 # Auth form components
│       ├── SignInForm.tsx (existing)
│       └── SignUpForm.tsx (existing)
└── dashboard/
    ├── layout.tsx                  # Shared dashboard layout with sidebar
    ├── overview/page.tsx           # /dashboard/overview
    ├── todos/page.tsx              # /dashboard/todos
    ├── priority/page.tsx           # /dashboard/priority
    ├── tags/page.tsx               # /dashboard/tags
    ├── components/                 # Dashboard-specific components
    │   ├── Sidebar.tsx
    │   ├── DashboardNav.tsx
    │   ├── StatCard.tsx
    │   └── ...
    └── page.tsx                    # Redirect to /dashboard/overview
```

**Rationale**:
- Route groups `(landing)` and `(auth)` organize public pages without affecting URLs
- Nested `dashboard/*` routes share common layout with sidebar
- Co-located components in feature directories for better organization
- Follows Next.js App Router best practices

**Alternatives Considered**:
- Flat structure with all pages in app root: Rejected - poor organization
- Single dashboard page with client-side routing: Rejected - loses App Router benefits
- Using `@modal` parallel routes for dialogs: Deferred - not needed for initial implementation

---

### Q3: State Management for Dashboard Navigation

**Question**: How should dashboard navigation state (active section, mobile menu) be managed?

**Findings**:
- React Context for shared state across dashboard
- URL state via Next.js `usePathname()` for active route detection
- Local state with `useState` for UI-only state (mobile menu open/closed)
- Server Components for initial rendering, Client Components for interactivity

**Decision**: Combine URL state + local state without global state library

**Implementation**:
- Active section: Derived from URL using `usePathname()`
- Mobile menu toggle: Local `useState` in Sidebar component
- User info: Existing Better Auth `useSession()` hook
- No Redux/Zustand needed for this feature

**Rationale**:
- Simple state requirements don't justify global state library
- URL is single source of truth for navigation
- Follows React and Next.js best practices
- Maintains existing patterns in codebase

**Alternatives Considered**:
- Redux/Zustand for dashboard state: Rejected - overkill for simple navigation
- React Context for all dashboard state: Rejected - URL state is simpler and more reliable

---

### Q4: Responsive Dashboard Layout Pattern

**Question**: What is the best approach for responsive sidebar that collapses to hamburger menu on mobile?

**Findings**:
- shadcn/ui provides `Sheet` component for slide-out menus
- Tailwind breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px)
- Common pattern: sidebar visible on desktop, Sheet drawer on mobile
- Conditional rendering based on screen size using Tailwind classes

**Decision**: Desktop sidebar + mobile Sheet component

**Implementation**:
```tsx
// Desktop: Fixed sidebar (hidden on mobile)
<aside className="hidden md:flex md:w-64 ...">
  <SidebarContent />
</aside>

// Mobile: Hamburger button + Sheet
<Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
  <SheetTrigger className="md:hidden">
    <MenuIcon />
  </SheetTrigger>
  <SheetContent side="left">
    <SidebarContent />
  </SheetContent>
</Sheet>
```

**Rationale**:
- shadcn Sheet component provides mobile-optimized drawer
- Tailwind responsive classes handle show/hide logic
- Single `<SidebarContent>` component reused in both contexts
- Standard pattern used in modern web applications

**Alternatives Considered**:
- Transform sidebar width on mobile: Rejected - poor UX on small screens
- Always-visible bottom navigation on mobile: Rejected - doesn't match requirement for hamburger menu
- Separate mobile and desktop navigation components: Rejected - violates DRY principle

---

### Q5: Todo Form Dialog vs Sheet Component

**Question**: Should the Add/Edit todo form use Dialog or Sheet component?

**Findings**:
- **Dialog**: Centered modal overlay, good for focused tasks
- **Sheet**: Slide-in panel from edge, more space for complex forms
- Both support backdrop click to close, escape key, and focus trapping

**Decision**: Use Dialog for Add/Edit todo forms

**Rationale**:
- Todo form is simple (4 fields: title, description, priority, tag)
- Centered Dialog provides better focus for data entry
- Consistent with typical form modal patterns
- Sheet reserved for navigation (mobile menu)

**Alternatives Considered**:
- Sheet for forms: Rejected - better suited for navigation or multi-step flows
- Inline form expansion: Rejected - specification requires Dialog/Sheet

---

### Q6: Empty State and Illustration Strategy

**Question**: How should empty states and illustrations (robot/3D element) be handled?

**Findings**:
- Lucide React icon library already installed (400+ icons)
- shadcn `empty` component available for empty states
- Illustration options:
  - Stock illustrations (unDraw, Storyset, etc.)
  - 3D libraries (Spline, Three.js)
  - SVG illustrations
  - Placeholder images

**Decision**: Lucide icons + simple SVG illustrations

**Hero Section Illustration**:
- Use Lucide `Bot` icon as placeholder or source free SVG from unDraw
- Fallback to icon-based design if no illustration asset available

**Empty States**:
- Use Lucide icons (`Inbox`, `Search`, `Filter`) with empty state text
- shadcn `empty` component for consistent styling

**Rationale**:
- Lucide icons immediately available
- SVG illustrations are lightweight and scalable
- Avoid complex 3D libraries for initial implementation
- Spec assumption: "Robot/3D illustration can be substituted with appropriate placeholder imagery"

**Alternatives Considered**:
- Three.js 3D robot: Rejected - adds complexity and bundle size
- Image files: Rejected - prefer SVG for scalability and performance

---

### Q7: Dark Mode Implementation

**Question**: Should dark mode be implemented in this phase?

**Findings**:
- shadcn/ui components support dark mode via `dark:` classes
- Next.js `next-themes` package recommended for theme switching
- CSS variables in `globals.css` define light/dark color schemes
- Current codebase has theme variables defined but no theme toggle

**Decision**: Defer dark mode toggle to future work

**Rationale**:
- Spec states: "FR-082: Application MUST support dark mode theming (if shadcn theme configuration supports it)"
- Theme configuration exists, but toggle UI not in requirements
- Assumption #10: "Dark mode implementation will follow existing theme configuration and may be deferred"
- Focus on core transformation features first

**Implementation**:
- Ensure all new components use CSS variable colors (not hardcoded)
- Prepare for future dark mode by avoiding dark-mode-incompatible styles
- No theme toggle UI in this phase

**Alternatives Considered**:
- Implement full dark mode with toggle: Rejected - not in scope, adds complexity
- Remove dark mode CSS variables: Rejected - they're already configured and don't hurt

---

### Q8: Loading States and Skeleton Components

**Question**: How should loading states be handled for async operations?

**Findings**:
- shadcn `skeleton` component available for loading placeholders
- shadcn `spinner` component for inline loading indicators
- Next.js App Router `loading.tsx` for route-level loading
- React Suspense for component-level loading

**Decision**: Combine multiple loading strategies

**Route-level**:
- `app/dashboard/loading.tsx` for initial page load
- Shows skeleton layout while data fetches

**Component-level**:
- Skeleton cards in Overview page while stats load
- Spinner in buttons during form submission
- Existing todo loading states (already implemented via `useTasks`)

**Rationale**:
- Layered approach provides feedback at appropriate granularity
- shadcn components ready to use
- Matches requirement FR-081: "Application MUST display loading states"

**Alternatives Considered**:
- Global loading spinner only: Rejected - poor UX, no context
- No loading states: Rejected - violates requirements

---

### Q9: Toast Notification Strategy

**Question**: Which toast system should be used (shadcn Sonner vs toast component)?

**Findings**:
- Sonner (already installed): Modern, feature-rich, `<Toaster />` in root layout
- shadcn `toast` component: Alternative implementation
- Current codebase uses Sonner

**Decision**: Continue using Sonner (already integrated)

**Implementation**:
- Sonner `<Toaster />` already in `app/layout.tsx`
- Import `toast` from `sonner` package
- Use for all CRUD notifications per FR-060

**Rationale**:
- Already installed and configured
- Feature-rich (promises, actions, customization)
- Consistent with existing implementation

**Alternatives Considered**:
- Switch to shadcn toast: Rejected - unnecessary change, Sonner works well

---

### Q10: Component Organization Strategy

**Question**: How should new components be organized?

**Findings**:
- Existing structure: `src/components/auth/`, `src/components/tasks/`, `src/components/ui/`
- Co-location patterns: Feature-specific components near pages
- Shared components in common directory

**Decision**: Hybrid approach - co-locate + shared components

**Structure**:
```
src/
├── app/
│   ├── (landing)/
│   │   ├── components/            # Landing-specific
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── Footer.tsx
│   │   └── page.tsx
│   └── dashboard/
│       ├── components/            # Dashboard-specific
│       │   ├── Sidebar.tsx
│       │   ├── DashboardNav.tsx
│       │   ├── StatCard.tsx
│       │   └── MobileMenu.tsx
│       └── ...
└── components/
    ├── ui/                        # shadcn components (existing)
    ├── auth/                      # Auth components (existing)
    └── tasks/                     # Task components (existing, reuse in dashboard)
```

**Rationale**:
- Co-location improves discoverability and maintainability
- Shared components remain in `src/components/` for reuse
- Follows Next.js App Router best practices
- Clear separation of concerns

**Alternatives Considered**:
- All components in `src/components/`: Rejected - poor discoverability
- Flat structure in app directory: Rejected - clutters page files

---

## Summary of Decisions

| Area | Decision | Key Rationale |
|------|----------|---------------|
| Component Library | Use existing shadcn/ui setup | 58 components installed, properly configured |
| Routing | Nested App Router with route groups | Best practice for dashboard multi-section layout |
| State Management | URL state + local state, no global library | Simple requirements, URL as source of truth |
| Responsive Layout | Desktop sidebar + mobile Sheet | Standard pattern, leverages shadcn components |
| Form Modals | Dialog component | Better for simple focused forms |
| Illustrations | Lucide icons + SVG placeholders | Lightweight, already available |
| Dark Mode | Defer toggle UI | Config exists, toggle out of scope |
| Loading States | Skeleton + Spinner + loading.tsx | Layered approach for different contexts |
| Toasts | Continue using Sonner | Already integrated, feature-rich |
| Component Organization | Co-locate + shared hybrid | Discoverability + reusability |

---

## Technology Integration Points

### Frontend Dependencies (No Changes Needed)
- Next.js 16.1.3 (App Router) ✅
- React 19.2.3 ✅
- TypeScript (strict mode) ✅
- Tailwind CSS 4 ✅
- shadcn/ui components (58 installed) ✅
- Better Auth 1.4.14 (client) ✅
- React Hook Form + Zod ✅
- Axios (with JWT interceptor) ✅
- Sonner (toast notifications) ✅
- Lucide React (icons) ✅

### Backend Dependencies (No Changes Needed)
- FastAPI (existing) ✅
- SQLModel (existing) ✅
- Better Auth (JWT verification) ✅
- PostgreSQL/Neon (existing) ✅

**Conclusion**: No new dependencies required. All technology already in place.

---

## Performance Considerations

### Bundle Size
- **Current**: shadcn components are tree-shakeable
- **Impact**: Minimal - only importing components actually used
- **Mitigation**: Code splitting via Next.js App Router (automatic)

### Initial Load Time
- **Target**: < 2 seconds (SC-006)
- **Strategy**:
  - Server Components for static content (landing, dashboard layout)
  - Client Components only where interactivity needed
  - Image optimization with Next.js Image component (if illustrations added)

### Route Navigation
- **Target**: < 1 second (SC-007)
- **Strategy**:
  - Prefetching with Next.js Link component
  - Shared dashboard layout prevents re-render
  - Skeleton loading states for perceived performance

---

## Security Considerations

### Authentication Flow
- **Existing**: Better Auth with JWT tokens
- **No Changes**: Use existing auth flow
- **Protected Routes**: Implement in dashboard layout (already partially done)

### API Security
- **Existing**: JWT token in Authorization header via Axios interceptor
- **No Changes**: Continue using existing pattern
- **User Isolation**: Backend already enforces user_id filtering

---

## Accessibility Considerations

### shadcn/ui Components
- Built on Radix UI (ARIA-compliant)
- Keyboard navigation supported
- Focus management in modals/dialogs
- Screen reader tested

### Additional Measures
- Semantic HTML elements
- Proper heading hierarchy
- Alt text for illustrations (when added)
- Color contrast compliance (via Tailwind design tokens)

**Note**: Spec assumption #13: "Basic accessibility through shadcn components' built-in ARIA support; comprehensive WCAG 2.1 AA compliance is out of scope"

---

## Open Questions Resolved

All technical unknowns have been resolved:

1. ✅ Component architecture → Use existing shadcn setup
2. ✅ Routing structure → Nested App Router with route groups
3. ✅ State management → URL state + local state
4. ✅ Responsive layout → Desktop sidebar + mobile Sheet
5. ✅ Form modals → Dialog component
6. ✅ Illustrations → Lucide icons + SVG
7. ✅ Dark mode → Defer toggle UI
8. ✅ Loading states → Multi-layered approach
9. ✅ Toasts → Sonner (existing)
10. ✅ Component organization → Co-locate + shared hybrid

**Ready to proceed to Phase 1: Design & Contracts**
