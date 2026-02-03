# Tasks: Fix Priority Dashboard and Comprehensive Theme Styling

**Input**: Design documents from `/specs/004-fix-priority-theme/`
**Branch**: `004-fix-priority-theme`
**Feature**: Fix priority dashboard filtering and comprehensive theme/styling overhaul
**Prerequisites**: spec.md, plan.md, research.md

**Tests**: No tests are specified in the feature specification. Following TDD principle, component-level tests (Jest) will be created during implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5, US6)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and theme system preparation

- [x] T001 Extend globals.css with semantic theme variables for priority colors and form states in `frontend/src/app/globals.css`
- [x] T002 Update PRIORITY_CONFIG in `frontend/src/lib/validations/task.ts` to remove hardcoded Tailwind color classes
- [x] T003 [P] Verify WCAG AA contrast ratios for all priority badge colors (high, medium, low, none) in light and dark modes

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core theme infrastructure that enables all component styling updates

**⚠️ CRITICAL**: Theme variable system must be complete before ANY component styling task can begin

- [x] T004 Create comprehensive CSS variable reference document mapping semantic tokens to all affected components in `specs/004-fix-priority-theme/theme-variables.md`
- [x] T005 [P] Setup test utilities for theme color verification in `frontend/__tests__/utils/theme-colors.test.ts`

**Checkpoint**: Theme system ready - component styling updates can now begin in parallel ✅

---

## Phase 3: User Story 1 - View All Priority Levels in Dashboard (Priority: P1) 🎯 MVP

**Goal**: Fix priority dashboard to display all three priority levels (High, Medium, Low) instead of only High

**Independent Test**: Navigate to `/dashboard/priority` and verify High, Medium, Low priority sections all display their respective todos

### Implementation for User Story 1

- [ ] T006 [US1] Fix priority filtering logic in `frontend/src/app/dashboard/priority/page.tsx` to render all priority levels (high, medium, low, none)
- [ ] T007 [US1] Update PriorityTabs component in `frontend/src/app/dashboard/components/PriorityTabs.tsx` to include all 4 priority tabs with correct labels and sort order
- [ ] T008 [US1] Verify dashboard displays empty state for priority levels with no todos in `frontend/src/app/dashboard/priority/page.tsx`
- [ ] T009 [US1] Test priority dashboard with mixed priority todos (some priorities empty, some full) to ensure all levels render correctly
- [ ] T010 [US1] Verify new todo immediately appears in correct priority section on dashboard after creation

**Checkpoint**: User Story 1 complete - priority dashboard shows all priority levels correctly

---

## Phase 4: User Story 2 - Read Text and Interact with Auth Forms (Priority: P1)

**Goal**: Make signin/signup forms readable with proper text contrast and styled inputs using theme variables

**Independent Test**: Navigate to signin/signup pages and verify all labels, inputs, buttons, and links are readable with proper styling

### Implementation for User Story 2

- [ ] T011 [P] [US2] Replace hardcoded error colors in `frontend/src/components/auth/SignInForm.tsx` with semantic theme variables (--error-bg, --error-border, --error-text)
- [ ] T012 [P] [US2] Replace hardcoded error colors in `frontend/src/components/auth/SignUpForm.tsx` with semantic theme variables
- [ ] T013 [P] [US2] Replace hardcoded link colors in both auth forms with `--link-text` and `--link-text-hover` variables
- [ ] T014 [P] [US2] Replace hardcoded input styling in both auth forms with `--input-bg`, `--input-border`, `--input-text` variables
- [ ] T015 [P] [US2] Replace hardcoded helper text colors in both auth forms with `--foreground` or appropriate semantic variable
- [ ] T016 [US2] Update signin page in `frontend/src/app/(auth)/sign-in/page.tsx` to use theme-aware styling if needed
- [ ] T017 [US2] Update signup page in `frontend/src/app/(auth)/sign-up/page.tsx` to use theme-aware styling if needed
- [ ] T018 [US2] Test auth forms in light mode - verify all text readable, inputs visible, buttons styled correctly
- [ ] T019 [US2] Test auth forms in dark mode - verify all text readable, inputs visible, buttons styled correctly
- [ ] T020 [US2] Test auth form focus states and placeholder text visibility in both light and dark modes

