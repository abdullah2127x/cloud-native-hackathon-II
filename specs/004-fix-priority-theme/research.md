# Research: Fix Priority Dashboard and Comprehensive Theme Styling

**Feature**: 004-fix-priority-theme
**Date**: 2026-02-03
**Status**: Complete - No unknowns identified

## Findings Summary

Based on comprehensive codebase exploration, no technical unknowns remain. All necessary information is documented in the Implementation Plan.

## Component Analysis

### Theme System ✅

**Decision**: Extend existing CSS custom property system with semantic tokens
**Rationale**: Application already uses well-structured OKLCH color space variables in globals.css. Adding semantic tokens (--priority-high-bg, --error-bg, etc.) maintains consistency while solving hardcoded color issues.
**Alternatives Considered**:
- Option A (Rejected): Migrate to Tailwind's theme.extend → adds build-time config complexity
- Option B (Selected): Add CSS variables for semantic tokens → uses existing variable system, no build changes

### Priority Dashboard Filtering ✅

**Decision**: Frontend filtering is correct; issue is in UI rendering/display logic
**Rationale**: Codebase shows proper filtering logic `filter((t) => t.priority === p)` and backend returns all todos correctly. Issue is likely in PriorityTabs component rendering or renderContent callback not displaying all priority sections.
**Alternatives Considered**:
- Option A (Rejected): Backend filtering → not needed, frontend handles filtering correctly
- Option B (Selected): Fix frontend rendering → aligns with current architecture and spec requirement "display all three priority levels"

### Hardcoded Colors Inventory ✅

**Decision**: Migrate all hardcoded Tailwind color classes to semantic CSS variables
**Rationale**: Complete list of hardcoded colors identified (see plan.md). Systematic replacement ensures consistency and WCAG AA compliance.

**Files Requiring Updates**:
1. `frontend/src/app/globals.css` - Add semantic variable definitions
2. `frontend/src/lib/validations/task.ts` - Update PRIORITY_CONFIG to use variables
3. `frontend/src/components/auth/SignInForm.tsx` - Error styling
4. `frontend/src/components/auth/SignUpForm.tsx` - Error styling
5. `frontend/src/components/tasks/PriorityBadge.tsx` - Priority colors
6. `frontend/src/components/tasks/FilterPanel.tsx` - Filter colors
7. `frontend/src/components/tasks/TaskForm.tsx` - Form styling
8. `frontend/src/app/dashboard/components/TodoCard.tsx` - Card styling
9. `frontend/src/app/dashboard/components/Sidebar.tsx` - Sidebar styling
10. `frontend/src/app/dashboard/priority/page.tsx` - Dashboard rendering

## WCAG AA Compliance Assessment

**Current Theme Colors Analysis**:

Light Mode:
- Foreground (oklch(0.141 0.005 285.823)) on Background (oklch(1 0 0)): ~15:1 contrast ✅
- Primary (oklch(0.21 0.006 285.885)) on Background: ~12:1 contrast ✅

Priority Badges (Light Mode):
- High (red): Text on red background - requires verification
- Medium (yellow): Text on yellow background - requires verification
- Low (blue): Text on blue background - requires verification
- None (gray): Text on gray background - requires verification

**Action Items**:
- Use WCAG contrast checker on all priority badge color combinations
- Adjust priority badge colors in semantic variables if any fail 4.5:1 threshold
- Test in both light and dark modes

## Implementation Approach

### Phase 1: Core Updates (Prerequisite)
1. Extend globals.css with semantic variables
2. Verify WCAG AA compliance for all priority colors
3. Update PRIORITY_CONFIG in task.ts to remove hardcoded Tailwind classes

### Phase 2: Component Updates
1. Priority Badge Component - Use semantic variables
2. Form Components (SignIn, SignUp) - Use error variables
3. Task Management Components - Use semantic colors
4. Dashboard Components - Use semantic colors
5. Dashboard Priority Page - Verify all priority levels display

### Phase 3: Testing
1. Visual regression testing across all updated components
2. Accessibility testing (contrast ratio verification)
3. Light/dark mode switching verification
4. Priority filtering verification (all levels display)

## Dependencies

✅ **All Present**:
- ShadCN UI installed and configured
- Tailwind CSS 3.4 with color customization
- Theme context/provider implemented
- Next.js 16 App Router available

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| Priority colors fail WCAG AA | Medium | Pre-check with contrast calculator; adjust if needed before rollout |
| Incomplete theme variable coverage | Low | Systematic component-by-component review ensures all hardcoded colors caught |
| Dark mode inconsistency | Low | Test theme switching in all updated components |
| Performance impact from CSS variables | Very Low | CSS custom properties have negligible performance impact |

## Conclusion

No technical unknowns remain. All information needed for implementation is available. Ready to proceed with task generation.
