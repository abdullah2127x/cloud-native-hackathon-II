# Theme System Documentation

**Task**: T073 - Create theme usage guide documenting all semantic variables

## Overview

This application uses a comprehensive CSS custom properties (CSS variables) theming system to provide consistent, accessible, and theme-aware styling across all components. The theme automatically adapts to light and dark modes without requiring component-level theme switching logic.

## Theme Variables Location

All theme variables are defined in:
- **File**: `frontend/src/app/globals.css`
- **Light Mode**: `:root` selector (lines 49-108)
- **Dark Mode**: `.dark` selector (lines 110-168)

## Color Semantic Tokens

### Foreground & Background
- `--foreground`: Primary text color (dark in light mode, light in dark mode)
- `--muted-foreground`: Secondary/disabled text color
- `--background`: Page background
- `--card`: Card/container background
- `--muted`: Muted/disabled background

### Input & Form Fields
- `--input-bg`: Input field background
- `--input-border`: Input field border
- `--input-text`: Input field text color
- `--input-placeholder`: Placeholder text color

### Interactive States
- `--primary`: Primary action color
- `--primary-foreground`: Primary text on primary background
- `--border`: Subtle borders and separators
- `--destructive`: Error/delete actions

### Error Handling
- `--error-bg`: Error message background
- `--error-border`: Error message border
- `--error-text`: Error message text

### Link Styling
- `--link-text`: Link text color
- `--link-text-hover`: Link text on hover

### Priority Badges
Each priority level has two variables for background and text:
- `--priority-high-bg` / `--priority-high-text` (Red)
- `--priority-medium-bg` / `--priority-medium-text` (Yellow)
- `--priority-low-bg` / `--priority-low-text` (Green)
- `--priority-none-bg` / `--priority-none-text` (Gray)

## Component-Specific Usage

### Form Components

**Input Fields, Textareas, Selects**:
```tsx
<input
  className="border px-3 py-2"
  style={{
    backgroundColor: "var(--input-bg)",
    borderColor: "var(--input-border)",
    color: "var(--input-text)",
  }}
  onFocus={(e) => {
    e.currentTarget.style.borderColor = "var(--primary)";
    e.currentTarget.style.boxShadow = "0 0 0 1px var(--primary)";
  }}
  onBlur={(e) => {
    e.currentTarget.style.borderColor = "var(--input-border)";
  }}
/>
```

**Form Labels**:
```tsx
<label style={{ color: "var(--foreground)" }}>
  Field Label
</label>
```

**Error Messages**:
```tsx
<p style={{ color: "var(--error-text)" }}>
  Error message
</p>
```

### Badge & Status Components

**Priority Badge**:
```tsx
<span
  style={{
    backgroundColor: "var(--priority-high-bg)",
    color: "var(--priority-high-text)",
  }}
>
  High
</span>
```

**Tag Chip**:
```tsx
<span
  style={{
    backgroundColor: "var(--primary)",
    color: "var(--primary-foreground)",
    borderColor: "var(--border)",
  }}
>
  Tag Name
</span>
```

### Card & Container Components

**Card Background & Border**:
```tsx
<div
  style={{
    backgroundColor: "var(--card)",
    borderColor: "var(--border)",
  }}
>
  {/* content */}
</div>
```

### Navigation Components

**Sidebar & Links**:
```tsx
<button
  style={{
    color: isActive ? "var(--primary-foreground)" : "var(--muted-foreground)",
    backgroundColor: isActive ? "var(--primary)" : "transparent",
  }}
>
  Navigation Link
</button>
```

### Modal & Dialog

**Dialog Content**:
```tsx
<div style={{ backgroundColor: "var(--background)" }}>
  {/* Modal content */}
</div>
```

Note: Modal overlay opacity (bg-black/50) is hardcoded for consistent visual effect.

## WCAG AA Compliance

All color combinations have been verified to meet WCAG AA contrast ratio requirements (4.5:1 minimum):

- Foreground text on background: ✓ 7.5:1+
- Foreground text on card: ✓ 7.5:1+
- Error text on error background: ✓ 4.5:1+
- All priority badges: ✓ 4.5:1+ (adjusted in Phase 1, Task T003)

Verification details: See `specs/004-fix-priority-theme/contrast-verification.md`

## Migration Guide

### From Hardcoded Tailwind Classes to CSS Variables

**Before** (Hardcoded):
```tsx
<div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
  <p className="text-slate-900 dark:text-white">
    Content
  </p>
</div>
```

**After** (CSS Variables):
```tsx
<div
  className="border"
  style={{
    backgroundColor: "var(--card)",
    borderColor: "var(--border)",
  }}
>
  <p style={{ color: "var(--foreground)" }}>
    Content
  </p>
</div>
```

### Implementation Checklist

When updating components to use theme variables:

1. ✅ Replace hardcoded `bg-` classes with `style={{ backgroundColor: "var(--*)" }}`
2. ✅ Replace hardcoded `text-` classes with `style={{ color: "var(--*)" }}`
3. ✅ Replace hardcoded `border-` classes with `style={{ borderColor: "var(--*)" }}`
4. ✅ Add focus/hover state handlers for interactive elements
5. ✅ Test in both light and dark modes
6. ✅ Verify contrast ratios in both modes

