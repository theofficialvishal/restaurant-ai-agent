---
name: build
description: Implement an approved feature plan incrementally, verify each task, and validate the completed feature without inventing requirements or making unrelated changes.
argument-hint: Plan path or step number and feature name...
allowed-tools: Read, Write, Glob, Bash
---

# Build

Implement an approved feature plan incrementally and safely.

You are the implementation engineer. Turn the approved plan into working code while following `GEMINI.md`, the approved specification, the approved plan, and the existing codebase.

Do not redesign requirements during implementation. Do not invent behavior that is not supported by the approved specification, plan, project context, or existing conventions.

## 1. Identify the approved plan

Determine which implementation plan the user wants to build.

The user may provide:
- a plan file path
- a feature/step number
- a feature name

If the plan cannot be identified unambiguously, stop and ask.

Read the selected plan completely.

## 2. Read project context

Before changing code, read:

1. `GEMINI.md`
2. The approved feature specification
3. The approved implementation plan
4. Relevant existing documentation
5. Relevant source code, templates, components, routes, services, models, tests, and configuration

Use the actual technology and project structure documented in `GEMINI.md`.

Do not assume a specific framework, database, language, styling system, or folder structure.

## 3. Verify approval

The plan must have been manually reviewed and approved by the user before implementation begins.

If there is no clear indication that the plan is approved, stop and ask for approval.

## 4. Verify repository state

Before implementation:

- Check git status.
- Confirm the correct feature branch if the project uses feature branches.
- Do not overwrite unrelated user changes.
- Do not reset, discard, or modify unrelated work.

If unexpected changes create a meaningful risk, stop and ask.

## 5. Reconcile the plan with the codebase

Compare the approved plan with the current implementation.

Check existing:
- architecture and boundaries
- reusable abstractions/components
- routes/API
- data models/storage
- UI patterns
- validation/error handling
- tests
- dependencies/configuration
- conventions in `GEMINI.md`

Reuse existing patterns where appropriate.

If the plan conflicts with the current architecture or reveals a material requirement that was not approved, do not silently invent a solution. Stop and surface the conflict.

## 6. Automatically use specialized skills when relevant

`build` remains the main implementation workflow, but specialized skills should be used automatically when their domain is involved.

### Frontend/UI work

If the feature includes frontend/UI work, automatically read and follow:

`.agents/skills/frontend-design/SKILL.md`

Use it for:
- pages/screens
- layouts
- components
- forms
- tables
- dashboards
- navigation
- modals/dialogs
- responsive behavior
- visual styling
- frontend interactions
- loading, empty, success, and error UI states

Do not require the user to separately invoke `frontend-design`.

The frontend skill does not replace `build`; it supplies specialized frontend rules while `build` remains responsible for the overall feature.

If the project does not contain a `frontend-design` skill, follow the frontend conventions in `GEMINI.md` and the existing codebase.

### Other specialized skills

Apply other project-specific skills automatically when their purpose clearly matches the work being implemented.

Do not use unrelated skills just because they exist.

## 7. Create an internal implementation checklist

Convert the approved plan into a small working checklist.

For each task, identify:
- files/components/modules involved
- implementation change
- dependencies on earlier tasks
- verification required
- acceptance criteria affected

Keep the checklist aligned with the approved plan.

## 8. Implement one task at a time

For each plan task:

1. Read the relevant existing code.
2. Make the smallest appropriate change.
3. Follow project conventions.
4. Verify the change immediately.
5. Continue only after the task is in a working state.

Avoid unrelated refactors.

## 9. Follow project conventions

Respect the conventions defined in `GEMINI.md` and existing code, including:
- language/framework conventions
- architecture boundaries
- naming and file organization
- validation and error handling
- security requirements
- database/storage conventions
- API conventions
- frontend/design conventions
- testing conventions
- dependency management

Do not introduce a new library, framework, pattern, or abstraction unless the approved plan or project context supports it.

## 10. Handle unexpected issues safely

If implementation reveals a missing requirement, contradiction, architecture conflict, security concern, destructive migration, or ambiguity that materially changes behavior, stop before making a speculative decision.

Small implementation details may be resolved using existing conventions. Material behavior or architecture changes require clarification or an updated approved plan.

## 11. Verify incrementally

After meaningful changes, run the smallest relevant verification available.

Examples:
- targeted tests
- type checking
- linting
- formatting checks
- build checks
- application startup
- API checks
- manual UI verification

Use commands documented in `GEMINI.md`. Do not assume commands such as `npm run build` or `pytest` exist unless documented or clearly established by the repository.

## 12. Validate the complete feature

After all plan tasks are implemented:

### Functional validation
Verify every acceptance criterion in the approved specification.

### Technical validation
Run the relevant project-documented tests, type checks, linting, formatting checks, build commands, and other validation.

### UI validation
If frontend work was involved:
- verify the UI against approved requirements
- verify existing design patterns were reused
- check responsive behavior where applicable
- check relevant loading/empty/error/success states
- confirm no unrelated UI changed

## 13. Review final changes

Before declaring the feature complete:

- inspect `git diff`
- inspect changed files
- confirm every change belongs to the feature
- check for debug code
- check for unused imports/dependencies
- check for obvious security issues
- confirm acceptance criteria are satisfied
- confirm no unrelated files changed

## 14. Final report

Report concisely:

### Implemented
- What was built
- Important files/components changed

### Specialized skills used
- Mention `frontend-design` when it was used.
- Mention other specialized skills that were actually used.

### Validation
- Tests/checks run
- Build/type/lint results
- Manual verification performed, if any

### Notes
- Known limitations
- Remaining issues or follow-ups
- Decisions requiring user attention

Never claim a check was run if it was not actually run.

## Core rules

1. Approved spec and plan are the source of truth for feature behavior.
2. `GEMINI.md` is the source of truth for project-specific technology, architecture, conventions, and commands.
3. Existing code is a source of truth for established implementation patterns.
4. Implement one plan task at a time.
5. Automatically use specialized skills when their domain is involved.
6. Frontend work must use `.agents/skills/frontend-design/SKILL.md` when that skill exists.
7. Never invent material requirements.
8. Never make unrelated changes.
9. Verify incrementally and validate the complete feature.
10. Do not automatically commit or push unless the approved project workflow explicitly requires it.
