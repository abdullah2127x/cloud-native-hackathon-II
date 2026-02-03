# Implementation Plan: Fix Priority Dashboard and Comprehensive Theme Styling

**Branch**: `004-fix-priority-theme` | **Date**: 2026-02-03 | **Spec**: [specs/004-fix-priority-theme/spec.md](spec.md)
**Input**: Feature specification from `/specs/004-fix-priority-theme/spec.md`

## Summary

This plan addresses two critical issues: (1) Priority dashboard only displays High priority todos, missing Medium and Low priorities; (2) Widespread theme styling issues causing unreadable text, invisible inputs, and transparent form backgrounds due to hardcoded Tailwind color classes instead of ShadCN semantic variables.

**Technical Approach**:
- Fix priority filtering logic in the dashboard component to include all priority levels
- Migrate all hardcoded Tailwind color classes to ShadCN CSS custom property variables
- Update theme variables in `globals.css` to include semantic tokens for all component states
- Ensure WCAG AA compliance (4.5:1 contrast) across all text elements
- Support consistent light/dark mode switching via CSS custom properties

## Technical Context

**Frontend Language/Version**: TypeScript 5.x, Next.js 16 (App Router)
**Frontend Dependencies**: React 19, ShadCN UI, Tailwind CSS 3.4, lucide-react
**Backend Language/Version**: Python 3.11+
**Backend Dependencies**: FastAPI, SQLModel, Pydantic, Better Auth
**Storage**: PostgreSQL (Neon Serverless)
**Testing**: Jest (frontend), pytest (backend)
**Target Platform**: Web (browser) - modern browsers with CSS custom property support
**Project Type**: Web application (monorepo with separate frontend/backend)
**Performance Goals**: <200ms API response time, <4.5:1 contrast ratio for text (WCAG AA)
**Constraints**: JWT authentication required, user data isolation enforced, CSS variables for theme consistency
**Scale/Scope**: Full-stack feature affecting 5+ components, 2 major areas (dashboard + theme system)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ PASS - All constitutional requirements satisfied:**

1. **Test-Driven Development (I)**: TDD workflow will be followed with tests written before implementation
2. **No Manual Coding (II)**: All code changes will be generated via Claude Code based on this specification
3. **Code Quality Standards (III)**:
   - TypeScript strict mode (frontend)
   - Type hints (backend)
   - Test coverage minimum 70%
   - No hardcoded secrets
   - ✅ Files WILL reference Task IDs and feature branch
4. **Development Workflow (IV)**: Following Specify → Plan → Tasks → Implement order
5. **Governance (V)**: All changes comply with constitutional principles
6. **Scope Boundaries (VI)**: This feature stays within Phase 2 scope (web app task management)
7. **Persistent Storage (VIII)**: No changes to storage layer
8. **RESTful API (IX)**: No backend API changes needed (filtering happens frontend)
9. **Security & User Isolation (X)**: Frontend filtering, backend maintains isolation
10. **Authentication (XI)**: Better Auth with JWT - no changes needed
11. **Architecture (XII)**: Monorepo structure maintained - frontend and backend separation maintained
12. **Performance (XIII)**: Frontend changes won't affect API response times
13. **Technology Stack (XIV)**: Using Next.js, TypeScript, Tailwind CSS, ShadCN - all constitutional

## Project Structure

### Documentation (this feature)

```text
specs/004-fix-priority-theme/
├── spec.md              # Feature specification ✅ Complete
├── plan.md              # This file ✅ In progress
├── research.md          # Phase 0 (Not needed - no unknowns)
├── data-model.md        # Phase 1 output (Not applicable - no data model changes)
├── quickstart.md        # Phase 1 output (Not applicable - no new APIs)
├── contracts/           # Phase 1 output (Not applicable - no contract changes)
├── checklists/requirements.md # Quality checklist ✅ Complete
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (Web Application Monorepo)

```text
frontend/
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   ├── priority/page.tsx         # 🔧 FIX: Priority filtering logic
│   │   │   └── components/
│   │   │       ├── TodoCard.tsx          # 🔧 Theme color migration
│   │   │       ├── Sidebar.tsx           # 🔧 Theme color migration
│   │   │       ├── PriorityTabs.tsx      # 🔧 Theme color migration
│   │   │       └── DashboardNav.tsx      # 🔧 Theme color migration
│   │   ├── (auth)/
│   │   │   ├── sign-in/page.tsx          # 🔧 Theme color migration
│   │   │   └── sign-up/page.tsx          # 🔧 Theme color migration
│   │   └── globals.css                   # 🔧 Add semantic theme variables
│   ├── components/
│   │   ├── auth/
│   │   │   ├── SignInForm.tsx            # 🔧 Theme color migration
│   │   │   └── SignUpForm.tsx            # 🔧 Theme color migration
│   │   └── tasks/
│   │       ├── PriorityBadge.tsx         # 🔧 Theme color migration
│   │       ├── FilterPanel.tsx           # 🔧 Theme color migration
│   │       └── TaskForm.tsx              # 🔧 Theme color migration
│   └── lib/
│       └── validations/task.ts           # 🔧 Remove hardcoded color classes
└── tests/
    └── [Jest tests for updated components]

