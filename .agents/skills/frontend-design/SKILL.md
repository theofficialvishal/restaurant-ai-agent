---
name: frontend-design
description: Design and implement polished, production-ready frontend UI for the current project. Use automatically whenever a feature involves creating, modifying, redesigning, styling, or improving a page, screen, layout, component, form, table, dashboard, navigation, modal, responsive behavior, frontend interaction, or visual state.
allowed-tools: Read, Write, Glob, Bash
---

# Frontend Design

Design and implement frontend UI that is consistent with the project's existing product, technology, architecture, and design system.

This is a specialized frontend skill. It does not define feature requirements or replace the main build workflow. The approved specification and plan remain the source of truth for what the feature must do.

Use `GEMINI.md` and the existing codebase to determine how the frontend should be implemented.

---

## 1. Read project context first

Before making frontend changes, read:

1. `GEMINI.md`
2. The approved feature specification, when one exists
3. The approved implementation plan, when one exists
4. Existing frontend documentation/design context
5. Relevant existing pages, components, styles, assets, and frontend logic

Do not assume a specific frontend framework, CSS system, component library, icon library, or folder structure.

Use only the technologies and conventions established by the project.

---

## 2. Inspect the existing UI before creating anything

When existing frontend code is available, inspect representative existing UI before generating new UI.

Look for and reuse:

- color/design tokens
- spacing scale
- typography and type scale
- border-radius conventions
- shadows/elevation
- buttons and form controls
- cards, tables, modals, navigation, and other reusable components
- page/container widths
- grid and layout patterns
- responsive breakpoints
- icons and icon usage
- interaction patterns
- loading, empty, error, and success states

The goal is visual consistency.

Do not create a new visual language when the project already has one.

---

## 3. Follow the project's frontend architecture

Determine from `GEMINI.md` and the codebase:

- frontend framework
- rendering model
- component architecture
- routing
- styling approach
- state management
- data fetching
- form handling
- validation
- asset management
- testing approach
- accessibility conventions

Follow the established architecture.

Do not introduce React, Vue, Angular, Tailwind, Bootstrap, CSS-in-JS, a new component library, or another framework simply because it is familiar or convenient.

Only introduce a new technology when the approved plan and project context support it.

---

## 4. Design from the approved requirements

The approved specification defines required behavior.

The frontend implementation should translate those requirements into clear UI.

Before coding, identify:

- primary user goal
- main content/sections
- required actions
- required data
- validation rules
- success/error behavior
- empty states
- loading states
- responsive requirements
- accessibility requirements

Do not add major product behavior that is not in the approved requirements.

Small visual decisions may follow the existing design system.

Material UX or product decisions should not be invented.

---

## 5. Build reusable UI where appropriate

Prefer existing reusable components over duplicating UI.

When a new component is genuinely reusable, follow the project's existing component organization and conventions.

Keep component responsibilities clear.

Avoid premature abstraction.

Do not create a generic design-system component for a one-off element unless the project already follows that pattern.

---

## 6. Visual design principles

When the project does not provide a specific design rule, prefer:

- clear visual hierarchy
- consistent spacing
- restrained use of color
- readable typography
- sufficient whitespace
- obvious primary actions
- clear secondary actions
- predictable interaction patterns
- accessible contrast
- responsive layouts
- minimal visual noise

Do not use decorative complexity merely to make a screen look impressive.

A polished UI should feel intentional rather than over-designed.

---

## 7. Responsive behavior

Treat responsive behavior as part of the implementation, not as a later patch.

Consider:

- narrow mobile widths
- tablet layouts
- desktop layouts
- content wrapping
- navigation behavior
- form stacking
- table overflow
- modal sizing
- touch targets
- long text
- empty and error states

Follow existing project breakpoints when they exist.

Do not invent a new breakpoint system when the project already has one.

---

## 8. Accessibility

Follow the project's existing accessibility conventions.

At minimum, consider:

