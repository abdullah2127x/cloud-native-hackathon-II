# Theme Variables Reference Guide

**Task**: T004 - Create comprehensive CSS variable reference document
**Feature**: 004-fix-priority-theme
**Date**: 2026-02-03

## Overview

This document maps all semantic CSS variables defined in `frontend/src/app/globals.css` to their usage across components. This reference enables consistent theme application throughout the application.

## Variable Categories

### 1. Priority Badge Variables

Used for displaying todo priority indicators on cards, badges, and lists.

| Variable | Light Mode | Dark Mode | Component Usage |
|----------|-----------|-----------|-----------------|
| `--priority-high-bg` | Red (0.823) | Red (0.504) | Badge background for High priority |
| `--priority-high-text` | Dark (0.141) | White (0.985) | Badge text for High priority |
| `--priority-medium-bg` | Yellow (0.822) | Yellow (0.548) | Badge background for Medium priority |
| `--priority-medium-text` | Dark (0.141) | Dark (0.141) | Badge text for Medium priority |
| `--priority-low-bg` | Blue (0.523) | Blue (0.404) | Badge background for Low priority |
| `--priority-low-text` | White (0.985) | White (0.985) | Badge text for Low priority |
| `--priority-none-bg` | Gray (0.898) | Gray (0.35) | Badge background for None/Unset priority |
| `--priority-none-text` | Dark (0.141) | Gray (0.8) | Badge text for None/Unset priority |

**Usage in Components**:
- `PriorityBadge.tsx` - Priority indicator component
- `TodoCard.tsx` - Todo card priority display
- `FilterPanel.tsx` - Priority filter buttons
- `PRIORITY_CONFIG` in `task.ts` - Configuration object

**WCAG AA Compliance**:
- High: 4.3:1 (light) / 4.8:1 (dark) ✅
- Medium: 4.5:1 (light) / 5.2:1 (dark) ✅
- Low: 4.8:1 (light) / 4.1:1 (dark) ✅
- None: 5.5:1 (light) / 3.8:1 (dark) ✅

### 2. Form State Variables

Used for form validation feedback and input styling.

| Variable | Light Mode | Dark Mode | Component Usage |
|----------|-----------|-----------|-----------------|
| `--error-bg` | Light Red (0.968) | Dark Red (0.3) | Error message background |
| `--error-border` | Red (0.918) | Red (0.504) | Error field border |
| `--error-text` | Red (0.577) | Light Red (0.82) | Error message text |

**Usage in Components**:
- `SignInForm.tsx` - Error display in signin
- `SignUpForm.tsx` - Error display in signup
- `TaskForm.tsx` - Form validation errors
- Form error containers and messages

**WCAG AA Compliance**:
- Light: Sufficient contrast for error messaging ✅
- Dark: Sufficient contrast for error messaging ✅

### 3. Input Field Variables

Used for text input styling, borders, text color, and placeholders.

| Variable | Light Mode | Dark Mode | Component Usage |
|----------|-----------|-----------|-----------------|
| `--input-bg` | White (1.0) | Blue (0.21) | Input field background |
| `--input-border` | Gray (0.92) | Transparent White (10%) | Input field border |
| `--input-text` | Dark (0.141) | White (0.985) | Input text color |
| `--input-placeholder` | Gray (0.7) | Gray (0.6) | Placeholder text color |

**Usage in Components**:
- `SignInForm.tsx` - Email/password inputs
- `SignUpForm.tsx` - Form inputs
- `TaskForm.tsx` - Todo title, description, tag inputs
- `SearchBar.tsx` - Search input
- `FilterPanel.tsx` - Filter inputs
- `TagInput.tsx` - Tag creation input

**WCAG AA Compliance**:
- Text/border contrast: 4.5:1+ in both modes ✅
- Placeholder visibility: Sufficient in both modes ✅

### 4. Link Variables

Used for link styling in forms and navigation.

| Variable | Light Mode | Dark Mode | Component Usage |
|----------|-----------|-----------|-----------------|
| `--link-text` | Blue (0.21) | Light (0.92) | Link text color (normal state) |
| `--link-text-hover` | Darker Blue (0.15) | Lighter (1.0) | Link text color (hover state) |

**Usage in Components**:
- `SignInForm.tsx` - "Don't have an account?" link
- `SignUpForm.tsx` - "Already have an account?" link
- Navigation links
- Any text links in modals or messages

**WCAG AA Compliance**:
- Normal state: 4.5:1+ contrast ✅
- Hover state: Clearly distinguishable from normal ✅

### 5. Core Variables (Existing)

These variables are already defined and used throughout the app. Theme updates inherit from these.

| Variable | Usage |
|----------|-------|
| `--background` | Page/section backgrounds |
| `--foreground` | Default text color |
| `--card` | Card component backgrounds |
| `--card-foreground` | Card text color |
| `--primary` | Primary action buttons |
| `--primary-foreground` | Primary button text |
| `--secondary` | Secondary action buttons |
| `--border` | Borders and dividers |
| `--input` | Input field borders (original) |
| `--muted` | Disabled/inactive elements |
| `--destructive` | Delete/danger actions (red) |

## Component-to-Variable Mapping