backend/
└── [No changes needed - filtering happens frontend]
```

**Structure Decision**: Monorepo with separate frontend/backend. This feature is **frontend-only** affecting:
- **Theme System**: `frontend/src/app/globals.css` (add semantic variables)
- **Dashboard Logic**: `frontend/src/app/dashboard/priority/page.tsx` (fix filtering)
- **Component Styling**: 8+ components for color class migration
- **Task Configuration**: `frontend/src/lib/validations/task.ts` (remove hardcoded colors)

## Phase 0: Research (None Required)

**Status**: ✅ **SKIPPED** - No technical unknowns

All technical context is clear from codebase exploration:
- Theme system fully documented (globals.css with OKLCH variables)
- Priority configuration centralized in `PRIORITY_CONFIG` (task.ts)
- Component structure well-organized (known file locations)
- Hardcoded color classes identified (bg-gray-100, text-blue-600, etc.)
- No external dependencies or integrations needed

## Phase 1: Design & Contracts

### 1.1 Theme Variable Architecture

**Current State**: CSS custom properties using OKLCH color space in `:root` and `.dark` selectors

**Semantic Variables to Add** (in `globals.css`):

Priority Badge Colors:
```css
/* Priority badge backgrounds */
--priority-high-bg: oklch(0.704 0.191 22.216);      /* Red */
--priority-medium-bg: oklch(0.822 0.131 67.202);    /* Yellow/Orange */
--priority-low-bg: oklch(0.648 0.146 258.338);      /* Blue */
--priority-none-bg: oklch(0.898 0.01 0);            /* Gray */

/* Priority badge text colors */
--priority-high-text: oklch(1 0 0);                 /* Light */
--priority-high-text-dark: oklch(0.577 0.245 27.325); /* Red foreground */
--priority-medium-text: oklch(0.141 0.005 285.823); /* Dark */
--priority-low-text: oklch(1 0 0);                  /* Light */
--priority-none-text: oklch(0.5 0 0);               /* Gray */
```

Form & Input Colors:
```css
/* Error states */
--error-bg: oklch(0.968 0.033 15.568);              /* Light red */
--error-border: oklch(0.918 0.065 15.568);          /* Medium red */
--error-text: oklch(0.577 0.245 27.325);            /* Dark red */

/* Input backgrounds */
--input-bg: var(--background);
--input-border: var(--border);
--input-text: var(--foreground);
--input-placeholder: oklch(0.7 0.02 286);           /* Lighter foreground */

/* Link colors */
--link-text: oklch(0.21 0.006 285.885);             /* Primary blue */
--link-text-hover: oklch(0.15 0.006 285.885);       /* Darker blue on hover */
```

### 1.2 Component Color Updates

**Components to Update**:

| Component | Current Colors | New Approach |
|-----------|---|---|
| PriorityBadge | Hardcoded Tailwind (bg-red-100, text-red-800) | Use `--priority-*-bg` and `--priority-*-text` variables |
| SignInForm | `border-red-200 bg-red-50 text-red-600` | Use `--error-*` variables |
| SignUpForm | `border-red-200 bg-red-50 text-red-600` | Use `--error-*` variables |
| TodoCard | `text-slate-600`, hardcoded colors | Use `--foreground` and semantic variables |
| Sidebar | `bg-slate-900 dark:bg-slate-800` | Use `--sidebar` or similar |
| FilterPanel | `bg-blue-100 text-blue-800` | Use `--priority-low-bg` and related |
| TagChip | Priority-based colors | Use semantic priority variables |
| TaskForm | `text-gray-600`, form styling | Use semantic form variables |

### 1.3 Priority Dashboard Logic Fix

**Current Issue**: `filter((t) => t.priority === p)` filters work, but display shows only High priority

**Root Cause**: Investigation needed to determine if issue is in:
1. Filter logic (unlikely - components show filtering works for other attributes)
2. Tab rendering (likely - PriorityTabs component or renderContent callback)
3. API response filtering (unlikely - backend returns all todos)

**Fix Approach**:
- Ensure PriorityTabs displays all 4 priority levels (high, medium, low, none)
- Verify renderPriorityContent() returns content for all priority levels
- Add conditional rendering for empty priority sections

### 1.4 Accessibility Compliance

**WCAG AA Standards** (4.5:1 contrast ratio for normal text):

Current Theme Colors - Light Mode:
- Foreground (oklch(0.141 0.005 285.823)) on Background (oklch(1 0 0)): ✅ ~15:1 (excellent)
- Primary (oklch(0.21 0.006 285.885)) on Background: ✅ ~12:1 (excellent)

Priority Badges - Need Verification:
- High priority text on red bg: needs contrast check
- Medium priority text on yellow bg: needs contrast check
- Low priority text on blue bg: needs contrast check

**Action**: Use contrast checker to verify all priority colors meet WCAG AA, adjust if needed.

## Complexity Tracking

> No constitution violations detected. Architecture decision made: theme migration via CSS variables only (no component restructuring).

| Decision | Rationale |
|----------|-----------|
| Frontend-only fix | Backend filtering logic not the issue; dashboard filtering happens client-side with React |
| CSS variables (not Tailwind classes) | Ensures light/dark mode consistency and WCAG AA compliance |
| Preserve component structure | No refactoring needed; only styling updates required |