- semantic HTML/equivalent semantic elements
- labels for form controls
- keyboard accessibility
- visible focus states
- meaningful button/link labels
- accessible error messages
- sufficient contrast
- appropriate heading hierarchy
- alt text for meaningful images
- appropriate ARIA only when necessary

Do not use an icon alone when its meaning is unclear and an accessible label is needed.

---

## 9. Frontend states

For interactive UI, consider the states required by the feature:

- default
- hover
- focus
- active/selected
- disabled
- loading
- empty
- validation error
- server/API error
- success

Implement only the states relevant to the feature and project.

Do not hide errors or create fake success behavior.

---

## 10. Keep frontend logic simple

Use the project's established frontend patterns.

Avoid:

- unnecessary state
- duplicated data-fetching logic
- large client-side abstractions for simple interactions
- unnecessary dependencies
- framework-specific patterns that conflict with the project
- mixing unrelated responsibilities

Frontend JavaScript/TypeScript should remain readable and focused.

---

## 11. Icons and assets

Use the project's existing icon and asset system.

Before adding a new icon or asset:

- check whether an existing project asset can be reused
- follow existing sizing and placement conventions
- use icons for meaning, not decoration
- avoid excessive icon density

Do not introduce a new icon library if the project already has one.

For images and other visual assets, follow the project's existing asset pipeline and optimization conventions.

---

## 12. Implement within existing styles

Prefer extending existing styles/components over creating duplicate versions.

If a new stylesheet/module is required:

- put it where the project expects frontend styles
- use the project's naming conventions
- scope styles appropriately
- avoid leaking page-specific styles globally
- reuse existing tokens and variables

Do not create multiple competing definitions for the same visual concept.

---

## 13. Output / implementation structure

When this skill is used during implementation:

### UI plan

Before substantial UI work, briefly identify:

- key UI sections
- important interaction decisions
- responsive behavior
- any assumptions that do not affect product requirements

Keep this short. It is an implementation orientation, not a replacement for the feature spec.

### Code

Implement the frontend using the project's actual file structure and technologies.

Keep related changes clear and focused.

### Integration

Ensure the UI is correctly connected to the project's:

- routes
- components
- data sources
- forms
- APIs
- state
- existing navigation
- existing layout

Do not leave placeholder wiring when the approved plan requires working integration.

---

## 14. Avoid

Avoid:

- generic template-like UI
- unrelated redesigns
- random colors
- inconsistent spacing
- excessive gradients
- excessive shadows
- unnecessary animations
- mystery-icon controls
- desktop-only layouts
- inaccessible forms
- duplicated components
- unnecessary dependencies
- changing the project's frontend technology
- changing unrelated screens

Do not redesign existing parts of the application simply because you prefer another style.

---

## 15. Handle ambiguity carefully

If the approved requirements leave a small visual detail unspecified, use the existing design system and make the smallest reasonable decision.

For example:

- choose an existing button variant
- reuse an existing card pattern
- follow an existing spacing scale
- use an existing responsive breakpoint

If the ambiguity changes product behavior or materially changes the user's workflow, stop and ask rather than inventing a requirement.

---

## 16. Verify frontend work

After implementing frontend changes:

- inspect the changed files
- check for broken imports/references
- run relevant project tests/checks
- run the project's build/type/lint commands when applicable
- manually verify the affected UI when the project can be run
- check responsive behavior
- check relevant UI states
- confirm existing UI was not unintentionally changed

Use commands documented in `GEMINI.md`.

Do not claim visual or functional verification that was not actually performed.

---

## Core rules

1. The approved specification and plan define what the feature should do.
2. `GEMINI.md` defines the project's actual frontend technology and conventions.
3. Existing UI is the primary reference for visual consistency.
4. Reuse existing components, tokens, patterns, and assets where appropriate.
5. Do not assume a particular frontend framework or styling system.
6. Do not introduce new frontend technologies without project/plan support.
7. Treat responsive behavior and accessibility as part of frontend implementation.
8. Implement relevant UI states instead of only the happy path.
9. Avoid unrelated redesigns and unnecessary abstractions.
10. Verify the frontend changes before considering the UI work complete.
