---
description: "Task list for Modern UI Dashboard Transformation feature"
---

# Tasks: Modern UI Dashboard Transformation

**Feature**: 003-modern-ui-dashboard
**Branch**: 003-modern-ui-dashboard
**Status**: Ready for Implementation
**Input**: Design documents from `specs/003-modern-ui-dashboard/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅

**Overview**: Frontend-only transformation with 7 user stories, zero backend changes. Tasks organized by user story priority for independent implementation and testing.

---

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1-US7) from spec.md
- Exact file paths included for implementation clarity

---

## Phase 1: Setup & Routing Structure

**Purpose**: Establish directory structure and routing organization

- [ ] T001 Create landing page route structure: `frontend/src/app/(landing)/` directory
- [ ] T002 Create dashboard page routes: `frontend/src/app/dashboard/{overview,todos,priority,tags}/` directories
- [ ] T003 Create dashboard components directory: `frontend/src/app/dashboard/components/`
- [ ] T004 Create landing page components directory: `frontend/src/app/(landing)/components/`

**Checkpoint**: Directory structure ready for implementation

---

## Phase 2: Foundational Components (Blocking Prerequisites)

**Purpose**: Core components and utilities ALL stories depend on

⚠️ **CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Implement shadcn Card component wrapper pattern in existing `frontend/src/components/ui/card.tsx`
- [ ] T006 [P] Verify shadcn Dialog component exists in `frontend/src/components/ui/dialog.tsx`
- [ ] T007 [P] Verify shadcn AlertDialog component exists in `frontend/src/components/ui/alert-dialog.tsx`
- [ ] T008 [P] Verify shadcn Button component exists in `frontend/src/components/ui/button.tsx`
- [ ] T009 [P] Verify Sonner Toast integration in `frontend/src/app/layout.tsx`
- [ ] T010 Create navigation configuration utility in `frontend/src/lib/dashboard-navigation.ts`
- [ ] T011 Create dashboard statistics calculation utility in `frontend/src/lib/dashboard-stats.ts`
- [ ] T012 Create priority color mapping utility in `frontend/src/lib/priority-colors.ts`
- [ ] T013 Update root layout with AuthProvider in `frontend/src/app/layout.tsx` (verify Toaster present)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Public Landing Page (Priority: P1) 🎯

**Goal**: Create professional public landing page at `/` with hero section, features grid, and CTAs

**Independent Test**: Visit `/` without authentication, verify all sections render correctly, test CTA navigation

### Implementation for User Story 1

- [ ] T014 [P] [US1] Implement Landing page component in `frontend/src/app/(landing)/page.tsx` with route guard (public accessible)
- [ ] T015 [P] [US1] Implement Hero component in `frontend/src/app/(landing)/components/Hero.tsx` with headline, description, illustration placeholder, two CTA buttons
- [ ] T016 [P] [US1] Implement Features component in `frontend/src/app/(landing)/components/Features.tsx` displaying 3-4 feature cards with icons and descriptions
- [ ] T017 [P] [US1] Implement Navigation component in `frontend/src/app/(landing)/components/Navigation.tsx` with logo, navigation links, auth action buttons
- [ ] T018 [P] [US1] Implement Footer component in `frontend/src/app/(landing)/components/Footer.tsx` with professional footer content
- [ ] T019 [US1] Add responsive layout to Landing page - test mobile (320px), tablet (768px), desktop (1920px) in `frontend/src/app/(landing)/page.tsx`
- [ ] T020 [US1] Verify all CTA buttons navigate correctly - "Get Started" → `/sign-up`, "Sign In" → `/sign-in`
- [ ] T021 [US1] Add smooth scroll and transitions to Landing page components
- [ ] T022 [US1] Add accessibility (ARIA labels, semantic HTML) to all Landing page components

**Checkpoint**: Landing page (US1) fully functional and testable independently

---

## Phase 4: User Story 2 - Enhanced Authentication (Priority: P1)

**Goal**: Provide professional auth pages using shadcn components with validation and error handling

**Independent Test**: Navigate to `/sign-in` and `/sign-up`, test form validation, valid/invalid credentials, successful auth flow

### Implementation for User Story 2

- [ ] T023 [P] [US2] Verify sign-in form exists in `frontend/src/components/auth/SignInForm.tsx` with email, password inputs, shadcn components
- [ ] T024 [P] [US2] Verify sign-up form exists in `frontend/src/components/auth/SignUpForm.tsx` with email, password inputs, validation
- [ ] T025 [US2] Enhance sign-in page styling in `frontend/src/app/(auth)/sign-in/page.tsx` - center form, add redirects
- [ ] T026 [US2] Enhance sign-up page styling in `frontend/src/app/(auth)/sign-up/page.tsx` - center form, add redirects
- [ ] T027 [US2] Add form validation error messages for both auth forms (inline validation)
- [ ] T028 [US2] Add authentication success redirect to `/dashboard/overview` in both sign-in and sign-up forms
- [ ] T029 [US2] Add authenticated users redirect - if already signed in and accessing `/sign-in` or `/sign-up`, redirect to `/dashboard/overview`
- [ ] T030 [US2] Add responsive design to auth pages - test mobile, tablet, desktop layouts
- [ ] T031 [US2] Add toast notifications for auth errors and success (using existing Sonner setup)

**Checkpoint**: Authentication (US2) fully functional with proper form handling and redirects

---

## Phase 5: User Story 3 - Dashboard Navigation Structure (Priority: P2)

**Goal**: Implement dashboard layout with persistent sidebar (desktop) and hamburger menu (mobile) for section navigation

**Independent Test**: Sign in, navigate dashboard - verify sidebar/menu sections accessible, active section highlighted, logout works, mobile responsiveness

### Implementation for User Story 3

- [ ] T032 [P] [US3] Implement Sidebar component in `frontend/src/app/dashboard/components/Sidebar.tsx` - display nav sections, user info, logout button
- [ ] T033 [P] [US3] Implement MobileMenu component in `frontend/src/app/dashboard/components/MobileMenu.tsx` - Sheet drawer for mobile navigation
- [ ] T034 [P] [US3] Implement DashboardNav component in `frontend/src/app/dashboard/components/DashboardNav.tsx` - navigation header with hamburger trigger
- [ ] T035 [US3] Update dashboard layout in `frontend/src/app/dashboard/layout.tsx` - add Sidebar + MobileMenu, implement responsive visibility (hidden on mobile, show on desktop)
- [ ] T036 [US3] Implement active section highlighting using `usePathname()` hook in `frontend/src/app/dashboard/components/Sidebar.tsx`
- [ ] T037 [US3] Implement logout functionality in navigation components - sign out and redirect to `/sign-in`
- [ ] T038 [US3] Add protected route check in dashboard layout - redirect unauthenticated users to `/sign-in`
- [ ] T039 [US3] Modify `/dashboard` page.tsx to redirect to `/dashboard/overview` in `frontend/src/app/dashboard/page.tsx`
- [ ] T040 [US3] Add responsive hamburger menu toggle in `frontend/src/app/dashboard/components/DashboardNav.tsx` - visible only on mobile
- [ ] T041 [US3] Test mobile responsiveness - hamburger menu opens/closes, sidebar hidden on mobile
- [ ] T042 [US3] Add user email/name display in navigation sidebar in `frontend/src/app/dashboard/components/Sidebar.tsx`

**Checkpoint**: Dashboard navigation (US3) fully functional with proper routing and responsive design

---

## Phase 6: User Story 4 - Dashboard Overview Statistics (Priority: P2)

**Goal**: Display todo statistics (total, completed, pending, today) in card-based layout

**Independent Test**: Navigate to `/dashboard/overview`, create various todos, verify stat counts accurate and update on todo changes

### Implementation for User Story 4

- [ ] T043 [P] [US4] Implement StatCard component in `frontend/src/app/dashboard/components/StatCard.tsx` - display stat label, number, icon, optional progress
- [ ] T044 [P] [US4] Create dashboard statistics calculation hook in `frontend/src/hooks/useDashboardStats.ts` - calculate total, completed, pending, today todos
- [ ] T045 [US4] Implement Overview page in `frontend/src/app/dashboard/overview/page.tsx` - render 4 StatCards using calculated statistics
- [ ] T046 [US4] Add empty state to Overview page - display helpful message when user has no todos
- [ ] T047 [US4] Add loading skeleton to Overview page - show skeleton while statistics load
- [ ] T048 [US4] Implement responsive grid layout for stat cards - stack vertically on mobile, 2-4 columns on larger screens
- [ ] T049 [US4] Add icons to stat cards from Lucide React - appropriate icons for total, completed, pending, today
- [ ] T050 [US4] Add color-coded stat cards - different background/border colors for visual distinction
- [ ] T051 [US4] Test statistics accuracy - create todos with different statuses and verify counts

**Checkpoint**: Overview page (US4) displays accurate statistics and updates dynamically

---

## Phase 7: User Story 5 - All Todos Management Page (Priority: P1)

**Goal**: Implement comprehensive todo management page with CRUD operations, filtering, searching, and visual feedback

**Independent Test**: Create/edit/delete todos with various priorities and tags, use filters and search, mark todos complete, verify Toast notifications

### Implementation for User Story 5

- [ ] T052 [P] [US5] Reuse existing `useTasks()` hook in `frontend/src/hooks/useTasks.ts` for todo data operations
- [ ] T053 [P] [US5] Verify existing TaskForm component exists in `frontend/src/components/tasks/TaskForm.tsx`
- [ ] T054 [US5] Implement Todos page component in `frontend/src/app/dashboard/todos/page.tsx` - display todo cards, add/edit/delete dialogs
- [ ] T055 [US5] Wrap TodoItem in shadcn Card component - display title, description, priority badge, tags, completion checkbox, action menu
- [ ] T056 [US5] Implement "Add Todo" button with Dialog modal for creating new todos using TaskForm in `frontend/src/app/dashboard/todos/page.tsx`
- [ ] T057 [US5] Implement todo edit functionality - clicking Edit opens Dialog with TaskForm pre-populated with todo data
- [ ] T058 [US5] Implement todo delete functionality - clicking Delete opens AlertDialog for confirmation
- [ ] T059 [US5] Implement todo completion toggle - checkbox marks todo complete/incomplete with optimistic UI update
- [ ] T060 [US5] Add priority badge styling to todos - use priority colors utility (high=red, medium=yellow, low=green, none=gray)
- [ ] T061 [US5] Add tag badges to todo cards - display as small badges with tag names
- [ ] T062 [US5] Implement filter options in todos page - All/Active/Completed filters
- [ ] T063 [US5] Implement search functionality - debounced search that filters todos by title or description (case-insensitive)
- [ ] T064 [US5] Add task count display - "Showing X of Y tasks (Z total)" with current filter applied
- [ ] T065 [US5] Implement empty state messaging - show contextual messages for no todos vs. filter returning zero results
- [ ] T066 [US5] Add separator components between todo items or use card spacing for visual organization
- [ ] T067 [US5] Add Toast notifications for all CRUD operations - success messages for create/update/delete, error messages for failures
- [ ] T068 [US5] Implement responsive design for todos page - stack cards vertically on mobile, multi-column on larger screens
- [ ] T069 [US5] Add visual styling for completed todos - gray background and strikethrough text

**Checkpoint**: Todos page (US5) fully functional with all CRUD operations, filtering, and search

---

## Phase 8: User Story 6 - Priority-Based Todo Organization (Priority: P3)

**Goal**: Organize todos by priority level with tabs/sections for High/Medium/Low priorities

**Independent Test**: Create todos with different priorities, navigate to `/dashboard/priority`, verify todos grouped correctly, tab switching works

### Implementation for User Story 6

- [ ] T070 [P] [US6] Implement PriorityTabs component in `frontend/src/app/dashboard/components/PriorityTabs.tsx` - tabs/sections for High/Medium/Low
- [ ] T071 [US6] Implement Priority page in `frontend/src/app/dashboard/priority/page.tsx` - display PriorityTabs, render todos for selected priority
- [ ] T072 [US6] Add count badges to priority tabs - show number of todos at each priority level
- [ ] T073 [US6] Reuse todo card component from todos page - same styling, filtering, CRUD functionality
- [ ] T074 [US6] Implement empty state for each priority section - show message when no todos at that priority
- [ ] T075 [US6] Add responsive tab layout - stacked tabs on mobile, horizontal on desktop
- [ ] T076 [US6] Test priority filtering - verify todos correctly grouped by high/medium/low

**Checkpoint**: Priority page (US6) displays todos correctly organized by priority level

---

## Phase 9: User Story 7 - Tag-Based Todo Organization (Priority: P3)

**Goal**: Display all unique tags as clickable badges, allow filtering todos by tag

**Independent Test**: Create todos with various tags, navigate to `/dashboard/tags`, click tag badges, verify filtered todos display correctly

### Implementation for User Story 7

- [ ] T077 [P] [US7] Implement TagsList component in `frontend/src/app/dashboard/components/TagsList.tsx` - display unique tags as clickable badges
- [ ] T078 [US7] Implement Tags page in `frontend/src/app/dashboard/tags/page.tsx` - render TagsList and filtered todos for selected tag
- [ ] T079 [US7] Add tag count display - show count of todos with each tag (optional in requirements)
- [ ] T080 [US7] Implement tag filtering - clicking a tag badge displays only todos containing that tag
- [ ] T081 [US7] Extract unique tags from todos data - derive list of all tags across user's todos
- [ ] T082 [US7] Reuse todo card component from todos page - same styling, CRUD functionality on tags page
- [ ] T083 [US7] Implement empty state - show message when user has no tags
- [ ] T084 [US7] Add responsive badge layout - wrap badges on mobile, grid layout on desktop
- [ ] T085 [US7] Test tag filtering - verify todos correctly filtered by selected tag

**Checkpoint**: Tags page (US7) displays all tags and filters todos correctly

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements, testing, and validation across all user stories

- [ ] T086 [P] Implement route loading skeleton in `frontend/src/app/dashboard/loading.tsx` - show skeleton while dashboard routes load
- [ ] T087 [P] Add smooth page transitions and animations using CSS/Tailwind in dashboard pages
- [ ] T088 [P] Verify dark mode support - test theme toggle if implemented, ensure all components work in dark mode
- [ ] T089 [P] Accessibility audit - verify ARIA labels, semantic HTML, keyboard navigation on all pages
- [ ] T090 [P] Test cross-browser compatibility - Chrome, Firefox, Safari, Edge on latest versions
- [ ] T091 Verify performance metrics - Landing page < 2s, Dashboard routes < 1s, CRUD feedback < 500ms
- [ ] T092 Create end-to-end test scenarios validating all user stories work together
- [ ] T093 Run quickstart.md validation - verify all dev setup instructions work correctly
- [ ] T094 Create PR description documenting all changes, linking to spec/plan/research docs
- [ ] T095 Final manual testing checklist - verify all 88 functional requirements addressed

**Checkpoint**: All user stories complete, tested, and ready for deployment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - BLOCKS all user stories
- **Phase 3 (US1 Landing)**: Depends on Phase 2 - independent of other user stories
- **Phase 4 (US2 Auth)**: Depends on Phase 2 - can run parallel to US1 or sequential
- **Phase 5 (US3 Navigation)**: Depends on Phase 2 - can run parallel to US1/US2
- **Phase 6 (US4 Overview)**: Depends on Phase 5 - needs navigation structure first
- **Phase 7 (US5 Todos)**: Depends on Phase 5 - needs navigation structure first
- **Phase 8 (US6 Priority)**: Depends on Phase 5 - uses todo card component from US5
- **Phase 9 (US7 Tags)**: Depends on Phase 5 - uses todo card component from US5
- **Phase 10 (Polish)**: Depends on all user story phases

### User Story Dependencies (After Foundational)

```
Foundational (Phase 2) [BLOCKING]
  ├─→ US1 Landing (P1) [Can start immediately]
  ├─→ US2 Auth (P1) [Can start immediately, parallel to US1]
  ├─→ US3 Navigation (P2) [Can start after Phase 2]
  │   ├─→ US4 Overview (P2) [Depends on US3 Navigation]
  │   ├─→ US5 Todos (P1) [Depends on US3 Navigation] ← Core functionality
  │   │   ├─→ US6 Priority (P3) [Depends on US5 Todos]
  │   │   └─→ US7 Tags (P3) [Depends on US5 Todos]
