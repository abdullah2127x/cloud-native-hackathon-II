---
id: 0001
title: Create spec for priority dashboard and theme fixes
stage: spec
date: 2026-02-03T00:00:00Z
surface: feature-specification
model: claude-haiku-4-5-20251001
feature: 004-fix-priority-theme
branch: 004-fix-priority-theme
user: AbdullahQureshi
command: /sp.specify
labels: [bug-fix, ui-ux, accessibility]
links:
  spec: specs/004-fix-priority-theme/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-fix-priority-theme/spec.md
  - specs/004-fix-priority-theme/checklists/requirements.md
tests: null
---

## Prompt

# 🛠️ Todo App Issues & Required Fixes

I am facing **two major issues** in my Todo application that need to be fixed properly.

---

## 1️⃣ Priority Dashboard Issue

### Route:
`/dashboard/priority`

### ❌ Actual Behavior:
- Only **High priority** todos are displayed.
- **Medium and Low priority todos are missing**, even though they exist.

### ✅ Expected Behavior:
- Todos should be displayed **in priority order**:
  1. High
  2. Medium
  3. Low

### 🔧 Required Fix:
- Identify why **Medium** and **Low** priority todos are being excluded.
- Fix the logic so **all priority levels are shown correctly and sequentially**.

---

## 2️⃣ Theme & Styling Issues (Major UI Problems)

There are **widespread theme-related issues** across the app, mainly due to improper color handling.

### ❌ Problems Observed:
- Text and buttons appear **black and unreadable**.
- Input field text and placeholders are not visible.
- Buttons look unstyled (plain black text).
- Some forms/modals have **transparent backgrounds**, which looks broken.

---
### 📍 Affected Areas:

#### 🔐 Signin & Signup Forms
- Input text and placeholders not visible
- Buttons not styled or visible

#### 📚 Sidebar (After Login)
- Sidebar heading text not visible

#### 🚪 Footer
- Logout button appears as plain black, unstyled text

#### 📝 Todo Card
- Three-dot (⋮) menu for **Edit/Delete** not visible properly
- Tags text inside todos not readable
#### ➕ Add / ✏️ Edit Todo Form
- Form background is transparent
- Input text not visible
- Buttons not styled properly

---

## 3️⃣ Mandatory Theme Fix (Very Important)

To fix this **globally and correctly**:

### ✅ Use ShadCN Theme Variables:
- `primary`
- `secondary`
- `foreground`
- `background`
- `muted`
- etc.

### ❌ Remove Hardcoded Tailwind Colors:
Avoid classes like:
- `text-blue-500`
- `text-black`
- `bg-black`

### 🔁 Replace With:
- ShadCN semantic classes
- Theme-based variables for **consistent light & dark mode support**

---

## 🎯 Final Goal

- A **fully theme-consistent application**
- Proper visibility of **text, buttons, inputs, dropdowns, menus, and modals**
- Styling managed **only via ShadCN design system**, not hardcoded Tailwind colors

---

## Response snapshot

Created comprehensive specification for feature branch `004-fix-priority-theme`:

**Specification Details:**
- Created branch `004-fix-priority-theme` (feature #4)
- 6 user stories covering all critical issues (P1 priority for main flows, P2 for logout)
- 12 functional requirements addressing dashboard logic and theme migration
- 9 measurable success criteria with clear acceptance metrics
- 4 edge cases identified for boundary conditions
- Quality checklist completed with all items verified

**Key Focus Areas:**
1. **Priority Dashboard Bug** - Fix filtering to display all three priority levels (High, Medium, Low) in correct order
2. **Theme Migration** - Replace all hardcoded Tailwind colors with ShadCN semantic tokens (primary, secondary, foreground, background, muted)
3. **Accessibility** - Ensure WCAG AA contrast ratios (4.5:1) for all text
4. **Component Styling** - Update auth forms, sidebar, footer, todo cards, and add/edit modals for proper visibility

**Files Created:**
- `specs/004-fix-priority-theme/spec.md` - Complete feature specification
- `specs/004-fix-priority-theme/checklists/requirements.md` - Quality validation checklist
- `history/prompts/004-fix-priority-theme/0001-create-spec.spec.prompt.md` - PHR record

**Status:** ✅ Specification complete and validated. Ready for planning phase (`/sp.plan`).

## Outcome

- ✅ Impact: Specification provides clear user value (fix critical dashboard bug, improve UI/UX accessibility, implement consistent theming)
- 🧪 Tests: All user scenarios have acceptance criteria; all requirements are testable
- 📁 Files: spec.md, requirements.md checklist, PHR record created
- 🔁 Next prompts: `/sp.plan` to design implementation approach
- 🧠 Reflection: User input clearly identified two distinct but intertwined issues (logic bug + styling system refactor). Specification separates concerns while acknowledging interdependencies. Success criteria are measurable and verifiable without implementation details.

## Evaluation notes (flywheel)

- Failure modes observed: None - user provided clear, detailed problem statement with specific examples of affected components
- Graders run and results (PASS/FAIL): N/A - spec generation does not require grading
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Move to planning phase to determine technical approach