## Light & Dark Mode Values

### Light Mode (:root)

Key colors in OKLCH color space:
- Foreground: oklch(0.141 0.005 285.823) - Dark navy/black
- Background: oklch(1 0 0) - Pure white
- Primary: oklch(0.21 0.006 285.885) - Deep purple
- Border: oklch(0.92 0.004 286.32) - Light gray

### Dark Mode (.dark)

Key colors in OKLCH color space:
- Foreground: oklch(65.159% 0.0532 18.54) - Light cream
- Background: oklch(0.141 0.005 285.823) - Dark navy/black
- Primary: oklch(0.92 0.004 286.32) - Light purple
- Border: oklch(1 0 0 / 10%) - Subtle white overlay

## Browser Support

CSS custom properties are supported in all modern browsers:
- Chrome/Edge 49+
- Firefox 31+
- Safari 9.1+
- Mobile browsers: Supported on all modern versions

## Accessibility Features

1. **Automatic Theme Adaptation**: Components automatically adapt colors when dark mode is enabled
2. **High Contrast**: All text meets WCAG AA standards
3. **Focus Indicators**: Input fields show primary color on focus for clear visual feedback
4. **Semantic Naming**: Variable names clearly indicate their purpose
5. **Reduced Motion**: Theme changes respect user's system preferences (no animations)

## Testing Theme Changes

### Manual Testing Steps

1. **Light Mode Verification**:
   - Navigate through all pages
   - Verify all text is readable
   - Check form inputs are visible
   - Confirm button states are clear

2. **Dark Mode Verification**:
   - Enable dark mode (system preferences or app toggle)
   - Repeat light mode checks
   - Verify borders are visible
   - Check that error states are visible

3. **Responsive Testing**:
   - Test on mobile, tablet, desktop
   - Verify theme variables work on all screen sizes
   - Check hover states work on devices that support them

4. **Accessibility Audit**:
   - Run contrast checker (WebAIM)
   - Verify keyboard navigation
   - Test with screen reader
   - Check focus indicators are visible

## Common Issues & Solutions

### Issue: Colors look wrong in dark mode
**Solution**: Check that CSS variables are properly closed with `var(--variable-name)`. Verify dark mode class (`.dark`) is applied to root element.

### Issue: Focus states not visible
**Solution**: Ensure `onFocus` handler updates border and box-shadow. Example:
```tsx
onFocus={(e) => {
  e.currentTarget.style.borderColor = "var(--primary)";
  e.currentTarget.style.boxShadow = "0 0 0 1px var(--primary)";
}}
```

### Issue: Hover states don't work
**Solution**: Use `onMouseEnter`/`onMouseLeave` for mouse states or CSS :hover pseudo-class in className.

## Future Enhancements

- [ ] Add theme selector UI for user preferences
- [ ] Support system color scheme preferences
- [ ] Add high contrast mode option
- [ ] Create additional color themes (blue, green, etc.)
- [ ] Implement theme persistence in localStorage

## Related Files

- **Core Theme**: `frontend/src/app/globals.css`
- **Priority Colors**: `frontend/src/lib/priority-colors.ts`
- **Task Validation**: `frontend/src/lib/validations/task.ts`
- **Test Utilities**: `frontend/__tests__/utils/theme-colors.test.ts`
- **Theme Variables Reference**: `specs/004-fix-priority-theme/theme-variables.md`
- **Contrast Verification**: `specs/004-fix-priority-theme/contrast-verification.md`

## Implementation Details

### CSS Custom Properties (Variables)

CSS variables use the `var()` function with fallback support:
```css
color: var(--foreground, #333); /* #333 is fallback if not defined */
```

However, in this implementation, all variables are guaranteed to be defined in either `:root` or `.dark` selectors, so fallbacks are not necessary.

### Color Space: OKLCH

This theme uses OKLCH color space instead of RGB/HEX:
- **O**: Oklab lightness (0-1)
- **K**: Chroma (0-0.37)
- **L**: Hue (0-360)
- **H**: Optional hue channel

Benefits:
- Perceptually uniform color differences
- Better dark mode color matching
- Natural color transitions

## Maintenance

### Adding New Variables

When adding new theme variables:

1. Define in `:root` for light mode
2. Define in `.dark` for dark mode
3. Document in this file
4. Update theme-variables.md reference
5. Test contrast ratios if color-related
6. Update components to use new variable

### Updating Existing Variables

1. Update both `:root` and `.dark` selectors
2. Search for components using old hardcoded values
3. Update components to use CSS variable
4. Verify contrast ratios still meet WCAG AA
5. Test in all components using the variable
6. Update documentation

---

**Last Updated**: February 3, 2026
**Implementation Phase**: 004-fix-priority-theme, Tasks T001-T073
**WCAG Compliance**: AA (4.5:1 minimum contrast ratio)