```

### Recommended Execution Order (Single Developer)

1. **Phase 1**: Setup routing structure (T001-T004)
2. **Phase 2**: Foundational components (T005-T013) - BLOCKING
3. **Phase 3 + 4**: Landing + Auth pages in parallel (T014-T031) - Both P1
4. **Phase 5**: Dashboard Navigation (T032-T042) - Enables all dashboard pages
5. **Phase 7**: All Todos page (T052-T069) - Core functionality and US5 implementation
6. **Phase 6**: Overview statistics (T043-T051) - Uses dashboard nav
7. **Phase 8 + 9**: Priority + Tags pages (T070-T085) - Both P3, depend on US5
8. **Phase 10**: Polish & testing (T086-T095)

### Parallel Opportunities (Multiple Developers)

With 3+ developers:

1. **Phase 1 + 2** (1 dev): Setup + foundational infrastructure
2. **Once Phase 2 complete**, start in parallel:
   - **Dev A**: Phase 3 (Landing) - independent, no dependencies
   - **Dev B**: Phase 4 (Auth) - independent, no dependencies
   - **Dev C**: Phase 5 (Navigation) - foundation for dashboard pages
3. **Once Phase 5 complete**, continue:
   - **Dev A**: Phase 7 (Todos) - core functionality
   - **Dev B**: Phase 6 (Overview) - depends on Phase 5
   - **Dev C**: Phase 8 + 9 (Priority + Tags) - depends on Phase 7
4. **Phase 10** (All devs): Polish & testing

---

## MVP Scope (Minimum Viable Product)

To deliver MVP with core todo functionality:

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T013)
3. Complete Phase 4: Auth (T023-T031)
4. Complete Phase 5: Navigation (T032-T042)
5. Complete Phase 7: Todos page (T052-T069)
6. **STOP HERE** - Now have working authenticated todo app with dashboard
7. Can add Landing (Phase 3), Overview (Phase 6), Priority/Tags (Phases 8-9) as enhancements

**MVP Delivery**: Authenticated users can view, create, edit, delete, filter, and search todos with modern UI

---

## Incremental Delivery Strategy

Each phase delivers measurable user value:

- **Phase 1-2**: Foundation ready for UI implementation
- **Phase 1-2-3**: Landing page live - users understand product
- **Phase 1-2-3-4**: Sign up/login works - users can create accounts
- **Phase 1-2-3-4-5**: Dashboard navigation live - users navigate sections
- **Phase 1-2-3-4-5-7**: Full todo management - core product value delivered ✅ MVP COMPLETE
- **Phase +6**: Dashboard statistics - enhanced visibility
- **Phase +8-9**: Priority/Tag organization - advanced filtering
- **Phase +10**: Polished, tested, production-ready application

---

## Implementation Strategy Notes

- **[P] tasks** = different files, can run in parallel with no conflicts
- **[Story] label** = maps task to specific user story for traceability and independence
- **Within a phase**, sequential order matters where indicated (dependencies noted)
- **Across phases**, follow phase order - especially Phase 2 (foundational) blocks all stories
- **Each user story** should be independently testable and deployable
- **Verify tests/requirements** after each phase before proceeding to next
- **Commit frequently** - after each task or logical group, reference task IDs in commit messages
- **Stop at any checkpoint** to validate story independently before continuing
- **Total task count**: 95 tasks across all phases

---

## Success Criteria by Phase

- **Phase 1**: Directory structure created, no build errors
- **Phase 2**: All foundational utilities and components verified/created
- **Phase 3**: Landing page accessible at `/`, all CTAs navigate correctly
- **Phase 4**: Auth forms functional, validation working, redirects correct
- **Phase 5**: Dashboard layout renders, navigation works, protected routes redirect
- **Phase 6**: Overview page displays accurate statistics
- **Phase 7**: Todos page shows all CRUD operations, filtering, search working
- **Phase 8**: Priority page groups todos correctly, tabs switch properly
- **Phase 9**: Tags page displays unique tags, filtering works
- **Phase 10**: All pages responsive, tested, optimized, ready for production

---

## Notes

- This feature is **frontend-only** - no backend/database changes required
- All tasks use **existing shadcn/ui components** - no new UI library needed
- **Zero new dependencies** - all tools already installed
- **100% backward compatible** - existing todo functionality unchanged
- Task organization enables **independent story implementation** - each story can be completed separately
- **Constitutional compliance** verified - no violations to project governance principles
- See `plan.md`, `spec.md`, `data-model.md`, `research.md` for detailed context

