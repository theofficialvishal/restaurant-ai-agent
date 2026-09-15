---
name: create-spec
description: Create a complete implementation specification and feature branch for the requested project feature.
argument-hint: "Step number and feature name (e.g. 02 registration)"
allowed-tools: Read, Write, Glob, Bash(git:*)
---

# Create Specification

You are responsible for preparing the next feature specification for the current project.

Your goal is NOT to write implementation code.

Your only responsibility is to create a complete, evidence-based implementation specification that another AI or developer can safely implement.

Always follow every rule defined in `GEMINI.md`.

The project may use any technology stack. Never assume a specific framework, language, database, UI library, folder structure, package manager, or architecture. Use the current project's `GEMINI.md` and existing codebase as the source of truth.

## User Input

$ARGUMENTS

---

# Step 1 — Verify Working Directory

Run:

git status

If there are ANY:

- modified files
- staged files
- untracked files

STOP.

Tell the user:

"The working directory is not clean. Please commit or stash your changes before creating a new feature specification."

Do NOT continue.

---

# Step 2 — Parse User Arguments

Extract:

1. `step_number`
   - Zero-pad to two digits.
   - Examples:
     - `2` → `02`
     - `8` → `08`
     - `11` → `11`

2. `feature_title`
   - Human-readable Title Case.

3. `feature_slug`
   - Lowercase.
   - kebab-case.
   - Maximum 40 characters.
   - Allowed characters:
     - `a-z`
     - `0-9`
     - `-`

Example:

login-logout

4. `branch_name`

Use:

feature/<feature_slug>

Example:

feature/login-logout

If anything cannot be confidently inferred:

STOP.

Ask the user for clarification.

Do NOT guess.

---

# Step 3 — Verify Feature Understanding

Before creating or changing project files:

Summarize your understanding of the requested feature in 3–5 concise bullet points.

The summary should describe:

- what the feature does
- who or what it affects
- the expected user/system behaviour
- important boundaries or constraints already known

If the request is ambiguous:

STOP.

Ask follow-up questions.

Do NOT continue until the request is clear.

---

# Step 4 — Ensure Branch Name is Unique

Run:

git branch

If the branch already exists, append a numeric suffix.

Examples:

feature/login
feature/login-01
feature/login-02

Use the first available suffix.

---

# Step 5 — Identify and Update the Base Branch

Determine the project's default/base branch from the repository configuration or `GEMINI.md`.

Do not assume that the base branch is `main`.

If the base branch cannot be confidently determined:

STOP.

Ask the user for clarification.

Once identified, switch to the base branch and update it:

git checkout <base_branch>
git pull origin <base_branch>

If the pull fails:

STOP.

Report the error.

---

# Step 6 — Create Feature Branch

Create the feature branch from the updated base branch:

git checkout -b <branch_name>

---

# Step 7 — Research the Existing Project

Before writing the specification, read:

- `GEMINI.md`
- existing specifications in the project's documented specification directory
- the relevant files in the existing codebase
- relevant architecture, design, roadmap, or documentation files referenced by `GEMINI.md`

Use the project structure documented in `GEMINI.md` to determine which files are relevant.

Research the existing codebase carefully.

Every recommendation inside the specification MUST be supported by the existing project, the user's request, or documented project requirements.

Never invent:

- routes or API endpoints
- components
- services
- modules
- database tables
- schemas
- fields
- files
- folders
- libraries
- architecture
- authentication behaviour
- business rules

If information is missing:

Write:

"Not enough information."

Do NOT guess.

---

# Step 8 — Check for Duplicate or Already Completed Work

Compare the requested feature against:

- the project's roadmap, if one exists
- existing specifications
- the current implementation
- completion/progress information documented by the project

If the feature is already fully specified or implemented:

STOP.

Explain which specification, implementation, or project documentation already covers it.

Do NOT generate a duplicate specification.

If the project's documentation indicates that the requested roadmap step is already completed:

STOP.

Warn the user.

---

# Step 9 — Generate the Specification

Generate the specification using EXACTLY the following structure.

# Spec: <Feature Title>

## Overview

One paragraph describing the purpose of the feature, the problem it solves, and why it exists at this stage of the project.

---

## Feature Summary

3–5 bullet points describing the expected behaviour.

---

## Depends On

Previous roadmap steps, existing features, modules, or system capabilities required by this feature.

If none:

None.

---

## Non Goals

Explicitly state what this feature will NOT implement.

---

## Acceptance Criteria

A measurable checklist describing what the finished feature must achieve.

