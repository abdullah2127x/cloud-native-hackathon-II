# Feature Specification: Fix Priority Dashboard and Comprehensive Theme Styling

**Feature Branch**: `004-fix-priority-theme`
**Created**: 2026-02-03
**Status**: Draft
**Input**: User description: Two critical issues - (1) Priority dashboard only shows High priority todos; Medium and Low are missing; (2) Widespread theme-related issues with text/buttons appearing black and unreadable, input fields invisible, forms transparent, requiring comprehensive ShadCN theme variable integration

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - View All Priority Levels in Dashboard (Priority: P1)

As a todo user, I want to see all my todos organized by priority level (High, Medium, Low) so that I can view my complete workload without missing items.

**Why this priority**: This is a critical functional bug affecting the priority dashboard. Users cannot see Medium and Low priority items, causing them to miss important tasks. This directly impacts the core value of the application.

**Independent Test**: Navigate to the priority dashboard and verify that all three priority levels display their respective todos in the correct order. This demonstrates the fix works independently.

**Acceptance Scenarios**:

1. **Given** a user has High, Medium, and Low priority todos, **When** they navigate to `/dashboard/priority`, **Then** all three priority groups display with todos listed under each priority level
2. **Given** the dashboard is displayed, **When** the page loads, **Then** priorities appear in order: High (first), Medium (second), Low (third)
3. **Given** a user creates a new Low priority todo, **When** they view the dashboard, **Then** the new todo appears in the Low priority section immediately

---

### User Story 2 - Read Text and Interact with Components in Auth Forms (Priority: P1)

As a new user, I want the signin and signup forms to be readable and usable with proper text contrast and styled input fields so that I can log in to the application.

**Why this priority**: Auth forms are the gateway to the application. If text is invisible and inputs are unstyled, users cannot sign in or create accounts, making the entire app inaccessible.

**Independent Test**: Navigate to signin/signup pages and verify all text is readable, inputs are visible and functional, and buttons are properly styled. This demonstrates auth accessibility works independently.

**Acceptance Scenarios**:

1. **Given** a user visits the signin page, **When** the page loads, **Then** all labels, input placeholders, and button text are visible and readable with sufficient contrast
2. **Given** a user is on the signup form, **When** they focus on an input field, **Then** the cursor is visible and text they type appears clearly
3. **Given** a user is ready to submit the auth form, **When** they look at the submit button, **Then** it is clearly styled and visually distinct from the rest of the page

---

### User Story 3 - Navigate and Read Sidebar Content After Login (Priority: P1)

As a logged-in user, I want to see the sidebar navigation with readable headings and links so that I can navigate between dashboard views.

**Why this priority**: The sidebar is essential for navigation after login. If headings are not visible, users cannot navigate the application effectively.

**Independent Test**: Log in successfully and verify sidebar headings, links, and labels are all readable. This demonstrates post-login navigation is accessible independently.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they view the sidebar, **Then** all headings and navigation text are clearly visible
2. **Given** the sidebar is displayed, **When** a user looks at navigation links, **Then** links are styled consistently and distinguish active routes from inactive ones
3. **Given** a user hovers over sidebar items, **When** they interact with them, **Then** hover states are visible and indicate interactivity

---

### User Story 4 - View and Edit Todo Cards with Visible Menus (Priority: P1)

As a todo user, I want to see todo cards with readable content and accessible edit/delete menus so that I can manage my todos.

**Why this priority**: Todo cards are the core content. If text is invisible and action menus are not visible, users cannot read or edit their todos.

**Independent Test**: View a list of todos and verify titles, descriptions, tags, and action menus are all visible and interactive. This demonstrates todo management works independently.

**Acceptance Scenarios**:

1. **Given** a user views their todo list, **When** they look at a todo card, **Then** the title, description, and tags are all readable
2. **Given** a user wants to edit a todo, **When** they click the three-dot menu on a todo card, **Then** the menu appears visibly with Edit and Delete options
3. **Given** a user is viewing tag information, **When** they look at tags on a todo, **Then** tag text and backgrounds provide clear contrast and readability

---

### User Story 5 - Use Add and Edit Todo Forms with Visible Inputs (Priority: P1)

As a todo user, I want to see all form fields, labels, and buttons when creating or editing todos so that I can input data confidently.

**Why this priority**: Add/edit forms are critical for todo management. If inputs are invisible or forms have transparent backgrounds, users cannot complete these actions.

**Independent Test**: Open add/edit todo modal and verify all form elements are visible, inputs accept text, and buttons are clearly styled. This demonstrates form functionality works independently.

**Acceptance Scenarios**:

1. **Given** a user opens the add todo form, **When** the modal appears, **Then** the background is opaque and all form fields are visible
2. **Given** a user is filling out the form, **When** they type in an input field, **Then** the text appears clearly and is not black on dark background
3. **Given** a user is ready to save, **When** they look at the save button, **Then** it is clearly styled, readable, and distinguishable from the cancel button

---

### User Story 6 - Log Out with Clear Visual Feedback (Priority: P2)

As a logged-in user, I want the logout button in the footer to be clearly visible and styled so that I can safely exit my session.

**Why this priority**: Logout is important for account security, but less critical than the main content areas. Users need to see it, but if they can't find it initially, they can scroll or search.

**Independent Test**: Find and click the logout button, verify it is styled clearly and executes logout correctly. This demonstrates logout functionality works independently.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they view the footer, **Then** the logout button is visible and styled like other interactive elements
2. **Given** a user clicks the logout button, **When** the action completes, **Then** they are redirected to the signin page and session is cleared

### Edge Cases

- What happens when a user has zero todos in a priority level? (The priority section should still display but with "No todos" message if needed)
- How does the application handle users viewing the priority dashboard with todos but all in only one priority level? (Other priority sections should display but be empty)
- What happens when switching between light and dark themes? (All theme colors must update consistently across the entire application)
- How are readonly vs editable form states visually distinguished? (Should use theme-appropriate styling without relying on color alone)

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST display all three priority levels (High, Medium, Low) on the priority dashboard
- **FR-002**: System MUST sort and display todos by priority in the correct order (High → Medium → Low)
- **FR-003**: System MUST ensure all text throughout the application uses theme-appropriate foreground colors that meet accessibility contrast ratios (WCAG AA standard minimum 4.5:1 for normal text)
- **FR-004**: System MUST apply theme-aware background colors to all input fields so text is visible
- **FR-005**: System MUST style all buttons using semantic theme classes (primary, secondary, etc.) instead of hardcoded colors
- **FR-006**: System MUST ensure form backgrounds are opaque and use theme-appropriate background colors
- **FR-007**: System MUST apply theme variables to all UI components (sidebars, modals, dropdowns, menus)
- **FR-008**: System MUST remove all hardcoded Tailwind color classes (text-black, bg-black, text-blue-500, etc.) from components
- **FR-009**: System MUST replace hardcoded colors with ShadCN semantic tokens (primary, secondary, foreground, background, muted, etc.)
- **FR-010**: System MUST ensure dropdown menus and popover menus are visually distinct and readable
- **FR-011**: System MUST apply consistent theme styling to tag components on todo cards
- **FR-012**: System MUST maintain theme consistency across light and dark mode variants

### Key Entities *(include if feature involves data)*

- **Priority**: Represents todo urgency level (High, Medium, Low) - affects sorting and display order on dashboard
- **Todo**: Core entity with title, description, priority, tags - must render with proper theme styling
- **Theme**: Application-wide design system using ShadCN variables for colors and styling

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 100% of todos across all priority levels (High, Medium, Low) display on the priority dashboard with none filtered out
- **SC-002**: All text throughout the application meets WCAG AA contrast ratio minimum of 4.5:1 for normal text
- **SC-003**: Users can successfully complete signin, signup, and todo operations without encountering visibility issues
- **SC-004**: All form input fields display with visible text and placeholder text when focused
- **SC-005**: Zero hardcoded color classes (text-black, bg-black, text-*-500, etc.) remain in active component code
- **SC-006**: 100% of UI components use ShadCN theme variables instead of hardcoded Tailwind colors
- **SC-007**: Theme changes (light/dark mode) apply consistently across all components without manual refresh
- **SC-008**: All interactive elements (buttons, links, menus) are visually distinguishable with proper hover and active states using theme colors
- **SC-009**: Modals and forms display with opaque, themed backgrounds rather than transparent backgrounds

## Assumptions

- ShadCN UI component library is already installed and configured in the frontend
- The application currently uses Tailwind CSS with ShadCN color tokens available
- The priority filtering bug in the dashboard endpoint only affects High priority display, not the data layer itself
- Users are accessing the application via modern browsers with CSS support for CSS variables
- Light and dark mode switching is already implemented via theme provider/context

## Non-Goals

- Restructuring the component architecture
- Refactoring component logic beyond what's needed to fix styling
- Adding new features or dashboard views
- Changing the data model for todos or priorities
- Implementing new authentication methods
- Adding new form fields or validation rules

## Dependencies

- ShadCN UI component library must be available
- Tailwind CSS configuration must include color token customization
- Theme context/provider must be implemented in the application
- Frontend application stack is Next.js with TypeScript

## Out of Scope

- Backend API modifications (unless priority filtering is backend-driven)
- Database schema changes
- Authentication system changes
- Adding new priority levels beyond High, Medium, Low