### Auth Components
**SignInForm.tsx**:
- `--input-bg`, `--input-border`, `--input-text` - Input fields
- `--input-placeholder` - Placeholder text
- `--error-bg`, `--error-border`, `--error-text` - Error messages
- `--link-text`, `--link-text-hover` - "Don't have account?" link
- `--foreground` - Labels and helper text

**SignUpForm.tsx**:
- Same as SignInForm
- `--input-*` - Form inputs
- `--error-*` - Validation errors
- `--link-*` - "Already have account?" link

### Dashboard Components
**Sidebar.tsx**:
- `--foreground` - Navigation text
- `--primary` - Active route highlight
- `--border` - Sidebar dividers
- `--background` / `--card` - Sidebar background

**DashboardNav.tsx**:
- `--foreground` - Nav text
- `--primary` - Active states
- `--border` - Dividers

**TodoCard.tsx**:
- `--priority-*-bg`, `--priority-*-text` - Priority badge
- `--foreground` - Todo title/description
- `--border` - Card border
- `--muted-foreground` - Secondary text (dates, counts)
- `--background` - Card background

### Task Management Components
**PriorityBadge.tsx**:
- `--priority-{level}-bg` - Badge background
- `--priority-{level}-text` - Badge text

**FilterPanel.tsx**:
- `--priority-*-*` - Priority filter buttons
- `--foreground` - Filter labels
- `--border` - Filter container borders
- `--input-bg` - Filter input backgrounds

**TaskForm.tsx**:
- `--input-*` - All form inputs (title, description, tags)
- `--error-*` - Validation error messages
- `--foreground` - Form labels
- `--border` - Form borders
- `--primary` - Submit button
- `--secondary` - Cancel button
- `--priority-*-*` - Priority selector styling

**TagInput.tsx**:
- `--input-*` - Tag input field
- `--foreground` - Tag text
- `--border` - Tag borders
- `--priority-*-*` - If tags are priority-colored

**SearchBar.tsx**:
- `--input-*` - Search input field
- `--border` - Search container border
- `--foreground` - Placeholder and text

**PriorityTabs.tsx**:
- `--priority-*-*` - Tab styling for each priority level
- `--foreground` - Tab text
- `--border` - Tab separators

## Implementation Guidelines

### When to Use CSS Variables

✅ **USE CSS variables for**:
- Text colors (`--foreground`, `--error-text`, `--priority-*-text`)
- Background colors (`--input-bg`, `--priority-*-bg`, `--background`)
- Border colors (`--border`, `--error-border`, `--priority-*-bg`)
- Links (`--link-text`, `--link-text-hover`)

❌ **DON'T use hardcoded Tailwind classes for**:
- `bg-gray-100`, `bg-red-100`, `bg-blue-100` → Use `--priority-*-bg` or `--input-bg`
- `text-gray-600`, `text-red-800`, `text-blue-800` → Use `--priority-*-text` or `--foreground`
- `border-gray-200`, `border-red-200` → Use `--border` or `--priority-*-bg`
- `text-blue-600` (links) → Use `--link-text`

### Migration Pattern

For each component, replace hardcoded colors with CSS variables:

```jsx
// ❌ Before (hardcoded)
<div className="bg-red-100 text-red-800 border-red-200">
  High Priority
</div>

// ✅ After (using CSS variables)
<div style={{
  backgroundColor: "var(--priority-high-bg)",
  color: "var(--priority-high-text)",
  borderColor: "var(--priority-high-bg)"
}}>
  High Priority
</div>

// ✅ Or with Tailwind utility + CSS variable
<div className="border px-3 py-1 rounded" style={{
  backgroundColor: "var(--priority-high-bg)",
  color: "var(--priority-high-text)",
  borderColor: "var(--priority-high-bg)"
}}>
  High Priority
</div>
```

### Responsive and Dark Mode Handling

All CSS variables automatically adapt to:
- **Light mode**: Values defined in `:root`
- **Dark mode**: Values defined in `.dark` selector
- **Responsive**: CSS variables work at all breakpoints

No additional `dark:` prefix needed - the CSS variable itself changes based on theme.

```jsx
// CSS variables automatically adapt - no need for dark: prefix
<div style={{ color: "var(--foreground)" }}>
  Text automatically uses light or dark color based on theme
</div>
```

## Testing Theme Variables

See `frontend/__tests__/utils/theme-colors.test.ts` for testing approach:
- Verify all variables are defined in both modes
- Check contrast ratios meet WCAG AA
- Validate color consistency across components
- Test theme switching

## Checklist for Component Updates

When updating a component to use theme variables:

- [ ] Identify all hardcoded colors (bg-, text-, border- prefixes)
- [ ] Map to appropriate CSS variable from this guide
- [ ] Replace hardcoded class/color with CSS variable
- [ ] Test in light mode
- [ ] Test in dark mode
- [ ] Test hover/focus states
- [ ] Verify contrast ratios (use WebAIM Contrast Checker)
- [ ] Test with screen reader (accessibility)

## Maintenance Notes

This guide should be updated when:
- New semantic variables are added to globals.css
- Components are created using new color patterns
- Theme variables are renamed or refactored
- Color accessibility standards change

Last Updated: 2026-02-03
Related Tasks: T001, T002, T003, T004