**Checkpoint**: User Story 2 complete - auth forms are readable with proper theme styling

---

## Phase 5: User Story 3 - Navigate and Read Sidebar (Priority: P1)

**Goal**: Make sidebar navigation readable with proper text contrast and consistent styling using theme variables

**Independent Test**: Log in, view sidebar, and verify all headings, links, and navigation text are readable with clear active/inactive states

### Implementation for User Story 3

- [ ] T021 [P] [US3] Replace hardcoded sidebar colors in `frontend/src/app/dashboard/components/Sidebar.tsx` with semantic theme variables
- [ ] T022 [P] [US3] Update sidebar heading styling to use `--foreground` theme variable in `frontend/src/app/dashboard/components/Sidebar.tsx`
- [ ] T023 [P] [US3] Update sidebar link styling to use semantic variables with proper hover and active states in `frontend/src/app/dashboard/components/Sidebar.tsx`
- [ ] T024 [US3] Update DashboardNav component in `frontend/src/app/dashboard/components/DashboardNav.tsx` to use theme-aware colors
- [ ] T025 [US3] Test sidebar in light mode - verify all text readable, links styled, active route highlighted correctly
- [ ] T026 [US3] Test sidebar in dark mode - verify all text readable, links styled, active route highlighted correctly
- [ ] T027 [US3] Test sidebar hover states on links - verify visual feedback is clear and accessible

**Checkpoint**: User Story 3 complete - sidebar navigation is readable and well-styled

---

## Phase 6: User Story 4 - View and Edit Todo Cards with Visible Menus (Priority: P1)

**Goal**: Make todo cards readable with visible action menus and proper color contrast using theme variables

**Independent Test**: View todo list, verify card content and tags readable, click three-dot menu, verify Edit/Delete options visible

### Implementation for User Story 4

- [ ] T028 [P] [US4] Replace hardcoded colors in `frontend/src/app/dashboard/components/TodoCard.tsx` with semantic theme variables
- [ ] T029 [P] [US4] Update todo title and description styling to use `--foreground` variable in TodoCard
- [ ] T030 [P] [US4] Update todo card background and border to use theme variables in TodoCard
- [ ] T031 [US4] Update three-dot menu styling in TodoCard to ensure menu icon and button are visible and clickable
- [ ] T032 [US4] Update menu dropdown styling to ensure Edit/Delete options are readable with proper contrast in TodoCard
- [ ] T033 [P] [US4] Replace hardcoded colors in `frontend/src/components/tasks/TagChip.tsx` with semantic theme variables
- [ ] T034 [P] [US4] Update tag styling in TodoCard to match theme system while maintaining priority-based coloring
- [ ] T035 [US4] Test todo cards in light mode - verify title/description readable, menu visible and functional
- [ ] T036 [US4] Test todo cards in dark mode - verify title/description readable, menu visible and functional
- [ ] T037 [US4] Test todo card hover states - verify visual feedback clear for interactive elements
- [ ] T038 [US4] Test editing todo from card menu - verify modal opens with proper styling

**Checkpoint**: User Story 4 complete - todo cards are readable with visible and functional menus

---

## Phase 7: User Story 5 - Use Add and Edit Todo Forms (Priority: P1)

**Goal**: Make add/edit todo forms fully visible with opaque backgrounds and readable input fields using theme variables

**Independent Test**: Open add/edit modal, verify background is opaque, all fields visible, text inputs accept and display text clearly, buttons styled

### Implementation for User Story 5

