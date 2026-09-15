---
name: create-plan
description: Create a detailed, implementation-ready development plan from an approved feature specification.
argument-hint: "Spec path or step number and feature name (e.g. 02 registration)"
allowed-tools: Read, Write, Glob, Bash(git:*)
---

# Create Implementation Plan

You are responsible for converting an approved feature specification into a clear,
implementation-ready development plan.

Your goal is NOT to implement the feature.

Your responsibility is to understand the approved specification and existing
project, then break the work into small, ordered, verifiable implementation tasks
that another AI or developer can execute safely.

Always follow every rule defined in `GEMINI.md`.

The project may use any technology stack. Never assume a specific framework,
language, database, UI library, package manager, folder structure, or architecture.
Use the project's `GEMINI.md`, approved specification, and existing codebase as
the sources of truth.

---

# User Input

$ARGUMENTS

---

# Step 1 — Identify the Specification

Determine which specification the user wants to plan.

The user may provide:

- a specification file path
- a step number
- a feature name

If the specification cannot be identified confidently:

STOP.

Ask the user for clarification.

Do NOT guess.

---

# Step 2 — Verify the Specification Exists

Read the identified specification.

If the specification does not exist:

STOP.

Tell the user that the specification could not be found.

Do NOT create a plan from memory or from an inferred feature description.

---

# Step 3 — Verify Specification Approval

The specification must have been reviewed and explicitly approved by the user
before planning begins.

Look for the project's documented approval convention or available project state.

If there is no reliable evidence that the specification has been approved:

STOP.

Tell the user:

"The specification has not been explicitly approved yet. Please review and
approve the specification before creating the implementation plan."

Do NOT continue.

---

# Step 4 — Read Project Context

Before creating the plan, read:

- `GEMINI.md`
- the approved specification
- relevant existing specifications
- relevant architecture/design documentation referenced by `GEMINI.md`
- relevant files in the existing codebase
- current progress information when available

Use `GEMINI.md` to determine the project's actual structure and relevant files.

Do not assume technology-specific details.

---

# Step 5 — Verify the Specification Against the Codebase

Research the relevant existing implementation.

Confirm:

- referenced files exist
- referenced modules/components/services exist
- referenced routes/APIs exist
- referenced data structures exist
- referenced dependencies exist
- existing patterns are understood
- the proposed changes fit the current architecture

Do not invent implementation details.

If the specification contradicts the existing codebase:

STOP.

Explain the contradiction and ask the user to resolve the specification before
planning.

If information required for planning is missing:

Write:

"Not enough information."

Do NOT guess.

---

# Step 6 — Identify the Implementation Boundaries

Determine the smallest meaningful implementation units required by the specification.

Group work by logical responsibility, for example:

- data/storage
- backend/API
- business logic
- frontend/UI
- integration
- validation
- testing
- documentation

Use only categories relevant to the project.

Do not create artificial tasks simply to make the plan longer.

---

# Step 7 — Create the Implementation Plan

Create a sequential plan.

Each task MUST:

- have a clear objective
- identify the files or areas involved
- describe the implementation change
- identify important dependencies
- be independently understandable
- be small enough to verify
- avoid unrelated work

Prefer tasks such as:

1. Prepare data/storage changes.
2. Implement reusable business logic.
3. Implement API/backend behaviour.
4. Implement UI behaviour.
5. Add validation and error handling.
6. Add or update tests.
7. Run validation/build checks.
8. Perform final regression checks.

Adapt the order to the actual architecture.

Do not blindly follow this example ordering.

---

# Step 8 — Define Dependencies and Order

For every task, explain what must exist before it can be started.

Example:

Task 2 depends on Task 1 because the service requires the new data structure.

The plan should make the implementation order obvious.

Avoid circular dependencies.

---

# Step 9 — Define Verification for Each Task

Every implementation task must include a concise verification method.

Examples:

- unit test passes
- API returns expected response
- page renders correctly
- validation rejects invalid input
- build/type check passes
- existing regression tests pass

Use the project's actual commands and conventions from `GEMINI.md`.

Do not invent commands.

---

# Step 10 — Identify Files

Create two explicit lists:

## Files to Modify

Only list files that the plan has evidence will need changes.

For each file, explain:

- why it changes
- what responsibility changes

## Files to Create

Only list files that the plan has evidence will need to be created.

For each file, explain:

- why it is needed
- what responsibility it owns

Do not list speculative files.

---

# Step 11 — Identify New Dependencies

Determine whether the approved specification requires new dependencies.

If yes:

- name the dependency
- explain why it is required
- identify where it will be used

If no:

No new dependencies.

Do not introduce dependencies merely because they are convenient.

---

# Step 12 — Identify Risks and Edge Cases

Review the implementation plan for:

- authentication/authorization issues
- validation issues
- data consistency
- migration concerns
- performance concerns
- concurrency concerns
- external service failures
- UI edge cases
- backward compatibility
- regression risks

Only include risks supported by the specification or existing project.

If a risk cannot be determined:

"Not enough information."

---

# Step 13 — Generate the Plan

Save the plan using the project's established planning/specification directory.

If the project does not document a planning directory, use:

.agents/plans/

Use the same step number and feature slug as the approved specification.

Example:

.agents/specs/02-registration.md
.agents/plans/02-registration.md

Use exactly this structure:

# Plan: <Feature Title>

## Goal

[What this implementation plan will accomplish.]

## Specification

[Path to the approved specification.]

## Implementation Strategy

[Short explanation of the overall implementation approach.]

## Tasks

### Task 1 — <Task Title>

**Objective**

[What this task accomplishes.]

**Files / Areas**

- `[path]` — [change]

**Implementation**

- [specific implementation step]
- [specific implementation step]

**Depends On**

None / [Task number]

**Verification**

- [How this task will be verified.]

### Task 2 — <Task Title>

Repeat the same structure for every task.

## Implementation Order

1. [Task]
2. [Task]
3. [Task]

## Files to Modify

- `[path]` — [reason]

## Files to Create

- `[path]` — [reason]

## New Dependencies

[Dependencies or "No new dependencies."]

## Risks & Edge Cases

- [Risk / edge case]
- [Risk / edge case]

## Validation Strategy

Describe the checks that must pass after implementation.

Include the project's relevant:

- tests
- build
- type checks
- linting
- formatting
- manual verification

Only include checks that actually apply to the project.

## Definition of Done

A measurable checklist derived from the approved specification.

---

# Step 14 — Validate the Plan

Before saving, verify:

✓ The plan is based on an approved specification.

✓ Every planned change is supported by the specification or existing codebase.

✓ Every referenced file exists or is explicitly listed as a file to create.

✓ No speculative files are included.

✓ No unrelated work is included.

✓ Implementation tasks are ordered logically.

✓ Dependencies between tasks are clear.

✓ Every task has a verification method.

✓ The plan follows `GEMINI.md`.

✓ The plan does not introduce undocumented architecture.

✓ The plan does not contradict the approved specification.

✓ The plan is detailed enough for another AI or developer to implement safely.

If validation fails:

Fix the plan before saving.

---

# Step 15 — Save the Plan

Save to:

.agents/plans/<step_number>-<feature_slug>.md

Create the directory if it does not already exist.

---

# Step 16 — Final Report

Print ONLY:

Plan file: .agents/plans/<step_number>-<feature_slug>.md

Title: <feature_title>

Then tell the user:

Review the implementation plan before proceeding.

Do not begin implementation until the user explicitly approves the plan.