Every criterion should be testable or verifiable.

---

## API / Routes

Document API endpoints, routes, server actions, commands, or other external interfaces affected by the feature.

Use this table when applicable:

| Method / Type | Route / Interface | Access | Purpose |
|---|---|---|---|

If there are no API or route changes:

No API or route changes.

---

## Data / Storage Changes

Describe changes to the project's data or persistence layer.

### Existing Data Structures Affected

### New Data Structures

### Indexes / Performance

### Constraints / Relationships

### Migration Notes

If nothing changes:

No data or storage changes.

---

## UI Changes

Describe user-facing changes when applicable.

Include:

- Navigation
- Pages / Screens
- Components
- Forms
- Buttons / Actions
- Validation
- Success / Error / Flash Messages
- Loading / Empty / Error States
- Responsive Behaviour
- Accessibility considerations

If there are no UI changes:

No UI changes.

---

## Files to Modify

List every existing file that is expected to be modified.

For each file, briefly state what will change.

Do not list speculative files.

---

## Files to Create

List every new file that is expected to be created.

For each file, briefly state its responsibility.

Do not list speculative files.

---

## New Dependencies

List new dependencies only if the feature requires them.

For each dependency, explain why it is needed.

If none:

No new dependencies.

---

## Risks

Potential implementation risks.

Consider where relevant:

- Data migration
- Authentication
- Authorization
- Security
- Performance
- Concurrency
- Compatibility
- Existing feature regressions
- External service dependencies

If a risk cannot be determined from available information:

"Not enough information."

---

## Security Considerations

Always consider:

- Authentication
- Authorization
- Input Validation
- CSRF protection where applicable
- XSS prevention where applicable
- Injection prevention
- Parameterized database queries where applicable
- Secrets handling
- Password/security credential handling where applicable
- Sensitive data exposure

Only include controls relevant to the project's architecture, but do not omit a relevant security concern.

---

## Manual Test Plan

Describe manual testing scenarios including:

### Happy Path

### Validation Errors

### Edge Cases

### Authentication / Authorization

### Regression Checks

Use the project's actual UI, API, commands, and behaviour when describing the scenarios.

---

## Rules for Implementation

Always include:

- Follow `GEMINI.md` and all project-specific coding standards.
- Follow the existing project architecture and folder structure.
- Reuse existing utilities, helpers, components, services, and patterns whenever possible.
- Do not duplicate existing logic.
- Do not introduce a new abstraction when an existing one is appropriate.
- Validate external input at system boundaries.
- Preserve existing functionality and backward compatibility unless the specification explicitly requires a breaking change.
- Avoid unnecessary dependencies.
- Follow the project's existing styling and UI conventions.
- Follow the project's existing data-access and persistence conventions.
- Keep each module, component, route, or service focused on its responsibility.
- Do not make unrelated changes.

If the project has additional implementation rules in `GEMINI.md`, those rules take precedence over this generic list.

---

## Definition of Done

A checklist where every item can be verified.

Include, when applicable:

- Feature behaviour matches the acceptance criteria.
- All affected existing functionality continues to work.
- Validation and error handling are implemented.
- Authentication and authorization requirements are satisfied.
- Tests pass.
- Build/type checks/linting pass when defined by the project.
- No unrelated files or behaviour were changed.
- Documentation/progress tracking is updated as required by the project workflow.

---

# Step 10 — Validate the Specification

Before saving, verify:

✓ Every referenced existing file exists.

✓ Referenced routes, APIs, modules, components, and data structures match the existing project.

✓ No duplicated routes or interfaces are introduced.

✓ No duplicated templates, components, or modules are introduced.

✓ Data/storage changes match the existing data layer.

✓ Feature dependencies match the actual project.

✓ Feature follows the project's roadmap and scope.

✓ Specification does not contradict `GEMINI.md`.

✓ No technology-specific assumptions were invented.

✓ No assumptions were made without evidence.

✓ Acceptance criteria are measurable.

✓ The specification contains enough detail for another developer or AI to implement safely.

If validation fails:

Fix the specification before saving.

---

# Step 11 — Save the Spec

Save to:

.agents/specs/<step_number>-<feature_slug>.md

Create the directory if it does not already exist.

---

# Step 12 — Final Report

Print ONLY:

Branch: <branch_name>

Spec file: .agents/specs/<step_number>-<feature_slug>.md

Title: <feature_title>

Then tell the user:

Review the specification before proceeding.

Do not begin design, task breakdown, or implementation until the user explicitly approves the spec.