- [ ] T039 [P] [US5] Update TaskForm modal styling in `frontend/src/components/tasks/TaskForm.tsx` to use opaque background with theme variable
- [ ] T040 [P] [US5] Replace hardcoded form styling in TaskForm with theme variables (background, border, text colors)
- [ ] T041 [P] [US5] Replace hardcoded input field styling in TaskForm with `--input-bg`, `--input-border`, `--input-text` variables
- [ ] T042 [P] [US5] Replace hardcoded button styling in TaskForm with semantic theme variables (primary, secondary buttons)
- [ ] T043 [US5] Update form label styling to use `--foreground` variable in TaskForm
- [ ] T044 [US5] Update form placeholder text styling to use `--input-placeholder` variable in TaskForm
- [ ] T045 [US5] Update tag input styling in TaskForm to use theme variables in `frontend/src/components/tasks/TagInput.tsx`
- [ ] T046 [P] [US5] Replace hardcoded priority selector styling in TaskForm with semantic priority variables
- [ ] T047 [US5] Test add todo form in light mode - verify all fields visible, background opaque, text clear
- [ ] T048 [US5] Test add todo form in dark mode - verify all fields visible, background opaque, text clear
- [ ] T049 [US5] Test edit todo form in light mode - verify data loads, all fields editable
- [ ] T050 [US5] Test edit todo form in dark mode - verify data loads, all fields editable
- [ ] T051 [US5] Test form input focus states - verify clear visual indication of focused field

**Checkpoint**: User Story 5 complete - add/edit forms are fully visible and functional with theme styling

---

## Phase 8: User Story 6 - Log Out with Visible Button (Priority: P2)

**Goal**: Make logout button in footer visible and clearly styled using theme variables

**Independent Test**: Log in, view footer, verify logout button visible and styled, click it, verify redirect to signin page

### Implementation for User Story 6

- [ ] T052 [US6] Identify footer location and logout button component in codebase (likely in DashboardNav or layout)
- [ ] T053 [US6] Update logout button styling to use semantic theme variables instead of hardcoded colors
- [ ] T054 [US6] Ensure logout button has clear hover state using theme variables
- [ ] T055 [US6] Update footer styling if needed to ensure button container has proper contrast
- [ ] T056 [US6] Test logout button in light mode - verify visible, styled, clickable
- [ ] T057 [US6] Test logout button in dark mode - verify visible, styled, clickable
- [ ] T058 [US6] Test logout button click - verify user is redirected to signin and session is cleared

**Checkpoint**: User Story 6 complete - logout button is visible and functional

---

## Phase 9: Additional Components & Cross-Cutting Styling

**Purpose**: Update remaining components and ensure theme consistency across entire app

- [ ] T059 [P] Replace hardcoded colors in `frontend/src/components/tasks/FilterPanel.tsx` with semantic theme variables
- [ ] T060 [P] Replace hardcoded colors in `frontend/src/components/tasks/PriorityBadge.tsx` with semantic priority variables (high, medium, low, none)
- [ ] T061 [P] Replace hardcoded colors in `frontend/src/components/tasks/SearchBar.tsx` with theme variables
- [ ] T062 [P] Replace hardcoded colors in `frontend/src/components/tasks/SortSelector.tsx` with theme variables
- [ ] T063 [P] Review all dashboard page files (`frontend/src/app/dashboard/overview/page.tsx`, `tags/page.tsx`, `todos/page.tsx`) for hardcoded colors and update with theme variables
- [ ] T064 [P] Verify all ShadCN UI components are using theme variables correctly in `frontend/src/components/ui/`
- [ ] T065 Ensure landing page (`frontend/src/app/(landing)/page.tsx`) uses theme variables if not already done

---

## Phase 10: Theme Consistency & Testing

**Purpose**: Verify theme works correctly across app, light/dark modes, and accessibility standards

- [ ] T066 Test light mode theme switching - navigate through all pages, verify all colors correct
- [ ] T067 Test dark mode theme switching - navigate through all pages, verify all colors correct
- [ ] T068 Test theme persistence - switch theme, reload page, verify theme persists
- [ ] T069 Verify WCAG AA contrast ratios for entire app (priority badges, buttons, text on backgrounds)
- [ ] T070 Test responsive behavior - verify theme colors work on mobile, tablet, desktop
- [ ] T071 Visual regression testing - compare screenshots of before/after for all updated components
- [ ] T072 Accessibility audit - screen reader testing, keyboard navigation, focus indicators

---

## Phase 11: Polish & Documentation

**Purpose**: Final cleanup, documentation, and cross-cutting concerns

- [ ] T073 [P] Create theme usage guide documenting all semantic variables and when to use each in `frontend/docs/THEME.md`
- [ ] T074 [P] Update component documentation to reference theme variables in appropriate places
- [ ] T075 Code review - verify all hardcoded Tailwind color classes have been replaced (use grep/search: `text-`, `bg-`, `border-` with specific colors)
- [ ] T076 Verify no regressions in other features (dashboard, tasks, auth flows)
- [ ] T077 Test with different browser zoom levels to ensure UI doesn't break
- [ ] T078 Performance check - verify CSS variable changes don't impact load time
- [ ] T079 Final cleanup - commit message following spec/branch naming conventions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all component updates
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - Can proceed in priority order (P1 stories, then P2)
  - User stories US1-US5 can proceed in parallel once Foundational done
  - User Story US6 is P2 and can start when convenient
- **Additional Components (Phase 9)**: Depends on foundational tasks, can run parallel with user stories
- **Testing (Phase 10)**: Depends on all component updates
- **Polish (Phase 11)**: Final phase after all substantive work complete

### Within User Stories

- Tests (if included) MUST be written and FAIL before implementation
- Components before integration
- Component styling before testing
- All components in story before moving to next story

### Parallel Opportunities

- **Phase 1 Setup**: T001 (globals.css) must be first; T002, T003 can parallel after
- **Phase 2 Foundational**: T004, T005 can run somewhat in parallel
- **Phase 3+ User Stories**: Multiple stories can be worked in parallel by different developers:
  - Developer A: User Story 1 (T006-T010)
  - Developer B: User Story 2 (T011-T020)
  - Developer C: User Story 3 (T021-T027)
  - Once available: Developer D: User Story 4 (T028-T038)
  - Once available: Developer E: User Story 5 (T039-T051)
- **Phase 9 Components**: All marked [P] can run in parallel - different files, no dependencies
- **Phase 10 Testing**: Can begin once Phase 9 components complete

---

## Parallel Example: Phase 9 Components (Can run simultaneously)

```
Task T059: FilterPanel.tsx colors
Task T060: PriorityBadge.tsx colors
Task T061: SearchBar.tsx colors
Task T062: SortSelector.tsx colors
Task T063: Dashboard pages colors
Task T064: ShadCN UI components review
→ All can execute in parallel - different files
```

---

## Parallel Example: User Stories 1-5 After Foundational

```
Developer A works on US1 (T006-T010):
  - Fix priority dashboard filtering
  - Update PriorityTabs
  - Test all priority levels display

Developer B works on US2 (T011-T020):
  - SignInForm colors
  - SignUpForm colors
  - Auth form testing

Developer C works on US3 (T021-T027):
  - Sidebar styling
  - DashboardNav styling
  - Sidebar testing

→ All can work in parallel - different files/components
```

---

## Implementation Strategy

### MVP First (User Stories 1-5)

1. Complete Phase 1: Setup (theme variables and config)
2. Complete Phase 2: Foundational (theme system ready)
3. Complete Phase 3: User Story 1 (priority dashboard)
4. Complete Phase 4: User Story 2 (auth forms)
5. Complete Phase 5: User Story 3 (sidebar)
6. Complete Phase 6: User Story 4 (todo cards)
7. Complete Phase 7: User Story 5 (add/edit forms)
8. **STOP and VALIDATE**: All critical user stories working, theme system functional
9. Deploy MVP with P1 features

### Extended Delivery

10. Complete Phase 8: User Story 6 (logout button - P2)
11. Complete Phase 9: Additional components
12. Complete Phase 10: Theme consistency & testing
13. Complete Phase 11: Polish & documentation
14. Final deploy with all features

### Incremental Validation

- After Phase 2: Verify theme variables loaded correctly
- After User Story 1: Check priority dashboard works independently
- After User Story 2: Check auth forms are readable
- After User Story 3: Check sidebar navigation works
- After User Story 4: Check todo cards visible with menus
- After User Story 5: Check forms complete
- After Phase 10: Full app tested for WCAG AA compliance

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Phase 2 (Foundational) MUST complete before any styling tasks begin
- Verify theme colors in both light and dark modes for each update
- Use semantic variables defined in Phase 1, not hardcoded Tailwind classes
- Stop at any checkpoint to validate independently
- Commit after each logical group of related tasks
- All file paths relative to repository root: `frontend/src/...`
